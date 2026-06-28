from __future__ import annotations

from typing import Any, List

from .ast_nodes import (
    ComparisonCondition,
    Config,
    Continue,
    ErrorCondition,
    Extract,
    Fetch,
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
    Validate,
    Value,
)


class PythonTranslator:
    """Tradutor orientado à sintaxe: gera um Python didático equivalente ao fluxo."""

    def translate(self, program: Program) -> str:
        self.lines: List[str] = []
        self.indent = 0
        self._line("# Código Python gerado de forma didática pela IntegraDSL")
        self._line("# Este arquivo mostra a semântica do programa, mas o interpretador oficial é src/integradsl/interpreter.py")
        self._line("state = {'env': {}, 'logs': [], 'erros': [], 'banco': {}, 'envios': []}")
        self._line(f"# fluxo: {program.flow.name!r}")
        for stmt in program.flow.statements:
            self._stmt(stmt)
        return "\n".join(self.lines)

    def _stmt(self, stmt) -> None:
        if isinstance(stmt, Config):
            self._line(f"state['env'][{stmt.name!r}] = {self._value(stmt.value)}")
        elif isinstance(stmt, LoadFile):
            self._line(f"state['env'][{stmt.target!r}] = carregar_json({stmt.filename!r})")
        elif isinstance(stmt, Fetch):
            self._line(f"state['env'][{stmt.target!r}] = http_request({stmt.method!r}, {stmt.url!r})")
        elif isinstance(stmt, Extract):
            self._line(f"state['env'][{stmt.target!r}] = get_path({self._path(stmt.source)})")
        elif isinstance(stmt, Loop):
            self._line(f"for {stmt.item_name} in get_path({self._path(stmt.collection)}):")
            self.indent += 1
            self._line(f"state['env'][{stmt.item_name!r}] = {stmt.item_name}")
            self._line("state['last_error'] = False")
            for child in stmt.statements:
                self._stmt(child)
            self.indent -= 1
        elif isinstance(stmt, If):
            self._line(f"if {self._condition(stmt.condition)}:")
            self.indent += 1
            if stmt.then_statements:
                for child in stmt.then_statements:
                    self._stmt(child)
            else:
                self._line("pass")
            self.indent -= 1
            if stmt.else_statements:
                self._line("else:")
                self.indent += 1
                for child in stmt.else_statements:
                    self._stmt(child)
                self.indent -= 1
        elif isinstance(stmt, Validate):
            if isinstance(stmt.rule.argument, Value):
                arg = stmt.rule.argument.value
            else:
                arg = self._value(stmt.rule.argument) if stmt.rule.argument else None
            self._line(f"validar({self._path(stmt.path)}, regra={stmt.rule.name!r}, argumento={arg!r})")
        elif isinstance(stmt, SetField):
            self._line(f"set_path({self._path(stmt.path)}, {self._value(stmt.value)})")
        elif isinstance(stmt, Save):
            self._line(f"salvar_em_banco({self._path(stmt.path)}, tabela={stmt.table!r})")
        elif isinstance(stmt, Send):
            self._line(f"enviar_http({stmt.method!r}, {stmt.url!r}, payload={self._path(stmt.payload)})")
        elif isinstance(stmt, Log):
            self._line(f"state['logs'].append({stmt.message!r})")
        elif isinstance(stmt, SaveError):
            self._line(f"salvar_erro({self._path(stmt.path)})")
        elif isinstance(stmt, Report):
            self._line(f"gerar_relatorio({stmt.filename!r})")
        elif isinstance(stmt, Continue):
            self._line("continue")
        else:
            self._line(f"# comando desconhecido: {stmt!r}")

    def _condition(self, condition) -> str:
        if isinstance(condition, ErrorCondition):
            return "state.get('last_error', False)"
        if isinstance(condition, ComparisonCondition):
            return f"{self._operand(condition.left)} {condition.operator} {self._operand(condition.right)}"
        return "False"

    def _operand(self, operand: Any) -> str:
        if isinstance(operand, Path):
            return f"get_path({self._path(operand)})"
        if isinstance(operand, Value):
            return repr(operand.value)
        return repr(operand)

    def _value(self, value: Any) -> str:
        if isinstance(value, Value):
            return repr(value.value)
        if isinstance(value, Path):
            return f"get_path({self._path(value)})"
        return repr(value)

    def _path(self, path: Path) -> str:
        return repr(".".join(path.parts))

    def _line(self, text: str) -> None:
        self.lines.append("    " * self.indent + text)
