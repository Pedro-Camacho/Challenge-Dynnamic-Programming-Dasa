from datetime import datetime, timedelta
from sprintTresContent.InsumoHospitalar import InsumoHospitalar
from typing import List, Tuple, Optional

class PilhaConsultasHospitalar:
    """Implementação de pilha para consultas inversas de consumos médicos (LIFO)"""

    def __init__(self):
        self.items = []

    def push(self, item: Tuple[datetime, InsumoHospitalar, int, str]):
        """Adiciona consulta ao topo da pilha"""
        self.items.append(item)

    def pop(self) -> Optional[Tuple[datetime, InsumoHospitalar, int, str]]:
        """Remove e retorna consulta do topo"""
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self) -> Optional[Tuple[datetime, InsumoHospitalar, int, str]]:
        """Retorna consulta do topo sem remover"""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def size(self) -> int:
        return len(self.items)

    def listar_ultimos_consumos(self):
        """Lista últimos consumos (ordem inversa)"""
        print("\n=== ÚLTIMOS CONSUMOS (MAIS RECENTES PRIMEIRO) ===")
        for data, insumo, qtd_consumida, responsavel in reversed(self.items):
            print(f"{data.strftime('%d/%m/%Y %H:%M')}: {insumo.nome} "
                  f"({qtd_consumida} unidades) - {responsavel}")
