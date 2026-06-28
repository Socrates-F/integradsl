from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Set

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


class SemanticError(Exception):
    pass


@dataclass
class SymbolTable:
    scopes: List[Set[str]] = field(default_factory=lambda: [set()])

    def define(self, name: str) -> None:
        self.scopes[-1].add(name)

    def push(self) -> None:
        self.scopes.append(set())

    def pop(self) -> None:
        self.scopes.pop()

    def is_defined(self, name: str) -> bool:
        return any(name in scope for scope in reversed(self.scopes))


class SemanticAnalyzer:
    """Verificações semânticas simples antes da execução."""

    def __init__(self):
        self.symbols = SymbolTable()
        self.errors: List[str] = []
        self.loop_depth = 0

    def analyze(self, program: Program) -> None:
        self._visit_flow(program.flow)
        if self.errors:
            formatted = "\n".join(f"- {err}" for err in self.errors)
            raise SemanticError(f"Erros semânticos encontrados:\n{formatted}")

    def _visit_flow(self, flow: Flow) -> None:
        for statement in flow.statements:
            self._visit_statement(statement)

    def _visit_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, Config):
            self.symbols.define(stmt.name)
        elif isinstance(stmt, LoadFile):
            self.symbols.define(stmt.target)
        elif isinstance(stmt, Fetch):
            self.symbols.define(stmt.target)
        elif isinstance(stmt, Extract):
            self._require_path(stmt.source)
            self.symbols.define(stmt.target)
        elif isinstance(stmt, Loop):
            self._require_path(stmt.collection)
            self.loop_depth += 1
            self.symbols.push()
            self.symbols.define(stmt.item_name)
            for child in stmt.statements:
                self._visit_statement(child)
            self.symbols.pop()
            self.loop_depth -= 1
        elif isinstance(stmt, If):
            self._visit_condition(stmt.condition)
            self.symbols.push()
            for child in stmt.then_statements:
                self._visit_statement(child)
            self.symbols.pop()
            self.symbols.push()
            for child in stmt.else_statements:
                self._visit_statement(child)
            self.symbols.pop()
        elif isinstance(stmt, Validate):
            self._require_path(stmt.path)
            self._require_value_or_path(stmt.rule.argument)
        elif isinstance(stmt, SetField):
            self._require_path_root(stmt.path)
            self._require_value_or_path(stmt.value)
        elif isinstance(stmt, Save):
            self._require_path(stmt.path)
        elif isinstance(stmt, Send):
            self._require_path(stmt.payload)
        elif isinstance(stmt, Log):
            pass
        elif isinstance(stmt, SaveError):
            self._require_path(stmt.path)
        elif isinstance(stmt, Report):
            pass
        elif isinstance(stmt, Continue):
            if self.loop_depth == 0:
                self.errors.append("o comando 'continuar' só pode ser usado dentro de 'para cada'.")
        else:
            self.errors.append(f"comando desconhecido: {stmt!r}")

    def _visit_condition(self, condition) -> None:
        if isinstance(condition, ErrorCondition):
            return
        if isinstance(condition, ComparisonCondition):
            self._require_value_or_path(condition.left)
            self._require_value_or_path(condition.right)

    def _require_value_or_path(self, item) -> None:
        if item is None:
            return
        if isinstance(item, Value):
            return
        if isinstance(item, Path):
            self._require_path(item)

    def _require_path(self, path: Path) -> None:
        self._require_path_root(path)

    def _require_path_root(self, path: Path) -> None:
        root = path.parts[0]
        if not self.symbols.is_defined(root):
            self.errors.append(f"variável '{root}' usada antes de ser definida no caminho '{path}'.")
