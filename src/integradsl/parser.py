from __future__ import annotations

import ast
from pathlib import Path as FsPath
from typing import Iterable

from lark import Lark, Token, Transformer, Tree

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
    Rule,
    Save,
    SaveError,
    Send,
    SetField,
    Validate,
    Value,
)


def _unquote(token: Token | str) -> str:
    return ast.literal_eval(str(token))


class AstBuilder(Transformer):
    """Transforma a árvore concreta produzida pelo Lark em uma AST própria."""

    def start(self, children):
        return Program(children[0])

    def fluxo(self, children):
        name = _unquote(children[0])
        statements = children[1]
        return Flow(name=name, statements=statements)

    def bloco(self, children):
        return list(children)

    def configurar(self, children):
        return Config(name=str(children[0]), value=children[1])

    def carregar_arquivo(self, children):
        return LoadFile(target=str(children[0]), filename=_unquote(children[1]))

    def buscar(self, children):
        return Fetch(target=str(children[0]), method=str(children[1]), url=_unquote(children[2]))

    def extrair(self, children):
        return Extract(target=str(children[0]), source=children[1])

    def repeticao(self, children):
        return Loop(item_name=str(children[0]), collection=children[1], statements=children[2])

    def condicional(self, children):
        condition = children[0]
        then_statements = children[1]
        else_statements = children[2] if len(children) > 2 else []
        return If(condition=condition, then_statements=then_statements, else_statements=else_statements)

    def validar(self, children):
        return Validate(path=children[0], rule=children[1])

    def definir(self, children):
        return SetField(path=children[0], value=children[1])

    def salvar(self, children):
        return Save(path=children[0], table=_unquote(children[1]))

    def enviar(self, children):
        return Send(method=str(children[0]), url=_unquote(children[1]), payload=children[2])

    def registrar(self, children):
        return Log(message=_unquote(children[0]))

    def salvar_erro(self, children):
        return SaveError(path=children[0])

    def relatorio(self, children):
        return Report(filename=_unquote(children[0]))

    def continuar(self, _children):
        return Continue()

    def cond_erro(self, _children):
        return ErrorCondition()

    def cond_comparacao(self, children):
        return ComparisonCondition(left=children[0], operator=str(children[1]), right=children[2])

    def caminho(self, children):
        return Path(parts=[str(child) for child in children])

    def string(self, children):
        return Value(_unquote(children[0]))

    def number(self, children):
        text = str(children[0])
        if "." in text:
            return Value(float(text))
        return Value(int(text))

    def true(self, _children):
        return Value(True)

    def false(self, _children):
        return Value(False)

    def regra_obrigatorio(self, _children):
        return Rule("obrigatorio")

    def regra_email(self, _children):
        return Rule("formato_email")

    def regra_maior(self, children):
        return Rule("maior_que", children[0])

    def regra_menor(self, children):
        return Rule("menor_que", children[0])

    def regra_igual(self, children):
        return Rule("igual", children[0])


class IntegraParser:
    """Fachada do analisador léxico/sintático."""

    def __init__(self):
        grammar_path = FsPath(__file__).with_name("grammar.lark")
        self.grammar = grammar_path.read_text(encoding="utf-8")
        self.lark = Lark(
            self.grammar,
            parser="lalr",
            lexer="contextual",
            propagate_positions=True,
            maybe_placeholders=False,
        )
        self.builder = AstBuilder()

    def lex(self, source: str) -> Iterable[Token]:
        return self.lark.lex(source)

    def parse_tree(self, source: str) -> Tree:
        return self.lark.parse(source)

    def parse_ast(self, source: str) -> Program:
        tree = self.parse_tree(source)
        return self.builder.transform(tree)
