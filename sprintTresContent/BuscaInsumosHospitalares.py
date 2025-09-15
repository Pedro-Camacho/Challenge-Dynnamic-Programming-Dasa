from sprintTresContent.InsumoHospitalar import InsumoHospitalar
from sprintTresContent.Criticidade import Criticidade

from typing import List, Optional
class BuscaInsumosHospitalares:
    """Implementação de algoritmos de busca para insumos hospitalares"""

    @staticmethod
    def busca_sequencial_por_codigo(lista: List[InsumoHospitalar], codigo_procurado: str) -> Optional[int]:
        """
        Busca sequencial por código do insumo - O(n)
        Essencial para localizar rapidamente insumos por identificação única
        """
        for i, insumo in enumerate(lista):
            if insumo.codigo.upper() == codigo_procurado.upper():
                return i
        return None

    @staticmethod
    def busca_sequencial_por_criticidade(lista: List[InsumoHospitalar],
                                       criticidade: Criticidade) -> List[int]:
        """Busca todos os insumos de determinada criticidade"""
        indices = []
        for i, insumo in enumerate(lista):
            if insumo.criticidade == criticidade:
                indices.append(i)
        return indices

    @staticmethod
    def busca_binaria_por_nome(lista_ordenada: List[InsumoHospitalar],
                              nome_procurado: str) -> Optional[int]:
        """
        Busca binária por nome - O(log n)
        Requer lista ordenada por nome
        Eficiente para localizar insumos em grandes estoques
        """
        esquerda, direita = 0, len(lista_ordenada) - 1

        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            nome_meio = lista_ordenada[meio].nome.lower()
            nome_procurado_lower = nome_procurado.lower()

            if nome_meio == nome_procurado_lower:
                return meio
            elif nome_meio < nome_procurado_lower:
                esquerda = meio + 1
            else:
                direita = meio - 1

        return None
