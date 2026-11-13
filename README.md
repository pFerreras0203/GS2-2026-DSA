# Citizen Assist AI — Documentação e Cidadania

**GS2 2026 | Data Structures and Algorithms | Turma 1CCPI** | **Linguagem:** Python

**Equipe:** Gustavo Kunitaki - RM: 571400 / Pedro Ferreras - RM:568713 / Pedro Santos - RM: 571017

---

## 1. Visão geral

O **Citizen Assist AI** é um protótipo em terminal que ajuda o cidadão a consultar informações sobre serviços de **documentação e cidadania** (RG, CPF, Carteira de Trabalho, benefícios do INSS etc.): o que é o serviço, quais documentos são exigidos, onde solicitar, quanto tempo leva e quanto custa.

O foco do trabalho é a aplicação prática de estruturas de dados e algoritmos **implementados pela equipe**: lista encadeada, busca sequencial e Merge Sort. Nenhuma função pronta de ordenação (`sort`, `sorted`) ou estrutura pronta é usada para cumprir os requisitos.

## 2. Como executar

- Ao iniciar, a lista está **vazia**. Use a opção **9** para carregar 4 serviços de exemplo (com IDs fora de ordem, para demonstrar o Merge Sort) ou a opção **1** para cadastrar manualmente.

## 3. Arquitetura do código

| Elemento         | Papel                                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `Servico`        | Registro com os dados de um serviço                                                                                        |
| `No`             | Nó da lista encadeada (`dado` + `proximo`)                                                                                 |
| `ListaEncadeada` | Lista encadeada simples com inserção, percurso, busca, remoção, ordenação e contagem por categoria                         |
| Funções do menu  | `cadastrar`, `consultar_por_id`, `pesquisar`, `atualizar`, `excluir`, `listar`, `ordenar`, `analisar`, `carregar_exemplos` |
| `main`           | Loop do menu interativo (dicionário que mapeia opção → função)                                                             |

### 3.1 Modelo dos registros (`Servico`)

| Campo        | Tipo               | Descrição                     | Exemplo                                              |
| ------------ | ------------------ | ----------------------------- | ---------------------------------------------------- |
| `id`         | `int` (> 0, único) | Identificador do serviço      | `10`                                                 |
| `titulo`     | `str`              | Nome do serviço               | `Segunda via de RG`                                  |
| `categoria`  | `str`              | Agrupamento do serviço        | `Identidade`                                         |
| `descricao`  | `str`              | O que é o serviço             | `Emissão de nova identidade.`                        |
| `requisitos` | `str`              | Documentos/condições exigidas | `Certidão de nascimento e comprovante de residência` |
| `local`      | `str`              | Onde solicitar                | `Poupatempo`                                         |
| `prazo`      | `str`              | Tempo para ficar pronto       | `10 dias úteis`                                      |
| `custo`      | `str`              | Valor cobrado                 | `Gratuito`                                           |

Todos os campos de texto são obrigatórios (não aceitam valor vazio no cadastro).

### 3.2 Lista encadeada

Lista **simples**, com referências explícitas (sem usar `list` do Python para armazenar os registros):

```
cabeca                                          cauda
  │                                               │
  ▼                                               ▼
┌──────────┬───┐   ┌──────────┬───┐   ┌──────────┬──────┐
│ Servico  │ ●─┼──▶│ Servico  │ ●─┼──▶│ Servico  │ None │
└──────────┴───┘   └──────────┴───┘   └──────────┴──────┘
```

Atributos: `cabeca` (primeiro nó), `cauda` (último nó) e `tamanho` (quantidade de nós).

| Operação               | Como funciona                                                                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `inserir_fim`          | Cria o nó; se a lista está vazia, ele vira cabeça e cauda; senão, `cauda.proximo` aponta para ele e ele vira a nova cauda             |
| `percorrer`            | Gerador que parte da cabeça e segue `proximo` até `None`                                                                              |
| `buscar_por_id`        | Busca sequencial comparando o `id`                                                                                                    |
| `pesquisar`            | Busca sequencial por título ou categoria (texto contido no campo, sem diferenciar maiúsculas/minúsculas); retorna todos os resultados |
| `remover`              | Usa os ponteiros `anterior` e `atual`; trata remoção da cabeça, do meio e da cauda, atualizando `cabeca`, `cauda` e `tamanho`         |
| `ordenar_por_id`       | Merge Sort que reordena a lista religando os nós                                                                                      |
| `contar_por_categoria` | Um percurso que acumula a contagem em um dicionário                                                                                   |

A **integridade da lista** é mantida porque toda inserção/remoção atualiza `cabeca`, `cauda` e `tamanho`, e o nó removido tem o `proximo` zerado.

### 3.3 Menu interativo

| Opção | Função                                                               |
| ----- | -------------------------------------------------------------------- |
| 1     | Cadastrar serviço                                                    |
| 2     | Consultar por ID                                                     |
| 3     | Pesquisar por título ou categoria                                    |
| 4     | Atualizar serviço (ENTER mantém o valor atual; o ID não é alterável) |
| 5     | Excluir serviço                                                      |
| 6     | Listar todos                                                         |
| 7     | Ordenar por ID (Merge Sort) e exibir                                 |
| 8     | Análise: total de serviços e quantidade por categoria                |
| 9     | Carregar dados de exemplo                                            |
| 0     | Sair                                                                 |

**Tratamentos implementados:** opção de menu inválida, ID duplicado, ID não numérico/zero/negativo, campo de texto vazio, lista vazia (em todas as operações), consulta/pesquisa/exclusão sem resultado, campo de pesquisa inválido (`ValueError`) e interrupção pelo teclado (Ctrl+C ou fim de entrada), que encerra o programa com mensagem em vez de mostrar erro.

## 4. Algoritmos implementados

### 4.1 Busca sequencial (linear)

Percorre a lista do primeiro ao último nó, comparando cada registro com o critério. É a única busca possível na lista encadeada simples, pois ela **não oferece acesso direto por índice** (inviabiliza a busca binária).

- **Por ID:** para no primeiro nó encontrado (os IDs são únicos). Se chega em `None`, informa que não há resultado.
- **Por título/categoria:** não para no primeiro, pois vários registros podem corresponder; acumula todos em uma lista de resultados. Se a lista ficar vazia, informa que nada foi encontrado.

### 4.2 Merge Sort (ordenação por ID)

Algoritmo de **dividir para conquistar**, adaptado à lista encadeada:

1. **Dividir:** `_dividir` localiza o nó do meio com dois ponteiros (`lento` avança 1 nó, `rapido` avança 2). A lista é cortada em duas metades (`meio.proximo = None`).
2. **Conquistar:** cada metade é ordenada recursivamente. O caso base é a lista com 0 ou 1 nó.
3. **Combinar:** `_mesclar` intercala as duas metades já ordenadas, sempre ligando o nó de menor ID, usando um **nó sentinela** para evitar tratar o primeiro nó como caso especial.

Características: **não copia dados**, apenas religa ponteiros; é **estável** (usa `<=`, então IDs iguais mantêm a ordem relativa); e não depende de acesso por índice, o que o torna a escolha natural para listas encadeadas. Ao final, a `cauda` é recalculada.

**Exemplo** (IDs na ordem de inserção dos dados de exemplo: `32 → 59 → 30 → 4`):

```
[32, 59, 30, 4]
   ├── [32, 59]  →  [32] [59]  →  mescla → [32, 59]
   └── [30, 4]  →  [30] [4]  →  mescla → [4, 30]
mescla final → [4, 30, 32, 59]
```

## 5. Análise de complexidade (Big-O)

Considere **n** = número de registros na lista e **m** = tamanho (em caracteres) do texto comparado. A análise reflete a implementação efetiva.

### 5.1 Resumo

| Operação                                    | Melhor caso | Caso médio | Pior caso  | Espaço extra |
| ------------------------------------------- | ----------- | ---------- | ---------- | ------------ |
| Inserção no fim (`inserir_fim`)             | O(1)        | O(1)       | O(1)       | O(1)         |
| Busca por ID (`buscar_por_id`)              | O(1)        | O(n)       | O(n)       | O(1)         |
| Pesquisa por título/categoria (`pesquisar`) | O(n·m)      | O(n·m)     | O(n·m)     | O(k)\*       |
| Remoção por ID (`remover`)                  | O(1)        | O(n)       | O(n)       | O(1)         |
| Ordenação (`ordenar_por_id` — Merge Sort)   | O(n log n)  | O(n log n) | O(n log n) | O(log n)     |
| Atualização (busca + alteração de campos)   | O(1)        | O(n)       | O(n)       | O(1)         |
| Percurso / listagem                         | O(n)        | O(n)       | O(n)       | O(1)         |
| Contagem por categoria                      | O(n)        | O(n)       | O(n)       | O(c)\*\*     |

\* k = quantidade de resultados encontrados. \*\* c = quantidade de categorias distintas.

### 5.2 Justificativas

**Inserção — O(1).** Como a lista guarda a referência à `cauda`, inserir no fim exige apenas criar o nó e ajustar dois ponteiros, independentemente de n. _Observação:_ a operação de **cadastro** completa do menu é **O(n)**, pois antes de inserir o programa verifica duplicidade de ID com `buscar_por_id`. A inserção em si continua O(1).

**Busca por ID — O(n).** Busca sequencial. No melhor caso o registro está na cabeça (1 comparação, O(1)); no pior caso está na cauda ou não existe (n comparações). No caso médio, para um registro existente, são cerca de n/2 comparações, o que é O(n).

**Pesquisa por título/categoria — O(n·m).** Sempre percorre os n nós (precisa achar todas as correspondências, então não há parada antecipada) e, em cada um, a operação `termo in valor` compara strings de tamanho m. Como m é pequeno e limitado (títulos e categorias curtos), na prática o custo se comporta como O(n).

**Remoção — O(n).** O custo está em **localizar** o nó (percurso com `anterior` e `atual`). Religar os ponteiros depois de encontrado é O(1). No melhor caso (remover a cabeça) o custo total é O(1).

**Ordenação (Merge Sort) — O(n log n).** A recorrência é T(n) = 2·T(n/2) + O(n): cada nível de recursão divide a lista (`_dividir`, percurso até o meio) e mescla (`_mesclar`), gastando O(n) por nível no total, e há log₂(n) níveis. O custo é o mesmo nos três casos, porque o algoritmo sempre divide e mescla independentemente da ordem inicial. O espaço extra é O(log n), referente à pilha de chamadas recursivas: como a mesclagem religa os nós existentes, não há cópia dos dados.

**Atualização — O(n).** Dominada pela busca do registro por ID; a alteração dos campos é O(1).

**Indicadores — O(n).** Um único percurso, acumulando contagens em um dicionário (inserção/consulta em média O(1)).
