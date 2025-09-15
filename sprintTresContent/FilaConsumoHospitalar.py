from datetime import datetime, timedelta
from sprintTresContent.InsumoHospitalar import InsumoHospitalar
from typing import List, Tuple, Optional
class FilaConsumoHospitalar:
    """Implementação de fila para registrar consumo diário de insumos médicos (FIFO)"""

    def __init__(self):
        self.items = []

    def enqueue(self, item: Tuple[datetime, InsumoHospitalar, int, str]):
        """Adiciona consumo ao final da fila (data, insumo, qtd_consumida, responsavel)"""
        self.items.append(item)

    def dequeue(self) -> Optional[Tuple[datetime, InsumoHospitalar, int, str]]:
        """Remove e retorna primeiro consumo da fila"""
        if self.is_empty():
            return None
        return self.items.pop(0)

    def peek(self) -> Optional[Tuple[datetime, InsumoHospitalar, int, str]]:
        """Retorna primeiro consumo sem remover"""
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def size(self) -> int:
        return len(self.items)

    def listar_consumos_cronologicos(self):
        """Lista consumos em ordem cronológica"""
        print("\n=== REGISTROS DE CONSUMO EM ORDEM CRONOLÓGICA ===")
        for data, insumo, qtd_consumida, responsavel in self.items:
            print(f"{data.strftime('%d/%m/%Y %H:%M')}: {insumo.nome} "
                  f"({qtd_consumida} unidades) - Responsável: {responsavel}")