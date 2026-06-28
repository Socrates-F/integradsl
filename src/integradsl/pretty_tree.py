from lark import Tree


# Ícones para cada tipo de nó
NODE_LABELS = {
    "start": "🚀 Programa",
    "fluxo": "📋 Fluxo",
    "bloco": "📦 Bloco",
    "configurar": "⚙ Configurar",
    "carregar_arquivo": "📂 Carregar Arquivo",
    "extrair": "📤 Extrair",
    "repeticao": "🔁 Para Cada",
    "validar": "✔ Validar",
    "condicional": "❓ Condicional",
    "definir": "✏ Definir",
    "salvar": "💾 Salvar",
    "enviar": "🌐 Enviar",
    "registrar": "📝 Registrar",
    "salvar_erro": "❌ Salvar Erro",
    "relatorio": "📄 Relatório",
    "caminho": "📍 Caminho",
    "string": "📝 Texto",
    "number": "🔢 Número",
}


def print_tree(tree):
    print("\n=== ÁRVORE SINTÁTICA PERSONALIZADA ===\n")
    _print_node(tree)


def _print_node(node, prefix="", is_last=True):

    connector = "└── " if is_last else "├── "

    if isinstance(node, Tree):

        label = NODE_LABELS.get(node.data, node.data)

        print(prefix + connector + label)

        children = node.children

        new_prefix = prefix + ("    " if is_last else "│   ")

        for i, child in enumerate(children):
            last = i == len(children) - 1
            _print_node(child, new_prefix, last)

    else:

        print(prefix + connector + f"📄 {node}")