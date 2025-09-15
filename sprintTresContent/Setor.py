from enum import Enum
class Setor(Enum):
    """Setores do hospital"""
    UTI = "UTI"
    EMERGENCIA = "Emergência"
    CIRURGIA = "Cirurgia"
    ENFERMARIA = "Enfermaria"
    PEDIATRIA = "Pediatria"
    MATERNIDADE = "Maternidade"
    LABORATORIO = "Laboratório"
    FARMACIA = "Farmácia"