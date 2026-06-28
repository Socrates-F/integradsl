from pathlib import Path

from integradsl.parser import IntegraParser
from integradsl.semantic import SemanticAnalyzer


def test_parser_accepts_main_example():
    source = Path("examples/sincronizar_pedidos.integra").read_text(encoding="utf-8")
    parser = IntegraParser()
    program = parser.parse_ast(source)
    SemanticAnalyzer().analyze(program)
    assert program.flow.name == "Sincronizar pedidos locais"


def test_tree_is_generated():
    source = 'fluxo "Demo" { configurar x = 1 relatorio "r.json" }'
    parser = IntegraParser()
    tree = parser.parse_tree(source)
    assert tree.data == "start"
