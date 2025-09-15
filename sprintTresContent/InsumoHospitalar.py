from dataclasses import dataclass
from datetime import datetime, timedelta
from sprintTresContent.Criticidade import Criticidade
from sprintTresContent.Setor import Setor
@dataclass
class InsumoHospitalar:
    """Classe para representar um insumo médico hospitalar"""
    nome: str
    codigo: str
    quantidade: int
    validade: datetime
    categoria: str
    setor: Setor
    criticidade: Criticidade
    lote: str
    fornecedor: str

    def __str__(self):
        return (f"{self.codigo} - {self.nome}: {self.quantidade} unidades "
                f"(Val: {self.validade.strftime('%d/%m/%Y')}) "
                f"[{self.criticidade.value}] - {self.setor.value}")
