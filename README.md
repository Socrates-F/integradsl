# IntegraDSL

**IntegraDSL** é uma linguagem de domínio específico, implementada com **Python** e **Lark**, criada para automatizar fluxos repetitivos de integração entre sistemas.

A linguagem permite descrever, em uma sintaxe própria, tarefas comuns em estágios e no mercado de computação, como:

* carregar dados de arquivos JSON;
* consumir APIs externas;
* validar campos obrigatórios;
* aplicar regras de negócio;
* transformar registros;
* salvar dados em uma base lógica em memória;
* enviar dados para outro sistema;
* tratar erros;
* gerar relatórios finais de execução.

O projeto foi desenvolvido seguindo a estrutura típica de um compilador/interpretador: **gramática formal**, **análise léxica**, **análise sintática**, **geração de árvore sintática**, **construção de AST**, **análise semântica**, **tradução orientada à sintaxe** e **interpretação**.

---

## Equipe

* Claudio Roberto
* Eduardo José
* Erasmo Alves
* Sócrates Farias


---

## Motivação

Em ambientes reais de desenvolvimento, é comum encontrar tarefas repetitivas relacionadas à integração entre sistemas. Por exemplo:

> Buscar pedidos em uma API, validar campos obrigatórios, transformar os dados, enviar para um ERP, registrar erros e gerar um relatório final.

Normalmente, esse tipo de automação é feito com scripts Python repetitivos, contendo muito código de requisição HTTP, validação, laços, condicionais, tratamento de erro e geração de logs.

A proposta da **IntegraDSL** é permitir que esse fluxo seja descrito por meio de uma linguagem mais próxima do domínio do problema, tornando a automação mais legível e reduzindo a complexidade de escrever scripts repetitivos.

---

## Descrição informal da linguagem

A IntegraDSL descreve um **fluxo de integração**. Todo programa começa com a palavra reservada `fluxo`, seguida de um nome e de um bloco de comandos.

Exemplo mínimo:

```txt
fluxo "Demo" {
    configurar ambiente = "teste"
    relatorio "relatorio_demo.json"
}
```

A linguagem possui comandos específicos para integração de dados:

| Comando       | Função                                              |
| ------------- | --------------------------------------------------- |
| `configurar`  | cria uma variável de configuração                   |
| `carregar`    | carrega dados de um arquivo JSON local              |
| `buscar`      | executa uma requisição HTTP externa                 |
| `extrair`     | extrai um campo de uma estrutura JSON               |
| `para cada`   | percorre uma lista de registros                     |
| `validar`     | aplica uma regra de validação                       |
| `se/senao`    | executa comandos condicionalmente                   |
| `se erro`     | verifica se o último comando gerou erro             |
| `definir`     | cria ou altera um campo de um registro              |
| `salvar`      | armazena um registro em uma base lógica em memória  |
| `enviar`      | envia um registro para uma API ou endpoint simulado |
| `registrar`   | adiciona uma mensagem aos logs                      |
| `salvar_erro` | registra um erro associado a um identificador       |
| `continuar`   | pula para a próxima iteração de um laço             |
| `relatorio`   | gera um relatório JSON da execução                  |

A IntegraDSL é uma linguagem **interpretada**, mas o projeto também possui um tradutor didático que exibe uma representação aproximada do programa em Python.

---

## Estrutura do projeto

```txt
integradsl_project/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .devcontainer/
│   └── devcontainer.json
├── data/
│   ├── pedidos.json
│   └── usuarios.json
├── examples/
│   ├── api_get_post_real.integra
│   ├── api_real_opcional.integra
│   ├── erro_semantico.integra
│   ├── erro_sintatico.integra
│   ├── sincronizar_pedidos.integra
│   └── validar_usuarios.integra
├── src/
│   └── integradsl/
│       ├── __init__.py
│       ├── __main__.py
│       ├── ast_nodes.py
│       ├── cli.py
│       ├── grammar.lark
│       ├── interpreter.py
│       ├── parser.py
│       ├── semantic.py
│       └── translator.py
└── tests/
    └── test_parser.py
```

---

## Função dos principais arquivos

| Arquivo          | Função                                      |
| ---------------- | ------------------------------------------- |
| `grammar.lark`   | define formalmente a gramática da linguagem |
| `parser.py`      | cria o analisador léxico/sintático com Lark |
| `ast_nodes.py`   | define os nós da AST                        |
| `semantic.py`    | realiza a análise semântica                 |
| `interpreter.py` | executa os programas escritos na DSL        |
| `translator.py`  | gera uma tradução didática para Python      |
| `cli.py`         | implementa a interface de linha de comando  |
| `examples/`      | contém programas de exemplo da DSL          |
| `data/`          | contém dados JSON usados nos testes offline |
| `tests/`         | contém testes automatizados com Pytest      |

---

## Fluxo interno de execução

O projeto segue as etapas clássicas de uma linguagem interpretada:

```txt
Arquivo .integra
      ↓
Análise léxica
      ↓
Tokens
      ↓
Análise sintática
      ↓
Árvore sintática do Lark
      ↓
AST própria
      ↓
Análise semântica
      ↓
Interpretador
      ↓
Relatório final
```

---

## Instalação em máquina local

### 1. Clonar ou baixar o projeto

Entre na pasta do projeto:

```bash
cd integradsl_project
```

No Windows, por exemplo:

```powershell
cd C:\Users\seu_usuario\integradsl_project
```

### 2. Criar ambiente virtual

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação com erro de política de execução, rode:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
pip install -e .
```

O comando `pip install -e .` instala o projeto em modo editável e permite usar o comando:

```bash
integradsl
```

---

## Execução no GitHub Codespaces

O projeto já possui a pasta `.devcontainer/`, permitindo uso no GitHub Codespaces.

### Passos

1. Suba o projeto para um repositório no GitHub.
2. Abra o repositório no navegador.
3. Clique em **Code**.
4. Acesse a aba **Codespaces**.
5. Clique em **Create codespace on main**.
6. No terminal do Codespaces, execute:

```bash
pip install -r requirements.txt
pip install -e .
```

Depois rode o exemplo principal:

```bash
integradsl examples/sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs
```

Caso prefira executar sem instalar o pacote em modo editável:

```bash
PYTHONPATH=src python -m integradsl examples/sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs
```

---

## Exemplo principal da linguagem

Arquivo:

```txt
examples/sincronizar_pedidos.integra
```

Código:

```txt
fluxo "Sincronizar pedidos locais" {
    configurar ambiente = "homologacao"

    carregar resposta de arquivo "../data/pedidos.json"
    extrair pedidos = resposta.carts

    para cada pedido em pedidos {
        validar pedido.id obrigatorio
        validar pedido.total maior_que 0

        se erro {
            registrar "Pedido inválido encontrado; envio cancelado."
            salvar_erro pedido.id
            continuar
        }

        se pedido.total > 1000 {
            definir pedido.prioridade = "alta"
        } senao {
            definir pedido.prioridade = "normal"
        }

        salvar pedido em "pedidos_integrados"
        enviar POST "mock://erp/pedidos" com pedido

        se erro {
            registrar "Falha no envio do pedido para o ERP."
            salvar_erro pedido.id
        }
    }

    relatorio "relatorio_sincronizacao_pedidos.json"
}
```

Esse programa realiza o seguinte fluxo:

1. carrega pedidos de um arquivo JSON local;
2. extrai a lista de pedidos;
3. percorre cada pedido;
4. valida os campos `id` e `total`;
5. se houver erro, registra a falha e pula para o próximo item;
6. define a prioridade como `alta` ou `normal`;
7. salva o pedido em uma base lógica;
8. simula o envio para um ERP;
9. gera um relatório final em JSON.

---

## Como executar o exemplo principal

```bash
integradsl examples/sincronizar_pedidos.integra --outdir outputs
```

No Windows PowerShell:

```powershell
integradsl examples\sincronizar_pedidos.integra --outdir outputs
```

Saída esperada:

```txt
=== EXECUÇÃO CONCLUÍDA ===
Registros processados: 4
Registros salvos: 3
Envios simulados/reais com sucesso: 3
Falhas de validação: 1
Falhas de envio: 0
Confira o diretório de saída para os relatórios gerados.
```

O relatório será gerado em:

```txt
outputs/relatorio_sincronizacao_pedidos.json
```

---

## Exemplos e testes disponíveis

A pasta `examples/` contém programas escritos na IntegraDSL que demonstram diferentes comportamentos da linguagem. Alguns exemplos executam fluxos válidos, enquanto outros foram criados propositalmente para demonstrar erros sintáticos ou semânticos.

> No Windows, use `examples\arquivo.integra`.
> No Linux, macOS ou Codespaces, use `examples/arquivo.integra`.

| Arquivo                       | Tipo de teste              | Descrição                                                                                                                                                                             | Comando                                                            |
| ----------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `sincronizar_pedidos.integra` | Execução principal offline | Executa o fluxo principal da DSL usando um arquivo JSON local. Carrega pedidos, valida campos, define prioridade, salva registros válidos, simula envio para um ERP e gera relatório. | `integradsl examples/sincronizar_pedidos.integra --outdir outputs` |
| `validar_usuarios.integra`    | Validação de dados         | Executa um fluxo alternativo para validar usuários. Testa campos como `id`, `email` e `idade`, demonstrando reutilização da linguagem em outro conjunto de dados.                     | `integradsl examples/validar_usuarios.integra --outdir outputs`    |
| `api_real_opcional.integra`   | API externa real           | Consome uma API pública real usando o comando `buscar`. Demonstra que a DSL consegue obter dados externos, processá-los, validá-los e gerar relatório.                                | `integradsl examples/api_real_opcional.integra --outdir outputs`   |
| `api_get_post_real.integra`   | GET e POST externos        | Testa uma requisição `GET` em API pública e um envio `POST` para um endpoint externo de teste. Depende de conexão com a internet.                                                     | `integradsl examples/api_get_post_real.integra --outdir outputs`   |
| `erro_sintatico.integra`      | Erro sintático             | Programa propositalmente incorreto para demonstrar que o analisador sintático rejeita código mal formado, como blocos não fechados corretamente.                                      | `integradsl examples/erro_sintatico.integra --tree --no-run`       |
| `erro_semantico.integra`      | Erro semântico             | Programa sintaticamente válido, mas semanticamente incorreto. Demonstra que a análise semântica detecta o uso de variável antes de sua definição.                                     | `integradsl examples/erro_semantico.integra --tree --no-run`       |

---

## Testes de etapas do compilador/interpretador

Além de executar os programas da pasta `examples/`, também é possível testar partes específicas do compilador/interpretador.

| Teste                | O que demonstra                                                 | Comando                                                                                          |
| -------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Ajuda da CLI         | Mostra os comandos disponíveis na ferramenta.                   | `integradsl --help`                                                                              |
| Análise léxica       | Exibe os tokens reconhecidos pelo Lark.                         | `integradsl examples/sincronizar_pedidos.integra --tokens --no-run`                              |
| Análise sintática    | Exibe a árvore sintática gerada pelo Lark.                      | `integradsl examples/sincronizar_pedidos.integra --tree --no-run`                                |
| Tradução para Python | Mostra uma tradução didática da DSL para Python.                | `integradsl examples/sincronizar_pedidos.integra --emit-python --no-run`                         |
| Teste completo       | Mostra tokens, árvore sintática, tradução e executa o programa. | `integradsl examples/sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs` |
| Testes automatizados | Executa os testes automatizados com Pytest.                     | `pytest -q`                                                                                      |

---

## Visualização dos relatórios

Após executar um fluxo com `--outdir outputs`, os relatórios são gerados na pasta `outputs/`.

Para visualizar o relatório principal:

```bash
python -m json.tool outputs/relatorio_sincronizacao_pedidos.json
```

Para visualizar o relatório da API pública:

```bash
python -m json.tool outputs/relatorio_api_publica.json
```

No Windows PowerShell também é possível visualizar partes específicas do relatório:

```powershell
(Get-Content outputs\relatorio_sincronizacao_pedidos.json -Raw | ConvertFrom-Json).logs
```

```powershell
(Get-Content outputs\relatorio_sincronizacao_pedidos.json -Raw | ConvertFrom-Json).contadores
```

```powershell
(Get-Content outputs\relatorio_sincronizacao_pedidos.json -Raw | ConvertFrom-Json).banco_logico
```

---

## Observação sobre os testes de erro

Os arquivos `erro_sintatico.integra` e `erro_semantico.integra` foram criados para falhar propositalmente.

Eles são importantes porque demonstram que o projeto diferencia:

* erro léxico/sintático: problema na forma do programa;
* erro semântico: programa escrito corretamente, mas com significado inválido;
* erro em tempo de execução: problema que ocorre durante a execução do fluxo.

Portanto, ao executar esses arquivos e receber uma mensagem de erro, isso indica que o compilador/interpretador está detectando corretamente programas inválidos.

### A seguir, segue as demais descrições dos testes vistos acima para melhor visualização de seus escopos.

### 1. Ajuda da CLI

Mostra os parâmetros aceitos pelo interpretador.

```bash
integradsl --help
```

Alternativa:

```bash
python -m integradsl --help
```

### 2. Teste de análise léxica

Mostra os tokens reconhecidos pelo Lark.

```bash
integradsl examples/sincronizar_pedidos.integra --tokens --no-run
```

No Windows:

```powershell
integradsl examples\sincronizar_pedidos.integra --tokens --no-run
```

Esse teste demonstra a etapa de **análise léxica**.

### 3. Teste de análise sintática

Mostra a árvore sintática concreta gerada pelo Lark.

```bash
integradsl examples/sincronizar_pedidos.integra --tree --no-run
```

No Windows:

```powershell
integradsl examples\sincronizar_pedidos.integra --tree --no-run
```

Esse teste demonstra a etapa de **análise sintática** e a geração da árvore.

### 4. Teste de tradução didática para Python

Mostra uma tradução aproximada do programa da DSL para Python.

```bash
integradsl examples/sincronizar_pedidos.integra --emit-python --no-run
```

No Windows:

```powershell
integradsl examples\sincronizar_pedidos.integra --emit-python --no-run
```

Esse teste demonstra a presença de um **tradutor orientado à sintaxe**.

### 5. Teste completo

Executa tokens, árvore, tradução e interpretação no mesmo comando.

```bash
integradsl examples/sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs
```

No Windows:

```powershell
integradsl examples\sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs
```

Esse é o comando mais indicado para demonstração do projeto.

### 6. Teste com validação de usuários

Arquivo:

```txt
examples/validar_usuarios.integra
```

Execução:

```bash
integradsl examples/validar_usuarios.integra --outdir outputs
```

No Windows:

```powershell
integradsl examples\validar_usuarios.integra --outdir outputs
```

Esse exemplo demonstra reutilização da linguagem em outro domínio de dados, validando usuários, e-mails e idade.

Para visualizar o relatório:

```bash
python -m json.tool outputs/relatorio_validacao_usuarios.json
```

No Windows:

```powershell
python -m json.tool outputs\relatorio_validacao_usuarios.json
```

### 7. Teste com API externa real

Arquivo:

```txt
examples/api_real_opcional.integra
```

Execução:

```bash
integradsl examples/api_real_opcional.integra --outdir outputs
```

No Windows:

```powershell
integradsl examples\api_real_opcional.integra --outdir outputs
```

Esse exemplo consome a API pública:

```txt
https://dummyjson.com/carts
```

O comando da DSL responsável pelo consumo da API é:

```txt
buscar resposta de GET "https://dummyjson.com/carts"
```

Para visualizar o relatório:

```bash
python -m json.tool outputs/relatorio_api_publica.json
```

No Windows:

```powershell
python -m json.tool outputs\relatorio_api_publica.json
```

No relatório, procure por uma mensagem semelhante a:

```txt
Requisição GET concluída: https://dummyjson.com/carts
```

Isso demonstra que a API externa foi realmente utilizada.

---

## Visualização de resultados

### Visualizar logs da execução

No PowerShell:

```powershell
(Get-Content outputs\relatorio_sincronizacao_pedidos.json -Raw | ConvertFrom-Json).logs
```

Para o exemplo da API externa:

```powershell
(Get-Content outputs\relatorio_api_publica.json -Raw | ConvertFrom-Json).logs
```

### Visualizar contadores da execução

```powershell
(Get-Content outputs\relatorio_sincronizacao_pedidos.json -Raw | ConvertFrom-Json).contadores
```

Esse comando mostra contadores como:

* registros processados;
* registros salvos;
* envios com sucesso;
* falhas de validação;
* falhas de envio.

### Visualizar banco lógico

```powershell
(Get-Content outputs\relatorio_sincronizacao_pedidos.json -Raw | ConvertFrom-Json).banco_logico.pedidos_integrados
```

Esse comando mostra os registros salvos pela DSL na base lógica em memória.

### Visualizar envios simulados

```powershell
(Get-Content outputs\relatorio_sincronizacao_pedidos.json -Raw | ConvertFrom-Json).envios
```

Esse comando mostra os envios executados pelo comando da DSL:

```txt
enviar POST "mock://erp/pedidos" com pedido
```

Endpoints iniciados por `mock://` são simulados para permitir que o projeto rode sem depender de sistemas externos reais.

---

## Testes automatizados com Pytest

Execute:

```bash
pytest -q
```

Se houver problema de importação, use:

```bash
PYTHONPATH=src pytest -q
```

No Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
pytest -q
```

Saída esperada:

```txt
2 passed
```

Os testes automatizados verificam se o parser aceita o exemplo principal e se a árvore sintática é gerada corretamente.

---

## Testes de erro

Os testes abaixo são úteis para demonstrar que a linguagem detecta problemas de sintaxe, semântica e execução.

### 1. Erro sintático

Crie o arquivo:

```txt
examples/erro_sintatico.integra
```

Conteúdo:

```txt
fluxo "Erro Sintatico" {
    configurar ambiente = "teste"
    carregar resposta de arquivo "../data/pedidos.json"
    extrair pedidos = resposta.carts

    para cada pedido em pedidos {
        validar pedido.id obrigatorio
}
```

Execute:

```bash
integradsl examples/erro_sintatico.integra --tree --no-run
```

No Windows:

```powershell
integradsl examples\erro_sintatico.integra --tree --no-run
```

Esse teste deve gerar erro porque o bloco não foi fechado corretamente.

### 2. Erro semântico

Crie o arquivo:

```txt
examples/erro_semantico.integra
```

Conteúdo:

```txt
fluxo "Erro Semantico" {
    extrair pedidos = resposta.carts
    relatorio "erro_semantico.json"
}
```

Execute:

```bash
integradsl examples/erro_semantico.integra --tree --no-run
```

No Windows:

```powershell
integradsl examples\erro_semantico.integra --tree --no-run
```

Esse programa é sintaticamente válido, mas semanticamente inválido, pois usa a variável `resposta` antes de ela ser definida.

## Criando um novo programa IntegraDSL

Para criar um novo teste sem alterar o código-fonte do interpretador, basta criar um novo arquivo `.integra` na pasta `examples/`.

Exemplo:

```txt
examples/validar_produtos.integra
```

Conteúdo:

```txt
fluxo "Validar Produtos" {
    carregar resposta de arquivo "../data/produtos_teste.json"
    extrair produtos = resposta.produtos

    para cada produto em produtos {
        validar produto.id obrigatorio
        validar produto.nome obrigatorio
        validar produto.preco maior_que 0

        se erro {
            registrar "Produto inválido encontrado."
            salvar_erro produto.id
            continuar
        }

        definir produto.status = "valido"
        salvar produto em "produtos_validos"
        enviar POST "mock://estoque/produtos" com produto
    }

    relatorio "relatorio_produtos.json"
}
```

Para executar:

```bash
integradsl examples/validar_produtos.integra --tokens --tree --outdir outputs
```

No Windows:

```powershell
integradsl examples\validar_produtos.integra --tokens --tree --outdir outputs
```

---

## Observação importante sobre PowerShell e arquivos `.integra`

Arquivos `.integra` devem conter **somente código da IntegraDSL**.

Não coloque comandos do PowerShell dentro de arquivos `.integra`, como:

```powershell
$codigo = @'
Out-File -Encoding utf8 examples\arquivo.integra
Set-Content -Path "examples\arquivo.integra"
```

Esses comandos pertencem ao terminal PowerShell, não à linguagem IntegraDSL.

Um arquivo `.integra` válido deve começar com:

```txt
fluxo "Nome do fluxo" {
```

Se o parser mostrar um erro como:

```txt
Expected one of:
    * FLUXO
```

significa que o arquivo não começou com a palavra `fluxo` ou contém comandos que não pertencem à DSL.

---

## Execução alternativa sem o comando `integradsl`

Se o comando `integradsl` não for reconhecido, execute diretamente pelo módulo Python.

### Linux, macOS ou Codespaces

```bash
PYTHONPATH=src python -m integradsl examples/sincronizar_pedidos.integra --outdir outputs
```

### Windows PowerShell

```powershell
$env:PYTHONPATH="src"
python -m integradsl examples\sincronizar_pedidos.integra --outdir outputs
```

---

## Para demonstração completa

Para demonstrar o projeto de forma completa, execute os comandos nesta ordem:

### 1. Mostrar a ajuda da CLI

```bash
integradsl --help
```

### 2. Mostrar análise léxica

```bash
integradsl examples/sincronizar_pedidos.integra --tokens --no-run
```

### 3. Mostrar árvore sintática

```bash
integradsl examples/sincronizar_pedidos.integra --tree --no-run
```

### 4. Mostrar tradução didática para Python

```bash
integradsl examples/sincronizar_pedidos.integra --emit-python --no-run
```

### 5. Executar o programa principal

```bash
integradsl examples/sincronizar_pedidos.integra --outdir outputs
```

### 6. Executar exemplo com API externa

```bash
integradsl examples/api_real_opcional.integra --outdir outputs
```

### 7. Executar testes automatizados

```bash
pytest -q
```

Esse roteiro demonstra:

* analisador léxico;
* analisador sintático;
* geração de árvore sintática;
* análise semântica;
* interpretação;
* tradução orientada à sintaxe;
* execução offline;
* execução com API externa;
* testes automatizados.

---

## Relação com os requisitos da atividade

| Requisito                                         | Como o projeto atende                                                                |
| ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Linguagem para tarefa tediosa de estágio/trabalho | automatiza fluxos repetitivos de integração entre sistemas                           |
| Linguagem interpretada ou compilada               | a IntegraDSL é interpretada                                                          |
| Analisador léxico definido formalmente            | implementado com Lark em `grammar.lark`                                              |
| Analisador sintático definido formalmente         | implementado com Lark em `grammar.lark`                                              |
| Uso da ferramenta Lark                            | usado em `parser.py`                                                                 |
| Geração de árvore sintática                       | opção `--tree` da CLI                                                                |
| Tradutor/interpretador orientado à sintaxe        | `interpreter.py` e `translator.py`                                                   |
| Estrutura típica de compilador                    | lexer, parser, AST, semântica, interpretação                                         |
| Execução no GitHub Codespaces                     | suportada via instalação Python e `.devcontainer/`                                   |
| README com equipe, motivação, execução e exemplos | documentado neste arquivo                                                            |
| Estruturas novas além da aula                     | comandos de domínio: `buscar`, `validar`, `salvar`, `enviar`, `se erro`, `relatorio` |

---

## Considerações finais

A IntegraDSL demonstra como uma linguagem de domínio específico pode simplificar uma tarefa real do mercado: a automação de integrações entre sistemas.

O projeto não se limita a uma linguagem simples com comandos básicos. Ele contém estruturas próprias do domínio de integração, como consumo de API, validação de dados, tratamento de erro, transformação de registros, simulação de envio e geração de relatório.

Dessa forma, o projeto atende aos requisitos da atividade e apresenta uma implementação sistemática baseada em técnicas de compiladores e interpretadores.
