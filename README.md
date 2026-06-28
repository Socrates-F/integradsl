# IntegraDSL

**IntegraDSL** é uma linguagem de domínio específico, implementada com **Python** e **Lark**, criada para automatizar fluxos repetitivos de integração entre sistemas.

A linguagem permite descrever tarefas comuns de estágio/trabalho em computação, como:

- carregar dados de arquivos JSON;
- consumir APIs;
- validar campos obrigatórios;
- aplicar regras de negócio;
- transformar registros;
- salvar dados em uma base lógica;
- enviar dados para outro sistema;
- tratar erros;
- gerar relatório final de execução.

O projeto foi estruturado seguindo a organização típica de um compilador/interpretador: gramática formal, análise léxica, análise sintática, geração de árvore sintática, construção de AST, análise semântica, tradução orientada à sintaxe e interpretação.

---

## Equipe

- Carlos Clistenes Bezerra Lira
- Integrante 2: preencher, se houver
- Integrante 3: preencher, se houver

---

## Motivação

Em estágios e ambientes reais de desenvolvimento, é comum encontrar tarefas repetitivas envolvendo integração entre sistemas. Por exemplo:

> Buscar pedidos em uma API, validar se os campos estão corretos, transformar os dados, enviar para um ERP, registrar erros e gerar um relatório final.

Normalmente, esse tipo de automação exige escrever scripts Python repetitivos, com muito código de requisição HTTP, validação, laços, tratamento de erro e geração de logs.

A proposta da **IntegraDSL** é permitir que esse fluxo seja descrito de forma mais próxima da linguagem do problema, reduzindo a repetição e tornando a intenção do processo mais clara.

---

## Descrição informal da linguagem

A IntegraDSL descreve um **fluxo de integração**. Um fluxo é formado por comandos, como:

- `configurar`: cria uma variável de configuração;
- `carregar`: carrega dados de um arquivo JSON local;
- `buscar`: executa uma requisição HTTP;
- `extrair`: extrai um campo de uma estrutura JSON;
- `para cada`: percorre uma lista de registros;
- `validar`: aplica uma regra de validação;
- `se/senao`: executa comandos condicionalmente;
- `definir`: cria ou altera um campo de um registro;
- `salvar`: armazena o registro em uma base lógica em memória;
- `enviar`: envia um registro para uma API ou endpoint mock;
- `se erro`: verifica se o último comando gerou erro;
- `salvar_erro`: registra uma falha associada a um identificador;
- `continuar`: pula para a próxima iteração de um laço;
- `relatorio`: gera um relatório JSON da execução.

A linguagem é **interpretada**, mas também possui um tradutor didático que gera uma representação equivalente em Python.

---

## Exemplo de programa IntegraDSL

Arquivo: `examples/sincronizar_pedidos.integra`

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

Esse programa faz o seguinte:

1. Carrega pedidos de um arquivo JSON;
2. Extrai a lista `resposta.carts` para a variável `pedidos`;
3. Percorre cada pedido;
4. Valida se o pedido possui `id` e `total > 0`;
5. Se houver erro, registra a falha e pula para o próximo pedido;
6. Define a prioridade como `alta` ou `normal`;
7. Salva o pedido em uma base lógica;
8. Envia o pedido para um endpoint mock;
9. Gera um relatório JSON final.

---

## Como executar no GitHub Codespaces

O projeto foi preparado para rodar em ambiente Python. No Codespaces, basta abrir o terminal e executar:

```bash
pip install -r requirements.txt
pip install -e .
```

Depois, execute o exemplo principal:

```bash
integradsl examples/sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs
```

Também é possível executar sem instalar o pacote em modo editável:

```bash
PYTHONPATH=src python -m integradsl examples/sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs
```

No Windows PowerShell, use:

```powershell
$env:PYTHONPATH="src"
python -m integradsl examples/sincronizar_pedidos.integra --tokens --tree --emit-python --outdir outputs
```

---

## Comandos úteis

Executar o programa normalmente:

```bash
integradsl examples/sincronizar_pedidos.integra --outdir outputs
```

Mostrar apenas a árvore sintática:

```bash
integradsl examples/sincronizar_pedidos.integra --tree --no-run
```

Mostrar os tokens reconhecidos pelo analisador léxico:

```bash
integradsl examples/sincronizar_pedidos.integra --tokens --no-run
```

Gerar uma tradução didática para Python:

```bash
integradsl examples/sincronizar_pedidos.integra --emit-python --no-run
```

Executar os testes automatizados:

```bash
PYTHONPATH=src pytest -q
```

---

## Saída esperada do exemplo principal

Ao executar:

```bash
integradsl examples/sincronizar_pedidos.integra --outdir outputs
```

A saída esperada no terminal é semelhante a:

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

Esse relatório contém logs, erros, dados salvos na base lógica e envios realizados.

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
│   ├── sincronizar_pedidos.integra
│   ├── validar_usuarios.integra
│   └── api_real_opcional.integra
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

## Estrutura típica de compilador usada no projeto

O projeto foi organizado em etapas sistemáticas:

| Etapa | Arquivo | Função |
|---|---|---|
| Definição formal da linguagem | `grammar.lark` | Define tokens e regras sintáticas |
| Análise léxica | `parser.py` + Lark | Reconhece tokens como `fluxo`, `validar`, `se`, `POST`, `STRING`, `NUMBER` |
| Análise sintática | `parser.py` + Lark | Gera a árvore sintática concreta |
| Construção da AST | `parser.py` + `ast_nodes.py` | Converte a árvore do Lark em nós semânticos próprios |
| Análise semântica | `semantic.py` | Verifica variáveis usadas antes da definição e uso correto de `continuar` |
| Interpretação | `interpreter.py` | Executa o fluxo descrito pela DSL |
| Tradução | `translator.py` | Gera uma versão didática em Python |
| Interface de execução | `cli.py` | Permite rodar, mostrar tokens, árvore e tradução |

---

## Definição léxica

A linguagem reconhece os seguintes grupos léxicos:

| Token | Exemplo | Descrição |
|---|---|---|
| Palavra-chave | `fluxo`, `validar`, `se`, `senao` | Comandos da linguagem |
| Identificador | `pedido`, `resposta`, `total` | Nome de variável ou campo |
| String | `"pedidos.json"` | Texto entre aspas |
| Número | `1000`, `12.5` | Valores numéricos inteiros ou reais |
| Método HTTP | `GET`, `POST`, `PUT`, `DELETE` | Métodos usados em integrações |
| Operador | `>`, `<`, `>=`, `<=`, `==`, `!=` | Operadores de comparação |
| Comentário | `# comentário` | Ignorado pelo analisador |

Exemplo de tokens para um trecho da linguagem:

```txt
validar pedido.total maior_que 0
```

Tokens reconhecidos:

```txt
VALIDAR         validar
NAME            pedido
DOT             .
NAME            total
MAIOR_QUE       maior_que
SIGNED_NUMBER   0
```

---

## Gramática formal resumida

A gramática completa está em `src/integradsl/grammar.lark`.

Resumo das principais regras:

```txt
start: fluxo

fluxo: "fluxo" STRING bloco

bloco: "{" comando* "}"

comando: configurar
       | carregar_arquivo
       | buscar
       | extrair
       | repeticao
       | condicional
       | validar
       | definir
       | salvar
       | enviar
       | registrar
       | salvar_erro
       | relatorio
       | continuar

configurar: "configurar" NAME "=" valor
carregar_arquivo: "carregar" NAME "de" "arquivo" STRING
buscar: "buscar" NAME "de" METODO STRING
extrair: "extrair" NAME "=" caminho

repeticao: "para" "cada" NAME "em" caminho bloco
condicional: "se" condicao bloco ("senao" bloco)?

validar: "validar" caminho regra
definir: "definir" caminho "=" valor
salvar: "salvar" caminho "em" STRING
enviar: "enviar" METODO STRING "com" caminho
registrar: "registrar" STRING
salvar_erro: "salvar_erro" caminho
relatorio: "relatorio" STRING
continuar: "continuar"
```

---

## Semântica da linguagem

A semântica define o significado de cada comando:

| Comando | Semântica |
|---|---|
| `fluxo` | Define o início de um programa IntegraDSL |
| `configurar` | Armazena uma variável simples no ambiente |
| `carregar` | Lê um arquivo JSON local e salva seu conteúdo em uma variável |
| `buscar` | Executa uma requisição HTTP ou uma requisição mock |
| `extrair` | Copia um campo de uma estrutura para uma nova variável |
| `para cada` | Percorre uma lista de objetos |
| `validar` | Aplica uma regra de validação e marca erro se falhar |
| `se erro` | Executa o bloco se o último comando relevante produziu erro |
| `se/senao` | Executa comandos de acordo com uma comparação |
| `definir` | Cria ou altera um campo em um objeto |
| `salvar` | Armazena o objeto em uma base lógica em memória |
| `enviar` | Envia o objeto para um endpoint HTTP ou `mock://` |
| `registrar` | Adiciona uma mensagem aos logs |
| `salvar_erro` | Registra uma falha associada a uma referência |
| `continuar` | Pula para a próxima iteração do laço |
| `relatorio` | Gera um arquivo JSON com o resultado da execução |

---

## Exemplos de estruturas novas além das linguagens básicas vistas em aula

A IntegraDSL inclui estruturas voltadas ao domínio de integração de sistemas:

1. **Comando de integração HTTP**

```txt
buscar resposta de GET "https://dummyjson.com/carts"
enviar POST "mock://erp/pedidos" com pedido
```

2. **Validações declarativas de dados**

```txt
validar pedido.id obrigatorio
validar pedido.total maior_que 0
validar usuario.email formato_email
```

3. **Tratamento de erro orientado ao fluxo**

```txt
se erro {
    registrar "Registro inválido."
    salvar_erro pedido.id
    continuar
}
```

4. **Manipulação de caminhos em objetos JSON**

```txt
extrair pedidos = resposta.carts
definir pedido.prioridade = "alta"
```

5. **Geração automática de relatório operacional**

```txt
relatorio "relatorio_sincronizacao_pedidos.json"
```

Essas estruturas tornam a linguagem mais específica e criativa do que uma linguagem apenas aritmética ou de comandos básicos.

---

## Árvore sintática

Executando:

```bash
integradsl examples/sincronizar_pedidos.integra --tree --no-run
```

Um trecho da árvore gerada pelo Lark será semelhante a:

```txt
start
  fluxo
    "Sincronizar pedidos locais"
    bloco
      configurar
        ambiente
        string "homologacao"
      carregar_arquivo
        resposta
        "../data/pedidos.json"
      extrair
        pedidos
        caminho
          resposta
          carts
      repeticao
        pedido
        caminho pedidos
        bloco
          validar
            caminho
              pedido
              id
            regra_obrigatorio
```

Isso demonstra a geração da árvore sintática exigida no projeto.

---

## Tradução orientada à sintaxe

Além do interpretador, o projeto possui um tradutor didático para Python.

Execute:

```bash
integradsl examples/sincronizar_pedidos.integra --emit-python --no-run
```

Trecho da tradução:

```python
state['env']['resposta'] = carregar_json('../data/pedidos.json')
state['env']['pedidos'] = get_path('resposta.carts')
for pedido in get_path('pedidos'):
    state['env']['pedido'] = pedido
    state['last_error'] = False
    validar('pedido.id', regra='obrigatorio', argumento=None)
    validar('pedido.total', regra='maior_que', argumento=0)
```

A tradução é didática: ela mostra a semântica do programa, mas a execução oficial é feita pelo interpretador em `interpreter.py`.

---

## Exemplos disponíveis

### 1. `sincronizar_pedidos.integra`

Exemplo principal, totalmente offline. Usa `data/pedidos.json` e endpoints `mock://`.

```bash
integradsl examples/sincronizar_pedidos.integra --outdir outputs
```

### 2. `validar_usuarios.integra`

Exemplo de validação de dados cadastrais com e-mail e idade mínima.

```bash
integradsl examples/validar_usuarios.integra --outdir outputs
```

### 3. `api_real_opcional.integra`

Exemplo opcional com API pública. Depende de internet no ambiente de execução.

```bash
integradsl examples/api_real_opcional.integra --outdir outputs
```

---

## Por que a linguagem resolve um problema bem definido?

O problema resolvido é a automação de fluxos repetitivos de integração operacional. Esse tipo de tarefa aparece em diversos contextos reais:

- integração entre marketplace e ERP;
- sincronização de pedidos;
- validação de cadastros;
- envio de dados para CRM;
- conferência de dados antes de importação;
- geração de logs e relatórios de falhas.

A IntegraDSL permite expressar esse processo de forma direta, usando comandos próprios do domínio, em vez de exigir que o usuário escreva todo o script Python manualmente.

---

## Relação com os critérios de avaliação

### a) Eu consegui rodar o programa a partir das instruções do README?

Sim. O README contém comandos para instalar dependências e executar exemplos.

### b) A linguagem foi implementada utilizando a estrutura típica de um compilador?

Sim. O projeto possui gramática formal, análise léxica, análise sintática, AST, análise semântica, interpretador e tradutor.

### c) A linguagem foi bem definida na documentação?

Sim. A documentação apresenta motivação, comandos, léxico, gramática resumida, semântica e exemplos.

### d) A linguagem resolve de maneira criativa um problema bem definido?

Sim. A linguagem resolve o problema de automação de integrações entre sistemas, com validação, transformação, erro e relatório.

### e) A linguagem contém estruturas novas além das linguagens mostradas na aula?

Sim. A linguagem contém comandos específicos de integração, validação declarativa, tratamento de erro operacional, endpoints `mock://`, manipulação de JSON e geração de relatório.

---

## Observações finais

A IntegraDSL foi pensada para ser pequena o suficiente para ser implementada em um projeto acadêmico, mas complexa o suficiente para representar um problema real do mercado de computação.

Ela pode ser expandida futuramente com:

- conexão real com PostgreSQL;
- autenticação por token;
- integração com filas como RabbitMQ;
- exportação para workflows do n8n;
- suporte a arquivos CSV;
- operadores lógicos `e` e `ou`;
- funções reutilizáveis.
