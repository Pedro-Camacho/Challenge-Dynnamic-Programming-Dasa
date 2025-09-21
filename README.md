# Integrantes do Grupo
* Camila Pedroza da Cunha RM 558768
* Isabelle Dallabeneta Carlesso RM 554592
* Nicoli Amy Kassa RM 559104
* Pedro Almeida e Camacho RM 556831
* Renan Dias Utida RM 558540
  
# 🏥 Sistema de Gerenciamento de Insumos Hospitalares

Este projeto implementa um **sistema de gerenciamento e simulação de
insumos hospitalares** utilizando **estruturas de dados clássicas (Fila,
Pilha, Ordenação, Busca)** aplicadas ao contexto médico.

Ele permite: - Registrar consumos de insumos em **ordem cronológica**\
- Consultar os **últimos consumos realizados**\
- Buscar insumos no catálogo ou nos registros (por código, nome ou
criticidade)\
- Ordenar insumos por critérios de estoque, validade ou criticidade\
- Gerar relatórios detalhados sobre uso, estoque e vencimentos

------------------------------------------------------------------------

## 📂 Estrutura do Projeto

-   `InsumoHospitalar.py` → Modelo de insumo (nome, código, validade,
    lote, criticidade etc.)
-   `Criticidade.py` → Enum com níveis de criticidade (Crítica, Alta,
    Média, Baixa)
-   `Setor.py` → Enum com setores hospitalares (UTI, Emergência,
    Cirurgia etc.)
-   `ConsumoAggregado.py` → Classe auxiliar para ranking de insumos mais
    consumidos
-   `FilaConsumoHospitalar.py` → Estrutura **Fila (FIFO)** para
    registrar consumos em ordem cronológica
-   `PilhaConsultasHospitalar.py` → Estrutura **Pilha (LIFO)** para
    consultar últimos consumos
-   `BuscaInsumosHospitalares.py` → Algoritmos de busca (sequencial e
    binária) para catálogo de insumos
-   `OrdenacaoInsumosHospitalares.py` → Algoritmos de ordenação (Merge
    Sort e Quick Sort)
-   `SistemaConsumoHospitalar.py` → Orquestra todas as estruturas e gera
    relatórios/demonstrações
-   `principal.py` → Ponto de entrada principal (`main()`)
-   `sprint-3.ipynb` → Notebook de testes e validações

------------------------------------------------------------------------

## ⚙️ Estruturas de Dados Utilizadas

### 🔄 Fila (`FilaConsumoHospitalar`)

-   **Tipo:** FIFO (First In, First Out)\
-   **Uso no sistema:**
    -   Registra eventos de consumo em ordem cronológica.\
    -   Garante rastreabilidade e auditoria hospitalar.\
    -   Usado para relatórios e para simular o processamento dos insumos
        na ordem correta.

``` python
fila = FilaConsumoHospitalar()
fila.enqueue((data, insumo, qtd, responsavel))
consumo = fila.dequeue()
```

------------------------------------------------------------------------

### 📚 Pilha (`PilhaConsultasHospitalar`)

-   **Tipo:** LIFO (Last In, First Out)\
-   **Uso no sistema:**
    -   Permite verificar os últimos consumos rapidamente.\
    -   Ajuda em auditorias reversas e emergências.\
    -   Exemplo: saber os últimos insumos utilizados em um plantão.

``` python
pilha = PilhaConsultasHospitalar()
pilha.push((data, insumo, qtd, responsavel))
ultimo = pilha.pop()
```

------------------------------------------------------------------------

### 🔍 Buscas (`BuscaInsumosHospitalares`)

-   **Busca Sequencial por Código (O(n)):**\
    Localiza insumos pelo identificador único.\
-   **Busca Sequencial por Criticidade (O(n)):**\
    Filtra insumos de nível Crítico, Alto, Médio ou Baixo.\
-   **Busca Binária por Nome (O(log n)):**\
    Requer catálogo ordenado; eficiente para estoques grandes.

``` python
indice = BuscaInsumosHospitalares.busca_sequencial_por_codigo(insumos, "SER001")
indices = BuscaInsumosHospitalares.busca_sequencial_por_criticidade(insumos, Criticidade.CRITICA)
pos = BuscaInsumosHospitalares.busca_binaria_por_nome(insumos_ordenados, "Luva Nitrilo")
```

------------------------------------------------------------------------

### 🔧 Ordenação (`OrdenacaoInsumosHospitalares`)

-   **Merge Sort (O(n log n), estável):**
    -   Ordena insumos por quantidade, validade ou criticidade.\
    -   Usado para relatórios confiáveis e rankings.\
-   **Quick Sort (O(n log n) médio):**
    -   Mais rápido em grandes volumes.\
    -   Ideal para ordenar por validade (FEFO).

``` python
ordenados_qtd = OrdenacaoInsumosHospitalares.merge_sort(insumos, chave="quantidade")
ordenados_val = OrdenacaoInsumosHospitalares.quick_sort(insumos, chave="validade")
```

------------------------------------------------------------------------

### 📊 Agregação (`ConsumoAggregado`)

-   Estrutura auxiliar para consolidar o **total consumido por
    insumo**.\
-   Usado para gerar **ranking dos mais consumidos**.

``` python
ranking = sistema.ranking_mais_consumidos_merge()
for item in ranking:
    print(item.insumo.nome, item.total_consumido)
```

------------------------------------------------------------------------

## 🖥️ Sistema Principal

A classe `SistemaConsumoHospitalar` integra todas as estruturas:

``` python
from sprintTresContent.SistemaConsumoHospitalar import SistemaConsumoHospitalar

sistema = SistemaConsumoHospitalar()
sistema.gerar_dados_hospitalares_simulados(20)

sistema.demonstrar_fila_hospitalar()
sistema.demonstrar_pilha_hospitalar()
sistema.demonstrar_buscas_hospitalares()
sistema.demonstrar_ordenacao_hospitalar()
sistema.gerar_relatorio_hospitalar()
sistema.imprimir_justificativas()
```

### 📈 Relatórios

-   Distribuição de insumos por criticidade\
-   Análise de estoque\
-   Controle de vencimentos (FEFO)\
-   Distribuição por setor\
-   Ranking de insumos mais consumidos

------------------------------------------------------------------------

## 🚀 Execução

1.  Clone o projeto ou copie os arquivos.\

2.  Certifique-se de ter **Python 3.10+** instalado.\

3.  Instale dependências (caso use notebook):

    ``` bash
    pip install pandas
    ```

4.  Rode o sistema:

    ``` bash
    python sprint-3.py
    ```

5.  Explore os relatórios e saídas no console.

------------------------------------------------------------------------

## 💡 Justificativa no Contexto Hospitalar

-   **Fila (FIFO):** garante rastreabilidade e controle cronológico.\
-   **Pilha (LIFO):** permite resposta rápida sobre últimos consumos.\
-   **Buscas:** localizam insumos críticos em emergências.\
-   **Ordenação:** organiza estoque por validade (FEFO) e quantidade.\
-   **Relatórios:** fornecem visão gerencial e suporte à tomada de
    decisão.
