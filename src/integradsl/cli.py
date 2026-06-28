from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lark import UnexpectedInput

from .interpreter import IntegraInterpreter, RuntimeFlowError
from .parser import IntegraParser
from .semantic import SemanticAnalyzer, SemanticError
from .translator import PythonTranslator


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="integradsl",
        description="IntegraDSL - DSL para automação de integrações operacionais com Lark.",
    )
    parser.add_argument("arquivo", help="Arquivo .integra a ser executado")
    parser.add_argument("--tokens", action="store_true", help="Mostra os tokens reconhecidos pelo analisador léxico")
    parser.add_argument("--tree", action="store_true", help="Mostra a árvore sintática concreta gerada pelo Lark")
    parser.add_argument("--emit-python", action="store_true", help="Mostra uma tradução didática do programa para Python")
    parser.add_argument("--no-run", action="store_true", help="Apenas analisa/traduz, sem interpretar o programa")
    parser.add_argument("--outdir", default="outputs", help="Diretório para relatórios gerados pela execução")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    source_path = Path(args.arquivo)
    if not source_path.exists():
        print(f"Arquivo não encontrado: {source_path}", file=sys.stderr)
        return 1

    source = source_path.read_text(encoding="utf-8")
    parser = IntegraParser()

    try:
        if args.tokens:
            print("\n=== TOKENS ===")
            for token in parser.lex(source):
                print(f"{token.type:<15} {token.value}")

        tree = parser.parse_tree(source)
        if args.tree:
            print("\n=== ÁRVORE SINTÁTICA LARK ===")
            print(tree.pretty())

        ast_program = parser.parse_ast(source)
        SemanticAnalyzer().analyze(ast_program)

        if args.emit_python:
            print("\n=== TRADUÇÃO DIDÁTICA PARA PYTHON ===")
            print(PythonTranslator().translate(ast_program))

        if args.no_run:
            print("\nAnálise concluída com sucesso. Execução ignorada por --no-run.")
            return 0

        interpreter = IntegraInterpreter(base_dir=source_path.parent, output_dir=args.outdir)
        state = interpreter.run(ast_program)
        print("\n=== EXECUÇÃO CONCLUÍDA ===")
        print(f"Registros processados: {state.counters['registros_processados']}")
        print(f"Registros salvos: {state.counters['registros_salvos']}")
        print(f"Envios simulados/reais com sucesso: {state.counters['envios_sucesso']}")
        print(f"Falhas de validação: {state.counters['validacoes_falha']}")
        print(f"Falhas de envio: {state.counters['falhas_envio']}")
        print("Confira o diretório de saída para os relatórios gerados.")
        return 0

    except UnexpectedInput as exc:
        print("Erro sintático/léxico no programa IntegraDSL:", file=sys.stderr)
        print(exc, file=sys.stderr)
        return 2
    except SemanticError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except RuntimeFlowError as exc:
        print(f"Erro em tempo de execução: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
