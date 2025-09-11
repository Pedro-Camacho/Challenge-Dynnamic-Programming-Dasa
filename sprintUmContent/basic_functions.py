
#------------------------
# Funções para manipulação de insumos   
#------------------------
#Retirar insumo
def retirar_insumo(laboratorios,laboratorio: str, insumo: str, quantidade: int):
    """
    Retira uma quantidade específica de um insumo de um laboratório, caso haja estoque suficiente.

    Args:
        laboratorio (str): Nome do laboratório.
        insumo (str): Nome do insumo a ser retirado.
        quantidade (int): Quantidade a ser retirada.

    Returns:
        None
    """
    if insumo in laboratorios[laboratorio]["insumos"]:
        # Verifica se há quantidade suficiente para retirada
        if laboratorios[laboratorio]["insumos"][insumo] >= quantidade:
            laboratorios[laboratorio]["insumos"][insumo] -= quantidade


def adicionar_insumo(laboratorios,laboratorio: str, insumo: str, quantidade: int):
    """
    Adiciona uma quantidade específica de um insumo ao laboratório.

    Args:
        laboratorio (str): Nome do laboratório.
        insumo (str): Nome do insumo a ser adicionado.
        quantidade (int): Quantidade a ser adicionada.

    Returns:
        None
    """
    if insumo in laboratorios[laboratorio]["insumos"]:
        laboratorios[laboratorio]["insumos"][insumo] += quantidade

def contar_insumos_total(laboratorios,nome_lab: str):
    """
    Conta a quantidade total de insumos presentes em um laboratório.

    Args:
        nome_lab (str): Nome do laboratório.

    Returns:
        int or None: Quantidade total de insumos, ou None se o laboratório não for encontrado.
    """
    insumos_totais = 0

    if nome_lab in laboratorios:
        # Soma todas as quantidades de insumos do laboratório
        for insumo in laboratorios[nome_lab]["insumos"]:
            insumos_totais += laboratorios[nome_lab]["insumos"][insumo]
        return insumos_totais
    else:
        print(f"Erro: laboratório '{nome_lab}' não foi encontrado.")
        return None
