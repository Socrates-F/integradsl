from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, field
from pathlib import Path as FsPath
from typing import Any, Dict, List, Optional

try:
    import requests
except Exception:  # pragma: no cover - permite rodar mesmo sem requests quando só há mock/local
    requests = None

from .ast_nodes import (
    ComparisonCondition,
    Config,
    Continue,
    ErrorCondition,
    Extract,
    Fetch,
    Flow,
    If,
    LoadFile,
    Log,
    Loop,
    Path,
    Program,
    Report,
    Save,
    SaveError,
    Send,
    SetField,
    Statement,
    Validate,
    Value,
)


class RuntimeFlowError(Exception):
    pass


class ContinueLoop(Exception):
    pass


@dataclass
class RuntimeState:
    env: Dict[str, Any] = field(default_factory=dict)
    database: Dict[str, List[Any]] = field(default_factory=dict)
    sent: List[Dict[str, Any]] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    last_error: bool = False
    last_error_detail: Optional[str] = None
    counters: Dict[str, int] = field(default_factory=lambda: {
        "registros_processados": 0,
        "registros_salvos": 0,
        "envios_sucesso": 0,
        "falhas_envio": 0,
        "validacoes_sucesso": 0,
        "validacoes_falha": 0,
    })


class IntegraInterpreter:
    """Interpretador orientado à sintaxe para a AST da IntegraDSL."""

    def __init__(self, base_dir: str | FsPath = ".", output_dir: str | FsPath = "outputs"):
        self.base_dir = FsPath(base_dir).resolve()
        self.output_dir = FsPath(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state = RuntimeState()
        self.flow_name = ""

    def run(self, program: Program) -> RuntimeState:
        self._execute_flow(program.flow)
        return self.state

    def _execute_flow(self, flow: Flow) -> None:
        self.flow_name = flow.name
        self.state.logs.append(f"Iniciando fluxo: {flow.name}")
        for statement in flow.statements:
            self._execute(statement)
        self.state.logs.append(f"Fluxo finalizado: {flow.name}")

    def _execute(self, stmt: Statement) -> None:
        if isinstance(stmt, Config):
            self.state.env[stmt.name] = self._resolve_value(stmt.value)
        elif isinstance(stmt, LoadFile):
            self._execute_load_file(stmt)
        elif isinstance(stmt, Fetch):
            self._execute_fetch(stmt)
        elif isinstance(stmt, Extract):
            self.state.env[stmt.target] = self._resolve_path(stmt.source)
        elif isinstance(stmt, Loop):
            self._execute_loop(stmt)
        elif isinstance(stmt, If):
            self._execute_if(stmt)
        elif isinstance(stmt, Validate):
            self._execute_validate(stmt)
        elif isinstance(stmt, SetField):
            self._set_path(stmt.path, self._resolve_value(stmt.value))
        elif isinstance(stmt, Save):
            self._execute_save(stmt)
        elif isinstance(stmt, Send):
            self._execute_send(stmt)
        elif isinstance(stmt, Log):
            self.state.logs.append(stmt.message)
        elif isinstance(stmt, SaveError):
            self._execute_save_error(stmt)
        elif isinstance(stmt, Report):
            self._execute_report(stmt)
        elif isinstance(stmt, Continue):
            raise ContinueLoop()
        else:
            raise RuntimeFlowError(f"Comando não implementado: {stmt!r}")

    def _execute_load_file(self, stmt: LoadFile) -> None:
        file_path = (self.base_dir / stmt.filename).resolve()
        if not file_path.exists():
            raise RuntimeFlowError(f"Arquivo não encontrado: {file_path}")
        with file_path.open("r", encoding="utf-8") as f:
            self.state.env[stmt.target] = json.load(f)
        self.state.logs.append(f"Arquivo carregado em '{stmt.target}': {stmt.filename}")

    def _execute_fetch(self, stmt: Fetch) -> None:
        url = self._substitute_url(stmt.url)
        if url.startswith("mock://"):
            self.state.env[stmt.target] = {"mock_url": url, "status": "ok"}
            self.state.last_error = False
            self.state.logs.append(f"GET simulado: {url}")
            return
        if requests is None:
            self._register_error(f"Biblioteca requests não disponível para buscar {url}")
            self.state.env[stmt.target] = None
            return
        try:
            response = requests.request(stmt.method, url, timeout=15)
            response.raise_for_status()
            try:
                self.state.env[stmt.target] = response.json()
            except ValueError:
                self.state.env[stmt.target] = response.text
            self.state.last_error = False
            self.state.last_error_detail = None
            self.state.logs.append(f"Requisição {stmt.method} concluída: {url}")
        except Exception as exc:
            self._register_error(f"Falha na requisição {stmt.method} {url}: {exc}")
            self.state.env[stmt.target] = None

    def _execute_loop(self, stmt: Loop) -> None:
        collection = self._resolve_path(stmt.collection)
        if not isinstance(collection, list):
            self._register_error(f"'{stmt.collection}' não é uma lista e não pode ser percorrido.")
            return
        previous_value = self.state.env.get(stmt.item_name, None)
        had_previous = stmt.item_name in self.state.env
        for index, item in enumerate(collection, start=1):
            self.state.counters["registros_processados"] += 1
            self.state.env[stmt.item_name] = item
            self.state.last_error = False
            self.state.last_error_detail = None
            try:
                for child in stmt.statements:
                    self._execute(child)
            except ContinueLoop:
                self.state.logs.append(f"Iteração {index} ignorada por comando 'continuar'.")
                continue
        if had_previous:
            self.state.env[stmt.item_name] = previous_value
        else:
            self.state.env.pop(stmt.item_name, None)

    def _execute_if(self, stmt: If) -> None:
        branch = stmt.then_statements if self._eval_condition(stmt.condition) else stmt.else_statements
        for child in branch:
            self._execute(child)

    def _execute_validate(self, stmt: Validate) -> None:
        try:
            value = self._resolve_path(stmt.path)
        except RuntimeFlowError:
            value = None
        rule = stmt.rule
        ok = True
        expected = self._resolve_value(rule.argument) if rule.argument is not None else None

        if rule.name == "obrigatorio":
            ok = value is not None and value != ""
        elif rule.name == "formato_email":
            ok = isinstance(value, str) and re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) is not None
        elif rule.name == "maior_que":
            ok = value is not None and value > expected
        elif rule.name == "menor_que":
            ok = value is not None and value < expected
        elif rule.name == "igual":
            ok = value == expected
        else:
            raise RuntimeFlowError(f"Regra de validação desconhecida: {rule.name}")

        if ok:
            self.state.counters["validacoes_sucesso"] += 1
        else:
            self.state.counters["validacoes_falha"] += 1
            self._register_error(f"Validação falhou: {stmt.path} deve atender à regra '{rule.name}'.")

    def _execute_save(self, stmt: Save) -> None:
        data = copy.deepcopy(self._resolve_path(stmt.path))
        self.state.database.setdefault(stmt.table, []).append(data)
        self.state.counters["registros_salvos"] += 1
        self.state.last_error = False
        self.state.last_error_detail = None
        self.state.logs.append(f"Registro salvo na tabela lógica '{stmt.table}'.")

    def _execute_send(self, stmt: Send) -> None:
        url = self._substitute_url(stmt.url)
        payload = copy.deepcopy(self._resolve_path(stmt.payload))
        if url.startswith("mock://"):
            self.state.sent.append({"method": stmt.method, "url": url, "payload": payload, "status_code": 200})
            self.state.counters["envios_sucesso"] += 1
            self.state.last_error = False
            self.state.last_error_detail = None
            self.state.logs.append(f"Envio simulado para {url}.")
            return
        if requests is None:
            self.state.counters["falhas_envio"] += 1
            self._register_error(f"Biblioteca requests não disponível para enviar {url}")
            return
        try:
            response = requests.request(stmt.method, url, json=payload, timeout=15)
            if response.status_code >= 400:
                self.state.counters["falhas_envio"] += 1
                self._register_error(f"Envio retornou status {response.status_code}: {url}")
            else:
                self.state.counters["envios_sucesso"] += 1
                self.state.sent.append({
                    "method": stmt.method,
                    "url": url,
                    "payload": payload,
                    "status_code": response.status_code,
                })
                self.state.last_error = False
                self.state.last_error_detail = None
                self.state.logs.append(f"Envio concluído para {url}.")
        except Exception as exc:
            self.state.counters["falhas_envio"] += 1
            self._register_error(f"Falha ao enviar {stmt.method} {url}: {exc}")

    def _execute_save_error(self, stmt: SaveError) -> None:
        try:
            reference = self._resolve_path(stmt.path)
        except RuntimeFlowError:
            reference = str(stmt.path)
        self.state.errors.append({
            "referencia": reference,
            "detalhe": self.state.last_error_detail or "Erro não detalhado",
        })
        self.state.logs.append(f"Erro salvo para referência: {reference}")

    def _execute_report(self, stmt: Report) -> None:
        report_path = (self.output_dir / stmt.filename).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "fluxo": self.flow_name,
            "contadores": self.state.counters,
            "logs": self.state.logs,
            "erros": self.state.errors,
            "banco_logico": self.state.database,
            "envios": self.state.sent,
        }
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        self.state.logs.append(f"Relatório gerado: {report_path}")

    def _eval_condition(self, condition) -> bool:
        if isinstance(condition, ErrorCondition):
            return self.state.last_error
        if isinstance(condition, ComparisonCondition):
            left = self._resolve_value(condition.left)
            right = self._resolve_value(condition.right)
            op = condition.operator
            if op == ">":
                return left > right
            if op == "<":
                return left < right
            if op == ">=":
                return left >= right
            if op == "<=":
                return left <= right
            if op == "==":
                return left == right
            if op == "!=":
                return left != right
        raise RuntimeFlowError(f"Condição inválida: {condition!r}")

    def _resolve_value(self, item) -> Any:
        if isinstance(item, Value):
            return item.value
        if isinstance(item, Path):
            return self._resolve_path(item)
        return item

    def _resolve_path(self, path: Path) -> Any:
        root = path.parts[0]
        if root not in self.state.env:
            raise RuntimeFlowError(f"Variável não definida: {root}")
        current = self.state.env[root]
        for part in path.parts[1:]:
            if isinstance(current, dict):
                if part not in current:
                    raise RuntimeFlowError(f"Campo '{part}' não existe em '{path}'.")
                current = current[part]
            else:
                raise RuntimeFlowError(f"Não é possível acessar '{part}' em valor não estruturado: {current!r}")
        return current

    def _set_path(self, path: Path, value: Any) -> None:
        if len(path.parts) == 1:
            self.state.env[path.parts[0]] = value
            return
        root = path.parts[0]
        if root not in self.state.env:
            raise RuntimeFlowError(f"Variável não definida: {root}")
        current = self.state.env[root]
        for part in path.parts[1:-1]:
            if not isinstance(current, dict):
                raise RuntimeFlowError(f"Não é possível definir campo em valor não estruturado: {current!r}")
            current = current.setdefault(part, {})
        if not isinstance(current, dict):
            raise RuntimeFlowError(f"Não é possível definir campo final em valor não estruturado: {current!r}")
        current[path.parts[-1]] = value

    def _substitute_url(self, url: str) -> str:
        def replace(match):
            raw_path = match.group(1)
            value = self._resolve_path(Path(raw_path.split(".")))
            return str(value)
        return re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\}", replace, url)

    def _register_error(self, detail: str) -> None:
        self.state.last_error = True
        self.state.last_error_detail = detail
        self.state.logs.append(f"ERRO: {detail}")
