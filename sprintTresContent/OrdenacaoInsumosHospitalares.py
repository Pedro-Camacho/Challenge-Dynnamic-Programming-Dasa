from typing import List
from sprintTresContent.InsumoHospitalar import InsumoHospitalar
from datetime import datetime, timedelta

class OrdenacaoInsumosHospitalares:
    """Implementação de algoritmos de ordenação para gestão hospitalar"""

    @staticmethod
    def merge_sort(lista: List[InsumoHospitalar], chave='quantidade') -> List[InsumoHospitalar]:
        """
        Merge Sort - O(n log n) estável
        Ideal para ordenar insumos por quantidade (controle de estoque)
        ou por validade (gestão de vencimentos)
        """
        if len(lista) <= 1:
            return lista.copy()

        meio = len(lista) // 2
        esquerda = OrdenacaoInsumosHospitalares.merge_sort(lista[:meio], chave)
        direita = OrdenacaoInsumosHospitalares.merge_sort(lista[meio:], chave)

        return OrdenacaoInsumosHospitalares._merge(esquerda, direita, chave)

    @staticmethod
    def _merge(esquerda: List[InsumoHospitalar], direita: List[InsumoHospitalar],
               chave: str) -> List[InsumoHospitalar]:
        """Função auxiliar do merge sort"""
        resultado = []
        i = j = 0

        while i < len(esquerda) and j < len(direita):
            if chave == 'criticidade':
                # Ordenação especial para criticidade (Crítica > Alta > Média > Baixa)
                ordem_crit = {'Crítica': 4, 'Alta': 3, 'Média': 2, 'Baixa': 1}
                valor_esq = ordem_crit[esquerda[i].criticidade.value]
                valor_dir = ordem_crit[direita[j].criticidade.value]
                # Ordem decrescente para criticidade
                comparacao = valor_esq >= valor_dir
            else:
                valor_esq = getattr(esquerda[i], chave)
                valor_dir = getattr(direita[j], chave)
                comparacao = valor_esq <= valor_dir

            if comparacao:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1

        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        return resultado

    @staticmethod
    def quick_sort(lista: List[InsumoHospitalar], chave='validade') -> List[InsumoHospitalar]:
        """
        Quick Sort - O(n log n) médio
        Eficiente para ordenar por validade (identificar vencimentos próximos)
        """
        lista_copia = lista.copy()
        OrdenacaoInsumosHospitalares._quick_sort_recursivo(lista_copia, 0, len(lista_copia) - 1, chave)
        return lista_copia

    @staticmethod
    def _quick_sort_recursivo(lista: List[InsumoHospitalar], inicio: int, fim: int, chave: str):
        """Implementação recursiva do quick sort"""
        if inicio < fim:
            pivot_index = OrdenacaoInsumosHospitalares._particionar(lista, inicio, fim, chave)
            OrdenacaoInsumosHospitalares._quick_sort_recursivo(lista, inicio, pivot_index - 1, chave)
            OrdenacaoInsumosHospitalares._quick_sort_recursivo(lista, pivot_index + 1, fim, chave)

    @staticmethod
    def _particionar(lista: List[InsumoHospitalar], inicio: int, fim: int, chave: str) -> int:
        """Função de particionamento do quick sort"""
        pivot_valor = getattr(lista[fim], chave)
        i = inicio - 1

        for j in range(inicio, fim):
            if getattr(lista[j], chave) <= pivot_valor:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]

        lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
        return i + 1
