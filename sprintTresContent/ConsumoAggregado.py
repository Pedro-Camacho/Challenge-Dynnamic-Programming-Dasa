from dataclasses import dataclass
from sprintTresContent.InsumoHospitalar import InsumoHospitalar
@dataclass
class ConsumoAggregado:
    """View para ranking por quantidade consumida no período simulado"""
    insumo: InsumoHospitalar
    total_consumido: int