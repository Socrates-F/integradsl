from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass(frozen=True)
class Path:
    parts: List[str]

    def __str__(self) -> str:
        return ".".join(self.parts)


@dataclass(frozen=True)
class Value:
    value: Any


@dataclass(frozen=True)
class Condition:
    pass


@dataclass(frozen=True)
class ErrorCondition(Condition):
    pass


@dataclass(frozen=True)
class ComparisonCondition(Condition):
    left: Any
    operator: str
    right: Any


@dataclass(frozen=True)
class Rule:
    name: str
    argument: Optional[Any] = None


@dataclass(frozen=True)
class Statement:
    pass


@dataclass(frozen=True)
class Flow:
    name: str
    statements: List[Statement] = field(default_factory=list)


@dataclass(frozen=True)
class Program:
    flow: Flow


@dataclass(frozen=True)
class Config(Statement):
    name: str
    value: Value


@dataclass(frozen=True)
class LoadFile(Statement):
    target: str
    filename: str


@dataclass(frozen=True)
class Fetch(Statement):
    target: str
    method: str
    url: str


@dataclass(frozen=True)
class Extract(Statement):
    target: str
    source: Path


@dataclass(frozen=True)
class Loop(Statement):
    item_name: str
    collection: Path
    statements: List[Statement]


@dataclass(frozen=True)
class If(Statement):
    condition: Condition
    then_statements: List[Statement]
    else_statements: List[Statement]


@dataclass(frozen=True)
class Validate(Statement):
    path: Path
    rule: Rule


@dataclass(frozen=True)
class SetField(Statement):
    path: Path
    value: Value


@dataclass(frozen=True)
class Save(Statement):
    path: Path
    table: str


@dataclass(frozen=True)
class Send(Statement):
    method: str
    url: str
    payload: Path


@dataclass(frozen=True)
class Log(Statement):
    message: str


@dataclass(frozen=True)
class SaveError(Statement):
    path: Path


@dataclass(frozen=True)
class Report(Statement):
    filename: str


@dataclass(frozen=True)
class Continue(Statement):
    pass
