from sprintTresContent.FilaConsumoHospitalar import FilaConsumoHospitalar
from sprintTresContent.PilhaConsultasHospitalar import PilhaConsultasHospitalar
from sprintTresContent.InsumoHospitalar import InsumoHospitalar
from sprintTresContent.Criticidade import Criticidade
from sprintTresContent.Setor import Setor
from sprintTresContent.BuscaInsumosHospitalares import BuscaInsumosHospitalares
from sprintTresContent.OrdenacaoInsumosHospitalares import OrdenacaoInsumosHospitalares
from sprintTresContent.ConsumoAggregado import ConsumoAggregado
import random
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict
from collections import deque, defaultdict

class SistemaConsumoHospitalar:
    """Sistema principal para gerenciamento de consumo de insumos hospitalares"""

    def __init__(self):
        self.fila_consumo = FilaConsumoHospitalar()
        self.pilha_consultas = PilhaConsultasHospitalar()
        self.insumos: List[InsumoHospitalar] = []
        self.busca = BuscaInsumosHospitalares()
        self.ordenacao = OrdenacaoInsumosHospitalares()

    # --------- GERAÇÃO DE DADOS ---------
    def gerar_dados_hospitalares_simulados(self, quantidade: int = 25):
        """Gera dados simulados de insumos e eventos de consumo"""
        insumos_medicos = [
            ("Seringa 10ml", "SER001", "Descartáveis", Criticidade.ALTA),
            ("Luva Nitrilo", "LUV001", "EPI", Criticidade.CRITICA),
            ("Máscara N95", "MAS001", "EPI", Criticidade.CRITICA),
            ("Cateter Venoso", "CAT001", "Invasivos", Criticidade.ALTA),
            ("Gaze Estéril", "GAZ001", "Curativos", Criticidade.MEDIA),
            ("Soro Fisiológico", "SOR001", "Soluções", Criticidade.ALTA),
            ("Dipirona 500mg", "DIP001", "Medicamentos", Criticidade.MEDIA),
            ("Morfina 10mg", "MOR001", "Controlados", Criticidade.CRITICA),
            ("Oxímetro Digital", "OXI001", "Equipamentos", Criticidade.BAIXA),
            ("Termômetro Digital", "TER001", "Equipamentos", Criticidade.BAIXA),
            ("Atadura Elástica", "ATA001", "Curativos", Criticidade.BAIXA),
            ("Álcool 70%", "ALC001", "Antissépticos", Criticidade.MEDIA),
            ("Iodopolividona", "IOD001", "Antissépticos", Criticidade.MEDIA),
            ("Desfibrilador Externo", "DEF001", "Equipamentos", Criticidade.CRITICA),
            ("Ventilador Pulmonar", "VEN001", "Equipamentos", Criticidade.CRITICA),
            ("Adrenalina 1mg", "ADR001", "Emergência", Criticidade.CRITICA),
            ("Aspirador Cirúrgico", "ASP001", "Equipamentos", Criticidade.ALTA),
            ("Fio de Sutura", "FIO001", "Cirúrgicos", Criticidade.ALTA),
            ("Lâmina Bisturi", "LAM001", "Cirúrgicos", Criticidade.ALTA),
            ("Tubo Endotraqueal", "TUB001", "Intubação", Criticidade.CRITICA)
        ]

        setores_lista = list(Setor)
        fornecedores = ["MedSupply", "HealthTech", "BioMed", "Cirúrgica Brasil", "Hospitalar SP"]
        responsaveis = ["Dr. Silva", "Enf. Maria", "Dr. Santos", "Enf. Ana", "Dr. Costa"]

        data_inicial = datetime.now() - timedelta(days=15)

        for i in range(quantidade):
            if i < len(insumos_medicos):
                nome, codigo, categoria, criticidade = insumos_medicos[i]
            else:
                idx = i % len(insumos_medicos)
                nome, codigo_base, categoria, criticidade = insumos_medicos[idx]
                codigo = f"{codigo_base}_{i}"

            quantidade_estoque = random.randint(5, 500)

            # Validade baseada na criticidade
            if criticidade == Criticidade.CRITICA:
                dias_validade = random.randint(180, 730)  # 6 meses a 2 anos
            elif criticidade == Criticidade.ALTA:
                dias_validade = random.randint(90, 365)   # 3 meses a 1 ano
            else:
                dias_validade = random.randint(30, 180)   # 1 a 6 meses

            validade = datetime.now() + timedelta(days=dias_validade)
            setor = random.choice(setores_lista)
            lote = f"LT{random.randint(1000, 9999)}"
            fornecedor = random.choice(fornecedores)

            insumo = InsumoHospitalar(
                nome, codigo, quantidade_estoque, validade, categoria,
                setor, criticidade, lote, fornecedor
            )

            # Simula um registro de consumo para esse insumo
            data_consumo = data_inicial + timedelta(days=i // 2, hours=random.randint(6, 22))
            qtd_consumida = random.randint(1, max(1, min(10, insumo.quantidade // 10 + 1)))
            responsavel = random.choice(responsaveis)

            consumo = (data_consumo, insumo, qtd_consumida, responsavel)

            # Registra consumo nas estruturas
            self.fila_consumo.enqueue(consumo)     # ordem cronológica
            self.pilha_consultas.push(consumo)     # para últimos consumos
            self.insumos.append(insumo)            # catálogo

    # --------- BUSCAS NO REGISTRO DE CONSUMO ---------
    def busca_consumo_por_codigo(self, codigo: str) -> List[Tuple[datetime, InsumoHospitalar, int, str]]:
        """Busca sequencial no REGISTRO DE CONSUMO (fila) por código do insumo"""
        resultados = []
        for data, insumo, qtd, resp in self.fila_consumo.items:
            if insumo.codigo.upper() == codigo.upper():
                resultados.append((data, insumo, qtd, resp))
        return resultados

    def busca_binaria_consumo_por_nome(self, nome: str) -> Optional[Tuple[int, Tuple[datetime, InsumoHospitalar, int, str]]]:
        """Busca binária por NOME no REGISTRO DE CONSUMO (pré-ordenando cópia dos eventos por nome)"""
        eventos = list(self.fila_consumo.items)
        eventos.sort(key=lambda e: e[1].nome.lower())  # e[1] é o InsumoHospitalar
        alvo = nome.lower()
        l, r = 0, len(eventos) - 1
        while l <= r:
            m = (l + r) // 2
            nome_m = eventos[m][1].nome.lower()
            if nome_m == alvo:
                return m, eventos[m]
            elif nome_m < alvo:
                l = m + 1
            else:
                r = m - 1
        return None

    # --------- AGREGAÇÃO/ORDENAÇÃO POR QUANTIDADE CONSUMIDA ---------
    def consumo_total_por_insumo(self) -> Dict[str, Tuple[InsumoHospitalar, int]]:
        """Mapa codigo -> (insumo_ref, total_consumido) a partir do REGISTRO DE CONSUMO"""
        acc: Dict[str, List] = defaultdict(lambda: [None, 0])
        for _, insumo, qtd, _ in self.fila_consumo.items:
            if acc[insumo.codigo][0] is None:
                acc[insumo.codigo][0] = insumo
            acc[insumo.codigo][1] += qtd
        # converte para dict tipado
        return {k: (v[0], v[1]) for k, v in acc.items()}

    def ranking_mais_consumidos_merge(self, k: int = 5) -> List[ConsumoAggregado]:
        """Ranking pelos mais consumidos usando MERGE SORT (estável)"""
        acc = self.consumo_total_por_insumo()
        lista = [ConsumoAggregado(insumo=ref, total_consumido=total) for ref, total in acc.values()]
        # queremos decrescente -> usamos merge crescente e invertimos, ou criamos chave negativa.
        ordenado = self.ordenacao.merge_sort(lista, chave='total_consumido')
        return list(reversed(ordenado))[:k]

    def ranking_mais_consumidos_quick(self, k: int = 5) -> List[ConsumoAggregado]:
        """Ranking pelos mais consumidos usando QUICK SORT"""
        acc = self.consumo_total_por_insumo()
        lista = [ConsumoAggregado(insumo=ref, total_consumido=total) for ref, total in acc.values()]
        ordenado = self.ordenacao.quick_sort(lista, chave='total_consumido')
        return list(reversed(ordenado))[:k]

    # --------- DEMONSTRAÇÕES ---------
    def demonstrar_fila_hospitalar(self):
        print("\n" + "="*70)
        print("DEMONSTRAÇÃO DA FILA - REGISTRO DE CONSUMO HOSPITALAR (FIFO)")
        print("="*70)
        self.fila_consumo.listar_consumos_cronologicos()
        print(f"\nTotal de registros na fila: {self.fila_consumo.size()}")
        print("\nProcessando primeiros 3 registros de consumo:")
        for i in range(3):
            if not self.fila_consumo.is_empty():
                data, insumo, qtd, responsavel = self.fila_consumo.dequeue()
                print(f"{i+1}. Processado: {data.strftime('%d/%m/%Y %H:%M')} - "
                      f"{insumo.nome} ({qtd} unidades) por {responsavel}")

    def demonstrar_pilha_hospitalar(self):
        print("\n" + "="*70)
        print("DEMONSTRAÇÃO DA PILHA - CONSULTA DE ÚLTIMOS CONSUMOS (LIFO)")
        print("="*70)
        self.pilha_consultas.listar_ultimos_consumos()
        print(f"\nTotal de registros na pilha: {self.pilha_consultas.size()}")
        print("\nConsultando últimos 3 registros:")
        for i in range(3):
            if not self.pilha_consultas.is_empty():
                data, insumo, qtd, responsavel = self.pilha_consultas.pop()
                print(f"{i+1}. Último: {data.strftime('%d/%m/%Y %H:%M')} - "
                      f"{insumo.nome} ({qtd} unidades) - {responsavel}")

    def demonstrar_buscas_hospitalares(self):
        print("\n" + "="*70)
        print("DEMONSTRAÇÃO DE BUSCAS EM SISTEMA HOSPITALAR")
        print("="*70)

        # --- Catálogo (insumos) ---
        codigo_procurado = "SER001"
        print(f"\n1. Catálogo: buscando insumo por código '{codigo_procurado}' (sequencial em catálogo):")
        indice = self.busca.busca_sequencial_por_codigo(self.insumos, codigo_procurado)
        if indice is not None:
            print(f"   ✓ Encontrado no catálogo: {self.insumos[indice]}")
        else:
            print("   ✗ Não encontrado no catálogo")

        print(f"\n2. Catálogo: buscando insumos CRÍTICOS (sequencial em catálogo):")
        indices_criticos = self.busca.busca_sequencial_por_criticidade(self.insumos, Criticidade.CRITICA)
        print(f"   Encontrados {len(indices_criticos)} insumos críticos (amostra de 3):")
        for idx in indices_criticos[:3]:
            print(f"   - {self.insumos[idx].nome} ({self.insumos[idx].codigo})")

        print(f"\n3. Catálogo: busca binária por nome (com pré-ordenação do catálogo):")
        insumos_ordenados = sorted(self.insumos, key=lambda x: x.nome.lower())
        nome_procurado = "Luva Nitrilo"
        indice = self.busca.busca_binaria_por_nome(insumos_ordenados, nome_procurado)
        if indice is not None:
            print(f"   ✓ '{nome_procurado}' encontrado na posição {indice}")
            print(f"   {insumos_ordenados[indice]}")
        else:
            print(f"   ✗ '{nome_procurado}' não encontrado no catálogo")

        # --- Registro de consumo (fila/pilha) ---
        print(f"\n4. REGISTRO DE CONSUMO: busca sequencial por CÓDIGO '{codigo_procurado}' na FILA:")
        ocorrencias = self.busca_consumo_por_codigo(codigo_procurado)
        if ocorrencias:
            print(f"   ✓ {len(ocorrencias)} ocorrência(s) no registro de consumo (exibindo 1):")
            d, ins, qtd, resp = ocorrencias[0]
            print(f"     - {d.strftime('%d/%m/%Y %H:%M')} {ins.nome} ({ins.codigo}) - {qtd} un. - {resp}")
        else:
            print("   ✗ Nenhum consumo encontrado para esse código.")

        print(f"\n5. REGISTRO DE CONSUMO: busca binária por NOME '{nome_procurado}' na FILA:")
        achado = self.busca_binaria_consumo_por_nome(nome_procurado)
        if achado:
            pos, (d, ins, qtd, resp) = achado
            print(f"   ✓ Encontrado após ordenação dos eventos por nome (pos {pos})")
            print(f"     - {d.strftime('%d/%m/%Y %H:%M')} {ins.nome} ({ins.codigo}) - {qtd} un. - {resp}")
        else:
            print("   ✗ Nenhum consumo encontrado para esse nome (no registro).")

    def demonstrar_ordenacao_hospitalar(self):
        print("\n" + "="*70)
        print("DEMONSTRAÇÃO DE ORDENAÇÃO PARA GESTÃO HOSPITALAR")
        print("="*70)

        # Merge Sort por quantidade (estoque disponível)
        print("\n1. MERGE SORT - Insumos com MENOR estoque (controle crítico):")
        insumos_por_estoque = self.ordenacao.merge_sort(self.insumos, 'quantidade')
        print("   Insumos que precisam de reposição urgente:")
        for i, insumo in enumerate(insumos_por_estoque[:5]):
            status = "🔴 CRÍTICO" if insumo.quantidade < 20 else "🟡 BAIXO"
            print(f"   {i+1}. {insumo.nome}: {insumo.quantidade} unidades [{status}]")

        # Merge Sort por criticidade (decrescente)
        print("\n2. MERGE SORT - Ordenação por CRITICIDADE:")
        insumos_por_criticidade = self.ordenacao.merge_sort(self.insumos, 'criticidade')
        for i, insumo in enumerate(insumos_por_criticidade[:5]):
            print(f"   {i+1}. {insumo.nome} - {insumo.criticidade.value}")

        # Quick Sort por validade (FEFO)
        print("\n3. QUICK SORT - Insumos próximos ao VENCIMENTO:")
        insumos_por_validade = self.ordenacao.quick_sort(self.insumos, 'validade')
        print("   Prioritários para uso (vencimento mais próximo):")
        hoje = datetime.now()
        for i, insumo in enumerate(insumos_por_validade[:5]):
            dias_restantes = (insumo.validade - hoje).days
            urgencia = "🔴 URGENTE" if dias_restantes < 30 else "🟡 ATENÇÃO" if dias_restantes < 90 else "🟢 OK"
            print(f"   {i+1}. {insumo.nome}: {dias_restantes} dias [{urgencia}]")

        # Ranking por quantidade CONSUMIDA (com merge e com quick, só para demonstrar ambos)
        print("\n4. RANKING - Mais consumidos (MERGE SORT):")
        for i, item in enumerate(self.ranking_mais_consumidos_merge(), 1):
            print(f"   {i}. {item.insumo.nome} ({item.insumo.codigo}) – {item.total_consumido} un.")

        print("\n5. RANKING - Mais consumidos (QUICK SORT):")
        for i, item in enumerate(self.ranking_mais_consumidos_quick(), 1):
            print(f"   {i}. {item.insumo.nome} ({item.insumo.codigo}) – {item.total_consumido} un.")

    # --------- RELATÓRIO ---------
    def gerar_relatorio_hospitalar(self):
        print("\n" + "="*80)
        print("RELATÓRIO COMPLETO - SISTEMA DE INSUMOS HOSPITALARES")
        print("="*80)

        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   • Total de insumos cadastrados: {len(self.insumos)}")
        print(f"   • Registros de consumo: {self.fila_consumo.size()}")
        print(f"   • Consultas realizadas: {self.pilha_consultas.size()}")

        if self.insumos:
            # Distribuição por criticidade
            criticos = sum(1 for i in self.insumos if i.criticidade == Criticidade.CRITICA)
            altos    = sum(1 for i in self.insumos if i.criticidade == Criticidade.ALTA)
            medios   = sum(1 for i in self.insumos if i.criticidade == Criticidade.MEDIA)
            baixos   = sum(1 for i in self.insumos if i.criticidade == Criticidade.BAIXA)

            print(f"\n🎯 DISTRIBUIÇÃO POR CRITICIDADE:")
            total = len(self.insumos)
            print(f"   • Crítica: {criticos} insumos ({criticos/total*100:.1f}%)")
            print(f"   • Alta: {altos} insumos ({altos/total*100:.1f}%)")
            print(f"   • Média: {medios} insumos ({medios/total*100:.1f}%)")
            print(f"   • Baixa: {baixos} insumos ({baixos/total*100:.1f}%)")

            # Análise de estoque
            quantidade_total = sum(i.quantidade for i in self.insumos)
            estoque_baixo = sum(1 for i in self.insumos if i.quantidade < 50)

            print(f"\n📦 ANÁLISE DE ESTOQUE:")
            print(f"   • Quantidade total em estoque: {quantidade_total:,} unidades")
            print(f"   • Insumos com estoque baixo (<50): {estoque_baixo}")

            # Análise de vencimentos
            hoje = datetime.now()
            vencendo_30_dias = sum(1 for i in self.insumos if (i.validade - hoje).days <= 30)
            vencendo_90_dias = sum(1 for i in self.insumos if (i.validade - hoje).days <= 90)

            print(f"\n⏰ CONTROLE DE VENCIMENTOS:")
            print(f"   • Vencendo em 30 dias: {vencendo_30_dias} insumos")
            print(f"   • Vencendo em 90 dias: {vencendo_90_dias} insumos")

            # Análise por setor
            setores_contagem: Dict[str, int] = defaultdict(int)
            for insumo in self.insumos:
                setores_contagem[insumo.setor.value] += 1

            print(f"\n🏥 DISTRIBUIÇÃO POR SETOR:")
            for setor, count in sorted(setores_contagem.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {setor}: {count} insumos")

            # Top consumidos no período
            print(f"\n🔥 TOP CONSUMIDOS (agregado no período):")
            for i, item in enumerate(self.ranking_mais_consumidos_merge(), 1):
                print(f"   {i}. {item.insumo.nome} ({item.insumo.codigo}) – {item.total_consumido} un.")

    # --------- EXPLICAÇÃO/CONTEXTUALIZAÇÃO ---------
    def imprimir_justificativas(self):
        print("\n" + "="*80)
        print("📚 JUSTIFICATIVA DAS ESTRUTURAS NO CONTEXTO HOSPITALAR:")
        print("="*80)
        justificativas = {
            "🔄 FILA (Queue) - FIFO": [
                "• Registra consumos na ordem cronológica exata",
                "• Garante rastreabilidade para auditoria hospitalar",
                "• Processa requisições de insumos por ordem de chegada",
                "• Essencial para controle de lotes e validades (FIFO médico)"
            ],
            "📚 PILHA (Stack) - LIFO": [
                "• Consulta rápida dos últimos consumos realizados",
                "• Histórico imediato para tomada de decisões urgentes",
                "• Auditoria reversa em caso de problemas com lotes",
                "• Análise de padrões de consumo recentes"
            ],
            "🔍 BUSCAS (Catálogo e Registro)": [
                "• Sequencial por código (ANVISA/identificador único)",
                "• Por criticidade para emergências",
                "• Binária por nome com pré-ordenação (catálogo e registro)",
                "• No registro de consumo (fila) para localizar eventos específicos"
            ],
            "🔧 MERGE SORT": [
                "• Ordenação estável - preserva ordem de equivalentes",
                "• Confiável para relatórios gerenciais (O(n log n))",
                "• Usado para estoque/criticidade e ranking por consumo"
            ],
            "⚡ QUICK SORT": [
                "• Ordenação rápida por validade - FEFO",
                "• Performance média superior para grandes volumes",
                "• Ajuda a priorizar uso e descarte"
            ]
        }
        for estrutura, detalhes in justificativas.items():
            print(f"\n{estrutura}:")
            for detalhe in detalhes:
                print(f"  {detalhe}")

        print(f"\n💡 CONTEXTO MÉDICO-HOSPITALAR:")
        print(f"  • CRITICIDADE: Insumos críticos (respiradores, medicamentos controlados)")
        print(f"  • RASTREABILIDADE: Controle de lotes para recalls e efeitos adversos")
        print(f"  • VENCIMENTO: Gestão FEFO para evitar desperdícios e riscos")
        print(f"  • AUDITORIA: Registros cronológicos para inspeções e conformidade")
        print(f"  • EMERGÊNCIA: Acesso rápido a insumos em situações críticas")
