import heapq
from sprintUmContent.basic_functions import *
from sprintUmContent.data_frame_functions import *
import matplotlib.pyplot as plt
def heap_labs_criticos(laboratorios: dict, df_media):
    """
    Cria uma min-heap com laboratórios baseando-se no índice de criticidade,
    que é a soma dos insumos críticos proporcional ao total de insumos.

    Retorna uma lista ordenada do mais crítico para o menos crítico, para facilitar a visualização.
    """

    heap = []

    for lab in laboratorios:
        # soma dos insumos críticos neste laboratório
        soma_criticos = 0
        for insumo in laboratorios[lab]["insumos"]:
            if estado_critico(laboratorios, lab, insumo, df_media):
                soma_criticos += laboratorios[lab]["insumos"][insumo]

        if soma_criticos > 0:
            total_insumos = contar_insumos_total(laboratorios, lab)
            if total_insumos > 0:
                indice_criticidade = soma_criticos / total_insumos
                # heapq é uma min heap, então insira (índice, lab)
                heapq.heappush(heap, (indice_criticidade, lab))

    # Para visualização, desempilha para uma lista ordenada (mais crítico primeiro)
    ordenados = []
    while heap:
        crit, lab = heapq.heappop(heap)
        ordenados.append((lab, crit))

    # invertendo para mostrar do maior índice para o menor
    ordenados.reverse()

    # Exibir resultado formatado (opcional)
    print("Laboratórios ordenados por criticidade (mais crítico primeiro):")
    for lab, crit in ordenados:
        print(f"{lab}: {crit:.3f}")

    return ordenados


def visualizar_heap_criticos(ordenados):
    """
    Recebe uma lista ordenada (lab, indice_criticidade) do mais crítico para o menos crítico
    e gera um gráfico de barras horizontal para visualização.
    """

    if not ordenados:
        print("Nenhum laboratório em estado crítico para visualizar.")
        return

    labs = [lab for lab, _ in ordenados]
    indices = [crit for _, crit in ordenados]

    plt.figure(figsize=(10, 6))
    plt.barh(labs, indices, color='tomato')
    plt.xlabel("Índice de Criticidade")
    plt.title("Laboratórios em Estado Crítico (Maior para Menor)")
    plt.gca().invert_yaxis()  # inverte eixo Y para o mais crítico ficar em cima
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
