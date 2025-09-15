from enum import Enum
class Criticidade(Enum):
    """Níveis de criticidade dos insumos hospitalares"""
    CRITICA = "Crítica"
    ALTA = "Alta"
    MEDIA = "Média"
    BAIXA = "Baixa"