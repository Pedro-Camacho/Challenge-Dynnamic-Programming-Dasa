import pandas as pd
from haversine import haversine as hs_func, Unit
# Dados dos laboratórios
#------------------------
# Função para utilizar de um dicionário externo e criar um dataFrame para médias
#------------------------
def criar_df_medias(laboratorios=None, soma_insumos=None):
    num_labs = len(laboratorios)
    """
    Calcula a média de uso de insumos por laboratório e retorna um DataFrame com os resultados.

    Esta função percorre todos os laboratórios e soma a quantidade de cada insumo utilizado.
    Em seguida, calcula a média de uso por insumo com base no número total de laboratórios,
    salva os resultados em um arquivo CSV e retorna um DataFrame com os dados.

    Returns:
        pd.DataFrame: DataFrame contendo os nomes dos insumos e suas médias de uso por laboratório.
    """

    # Somar os insumos de todos os laboratórios
    for dados in laboratorios.values():
        for insumo, quantidade in dados["insumos"].items():
            soma_insumos[insumo] = soma_insumos.get(insumo, 0) + quantidade

    # Calcular a média de insumos por laboratório
    medias = {
        insumo: quantidade / num_labs
        for insumo, quantidade in soma_insumos.items()
    }

    # Criar DataFrame com os dados de média
    df_medias = pd.DataFrame(list(medias.items()), columns=["Insumo", "Média"])

    # Caminho onde o CSV será salvo (ajuste se necessário)
    caminho_medias_csv = "sprintUmContent/medias_insumos_laboratorios.csv"

    # Salvar o DataFrame em CSV
    df_medias.to_csv(caminho_medias_csv, index=False)

    # Ler o arquivo salvo e retornar o DataFrame
    df = pd.read_csv(caminho_medias_csv)
    return df



def estado_critico(laboratorios, laboratorio: str, insumo: str, df_media):
    """
    Verifica se um insumo de um laboratório está em estado crítico,
    ou seja, abaixo ou igual à média geral desse insumo.

    Args:
        laboratorio (str): Nome do laboratório.
        insumo (str): Nome do insumo a ser verificado.
        df_media (pd.DataFrame): DataFrame com as médias dos insumos (opcional).

    Returns:
        bool: True se o insumo está em estado crítico, False caso contrário.
    """
    media_insumo = df_media[df_media['Insumo'] == insumo]
    return laboratorios[laboratorio]["insumos"][insumo] <= media_insumo['Média'].values[0]


def labs_criticos(laboratorios: dict, df_media):
    """
    Retorna uma lista de tuplas com laboratórios e insumos que estão em estado crítico.

    Args:
        laboratorios (dict): Dicionário contendo os dados dos laboratórios.
        df_media (pd.DataFrame): DataFrame com as médias dos insumos (opcional).

    Returns:
        list[tuple]: Lista de tuplas (laboratório, insumo) em estado crítico.
    """
    labs_criticos = []
    for lab in laboratorios:
        for insumo in laboratorios[lab]["insumos"]:
            if estado_critico(laboratorios,lab, insumo, df_media):
                labs_criticos.append((lab, insumo))
    return labs_criticos


def dict_labs_criticos(laboratorios: dict, df_media):
    """
    Retorna um dicionário contendo, para cada laboratório, uma lista de insumos
    em estado crítico com suas quantidades atuais.

    Args:
        laboratorios (dict): Dicionário com os dados dos laboratórios.
        df_media (pd.DataFrame): DataFrame com as médias dos insumos (opcional).

    Returns:
        dict: Dicionário {laboratório: [(insumo, quantidade), ...]}.
    """
    resultado = {}

    for lab in laboratorios:
        insumos_criticos = []
        for insumo, quantidade in laboratorios[lab]["insumos"].items():
            if estado_critico(laboratorios,lab, insumo, df_media):
                insumos_criticos.append((insumo, quantidade))

        if insumos_criticos:
            resultado[lab] = insumos_criticos

    return resultado


def df_labs_criticos(laboratorios: dict, df_media):
    """
    Constrói um DataFrame contendo os laboratórios e insumos que estão em estado crítico,
    com as respectivas quantidades atuais.

    Args:
        laboratorios (dict): Dicionário com os dados dos laboratórios.
        df_media (pd.DataFrame): DataFrame com as médias dos insumos (opcional).

    Returns:
        pd.DataFrame: DataFrame com colunas: "Laboratório", "Insumo Crítico" e "Quantidade Atual",
                      ordenado por quantidade e nome do laboratório.
    """
    dados = []

    for lab, insumos in dict_labs_criticos(laboratorios, df_media).items():
        for insumo, quantidade in insumos:
            dados.append({
                "Laboratório": lab,
                "Insumo Crítico": insumo,
                "Quantidade Atual": quantidade
            })

    df = pd.DataFrame(dados)
    return df.sort_values(by=["Quantidade Atual", "Laboratório"])


#------------------------
# Função para encontrar o almoxarifado mais próximo
#-------------------------
def encontrar_almoxarifado_mais_proximo(laboratorios,almoxarifados, lab_nome, insumo):
    """
    Encontra o almoxarifado mais próximo de um laboratório que possua o insumo disponível em estoque.

    A função calcula a distância entre o laboratório e os almoxarifados com base nas coordenadas geográficas
    usando a fórmula de Haversine. Retorna o almoxarifado mais próximo com o insumo disponível.

    Args:
        lab_nome (str): Nome do laboratório de origem.
        insumo (str): Nome do insumo necessário.

    Returns:
        tuple or str:
            - (str) Nome do almoxarifado mais próximo
            - (float) Distância em quilômetros até o almoxarifado
            - (int) Quantidade disponível do insumo no almoxarifado
            - Caso nenhum almoxarifado tenha o insumo, retorna uma string com mensagem de erro.
    """
    lab_coord = laboratorios[lab_nome]["coordenadas"]
    candidatos = []

    for nome_almox, dados in almoxarifados.items():
        # Verifica se o almoxarifado tem o insumo em estoque
        if dados["estoque"].get(insumo, 0) > 0:
            # Calcula a distância usando Haversine
            dist = hs_func(
                (lab_coord["latitude"], lab_coord["longitude"]),
                (dados["coordenadas"]["latitude"], dados["coordenadas"]["longitude"]),
                unit=Unit.KILOMETERS
            )
            # Armazena os candidatos como tupla: (nome, distância, quantidade disponível)
            candidatos.append((nome_almox, dist, dados["estoque"][insumo]))

    if not candidatos:
        return f"Nenhum almoxarifado com estoque disponível para '{insumo}'."

    # Ordena os candidatos pela menor distância
    candidatos.sort(key=lambda x: x[1])
    nome, distancia, qtd_disp = candidatos[0]

    return nome, round(distancia, 2), qtd_disp


def df_completo_labs_criticos(laboratorios: dict, almoxarifados:dict, df_media):
    """
    Gera um DataFrame com todos os laboratórios que possuem insumos em estado crítico,
    incluindo o almoxarifado mais próximo para reabastecimento.

    Para cada insumo crítico encontrado em um laboratório, a função localiza o almoxarifado
    mais próximo com base na função `encontrar_almoxarifado_mais_proximo` e adiciona essa
    informação ao relatório.

    Args:
        laboratorios (dict): Dicionário com os dados dos laboratórios e seus insumos.
        almoxarifados (dict): Dicionário com os almoxarifados disponíveis e suas localizações.
        df_media (pd.DataFrame): DataFrame contendo as médias dos insumos por laboratório.

    Returns:
        pd.DataFrame: Um DataFrame com os seguintes campos:
            - Laboratório
            - Insumo
            - Quantidade Atual
            - Nome almoxarifado
            - Distância (em km) até o almoxarifado
    """
    dados = []

    # Obtém todos os insumos em estado crítico por laboratório
    criticos = dict_labs_criticos(laboratorios, df_media)

    for lab, insumos in criticos.items():
        for insumo, quantidade in insumos:
            # Retorna uma tupla: (nome do almoxarifado, distância, coordenadas)
            retorno = encontrar_almoxarifado_mais_proximo(laboratorios, almoxarifados,lab, insumo)
            if isinstance(retorno, tuple):
                almox, distancia, _ = retorno
                dados.append({
                    "Laboratório": lab,
                    "Insumo": insumo,
                    "Quantidade Atual": quantidade,
                    "Nome almoxarifado": almox,
                    "Distancia": f"{distancia:.2f} km"
                })

    return pd.DataFrame(dados)

def almoxarifados_labs_criticos(laboratorios: dict, almoxarifados:dict, df_media):
    """
    Para cada laboratório com insumos em estado crítico, encontra o almoxarifado mais próximo
    que possui o insumo em estoque.

    Utiliza a função `labs_criticos` para identificar os pares (laboratório, insumo crítico)
    e depois busca o almoxarifado mais próximo com base na distância geográfica.

    Returns:
        list[dict]: Lista de dicionários, cada um contendo:
            - 'Nome almoxarifado': nome do almoxarifado mais próximo
            - 'Distancia': distância em km
            - 'Quantidade': quantidade disponível no almoxarifado
            - 'Laboratório': nome do laboratório em estado crítico
            - 'Insumo': insumo em estado crítico
    """
    almoxarifados_dist = []

    # Itera sobre todos os laboratórios e insumos críticos
    for lab in labs_criticos(laboratorios,df_media):
        retorno = encontrar_almoxarifado_mais_proximo(laboratorios,almoxarifados,lab[0], lab[1])

        # Monta o dicionário com informações de rota e estoque
        almoxarifado_info = {
            'Nome almoxarifado': retorno[0],
            'Distancia': retorno[1],
            'Quantidade': retorno[2],
            'Laboratório': lab[0],
            'Insumo': lab[1]
        }

        almoxarifados_dist.append(almoxarifado_info)

    return almoxarifados_dist


def df_almoxarifados_labs_criticos(laboratorios: dict, almoxarifados:dict, df_media):
    """
    Constrói um DataFrame contendo os laboratórios com insumos críticos e seus respectivos
    almoxarifados mais próximos.

    Retorna:
        pd.DataFrame: DataFrame com as colunas:
            - 'Nome almoxarifado'
            - 'Distancia'
            - 'Quantidade'
            - 'Laboratório'
            - 'Insumo'
        O DataFrame é ordenado pela distância e nome do laboratório.
    """
    dados = almoxarifados_labs_criticos(laboratorios, almoxarifados,df_media)
    df = pd.DataFrame(dados)

    # Ordena por menor distância e nome do laboratório
    df = df.sort_values(by=["Distancia", "Laboratório"])

    return df

