from sprintTresContent.FilaConsumoHospitalar import FilaConsumoHospitalar
from sprintTresContent.PilhaConsultasHospitalar import PilhaConsultasHospitalar
from sprintTresContent.InsumoHospitalar import InsumoHospitalar
from sprintTresContent.Criticidade import Criticidade
from sprintTresContent.Setor import Setor
from sprintTresContent.BuscaInsumosHospitalares import BuscaInsumosHospitalares
from sprintTresContent.OrdenacaoInsumosHospitalares import OrdenacaoInsumosHospitalares
import random
from datetime import datetime, timedelta
class SistemaConsumoHospitalar:
    """Sistema principal para gerenciamento de consumo de insumos hospitalares"""

    def __init__(self):
        self.fila_consumo = FilaConsumoHospitalar()
        self.pilha_consultas = PilhaConsultasHospitalar()
        self.insumos = []
        self.busca = BuscaInsumosHospitalares()
        self.ordenacao = OrdenacaoInsumosHospitalares()

    def gerar_dados_hospitalares_simulados(self, quantidade: int = 25):
        """Gera dados simulados de insumos hospitalares"""
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
                # Reutiliza insumos se quantidade > lista disponível
                idx = i % len(insumos_medicos)
                nome, codigo_base, categoria, criticidade = insumos_medicos[idx]
                codigo = f"{codigo_base}_{i}"

            quantidade_estoque = random.randint(5, 500)

            # Validade baseada na criticidade (críticos têm validade mais longa)
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

            # Simula consumo
            data_consumo = data_inicial + timedelta(days=i//2, hours=random.randint(6, 22))
            qtd_consumida = random.randint(1, min(10, quantidade_estoque//10 + 1))
            responsavel = random.choice(responsaveis)

            consumo = (data_consumo, insumo, qtd_consumida, responsavel)

            # Adiciona na fila (ordem cronológica)
            self.fila_consumo.enqueue(consumo)

            # Adiciona na pilha (para consultas inversas)
            self.pilha_consultas.push(consumo)

            # Adiciona na lista geral
            self.insumos.append(insumo)

    def demonstrar_fila_hospitalar(self):
        """Demonstra o funcionamento da fila para registros hospitalares"""
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
        """Demonstra o funcionamento da pilha para consultas hospitalares"""
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
        """Demonstra algoritmos de busca para insumos hospitalares"""
        print("\n" + "="*70)
        print("DEMONSTRAÇÃO DE BUSCAS EM SISTEMA HOSPITALAR")
        print("="*70)

        # Busca sequencial por código
        codigo_procurado = "SER001"
        print(f"\n1. Buscando insumo por código '{codigo_procurado}' (busca sequencial):")

        indice = self.busca.busca_sequencial_por_codigo(self.insumos, codigo_procurado)
        if indice is not None:
            print(f"   ✓ Encontrado: {self.insumos[indice]}")
        else:
            print("   ✗ Não encontrado")

        # Busca por criticidade
        print(f"\n2. Buscando insumos CRÍTICOS (busca sequencial):")
        indices_criticos = self.busca.busca_sequencial_por_criticidade(
            self.insumos, Criticidade.CRITICA
        )
        print(f"   Encontrados {len(indices_criticos)} insumos críticos:")
        for idx in indices_criticos[:3]:  # Mostra apenas os 3 primeiros
            print(f"   - {self.insumos[idx].nome} ({self.insumos[idx].codigo})")

        # Busca binária por nome
        print(f"\n3. Busca binária por nome (requer ordenação):")
        insumos_ordenados = sorted(self.insumos, key=lambda x: x.nome.lower())
        nome_procurado = "Luva Nitrilo"

        indice = self.busca.busca_binaria_por_nome(insumos_ordenados, nome_procurado)
        if indice is not None:
            print(f"   ✓ '{nome_procurado}' encontrado na posição {indice}")
            print(f"   {insumos_ordenados[indice]}")
        else:
            print(f"   ✗ '{nome_procurado}' não encontrado")

    def demonstrar_ordenacao_hospitalar(self):
        """Demonstra algoritmos de ordenação para gestão hospitalar"""
        print("\n" + "="*70)
        print("DEMONSTRAÇÃO DE ORDENAÇÃO PARA GESTÃO HOSPITALAR")
        print("="*70)

        # Merge Sort por quantidade (controle de estoque)
        print("\n1. MERGE SORT - Insumos com MENOR estoque (controle crítico):")
        insumos_por_estoque = self.ordenacao.merge_sort(self.insumos, 'quantidade')
        print("   Insumos que precisam de reposição urgente:")
        for i, insumo in enumerate(insumos_por_estoque[:5]):
            status = "🔴 CRÍTICO" if insumo.quantidade < 20 else "🟡 BAIXO"
            print(f"   {i+1}. {insumo.nome}: {insumo.quantidade} unidades [{status}]")

        # Merge Sort por criticidade
        print("\n2. MERGE SORT - Ordenação por CRITICIDADE:")
        insumos_por_criticidade = self.ordenacao.merge_sort(self.insumos, 'criticidade')
        for i, insumo in enumerate(insumos_por_criticidade[:5]):
            print(f"   {i+1}. {insumo.nome} - {insumo.criticidade.value}")

        # Quick Sort por validade
        print("\n3. QUICK SORT - Insumos próximos ao VENCIMENTO:")
        insumos_por_validade = self.ordenacao.quick_sort(self.insumos, 'validade')
        print("   Prioritários para uso (vencimento mais próximo):")
        hoje = datetime.now()
        for i, insumo in enumerate(insumos_por_validade[:5]):
            dias_restantes = (insumo.validade - hoje).days
            urgencia = "🔴 URGENTE" if dias_restantes < 30 else "🟡 ATENÇÃO" if dias_restantes < 90 else "🟢 OK"
            print(f"   {i+1}. {insumo.nome}: {dias_restantes} dias [{urgencia}]")

    def gerar_relatorio_hospitalar(self):
        """Gera relatório completo do sistema hospitalar"""
        print("\n" + "="*80)
        print("RELATÓRIO COMPLETO - SISTEMA DE INSUMOS HOSPITALARES")
        print("="*80)

        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   • Total de insumos cadastrados: {len(self.insumos)}")
        print(f"   • Registros de consumo: {self.fila_consumo.size()}")
        print(f"   • Consultas realizadas: {self.pilha_consultas.size()}")

        if self.insumos:
            # Análise por criticidade
            criticos = len([i for i in self.insumos if i.criticidade == Criticidade.CRITICA])
            altos = len([i for i in self.insumos if i.criticidade == Criticidade.ALTA])
            medios = len([i for i in self.insumos if i.criticidade == Criticidade.MEDIA])
            baixos = len([i for i in self.insumos if i.criticidade == Criticidade.BAIXA])

            print(f"\n🎯 DISTRIBUIÇÃO POR CRITICIDADE:")
            print(f"   • Crítica: {criticos} insumos ({criticos/len(self.insumos)*100:.1f}%)")
            print(f"   • Alta: {altos} insumos ({altos/len(self.insumos)*100:.1f}%)")
            print(f"   • Média: {medios} insumos ({medios/len(self.insumos)*100:.1f}%)")
            print(f"   • Baixa: {baixos} insumos ({baixos/len(self.insumos)*100:.1f}%)")

            # Análise de estoque
            quantidade_total = sum(i.quantidade for i in self.insumos)
            estoque_baixo = len([i for i in self.insumos if i.quantidade < 50])

            print(f"\n📦 ANÁLISE DE ESTOQUE:")
            print(f"   • Quantidade total em estoque: {quantidade_total:,} unidades")
            print(f"   • Insumos com estoque baixo (<50): {estoque_baixo}")

            # Análise de vencimentos
            hoje = datetime.now()
            vencendo_30_dias = len([i for i in self.insumos if (i.validade - hoje).days <= 30])
            vencendo_90_dias = len([i for i in self.insumos if (i.validade - hoje).days <= 90])

            print(f"\n⏰ CONTROLE DE VENCIMENTOS:")
            print(f"   • Vencendo em 30 dias: {vencendo_30_dias} insumos")
            print(f"   • Vencendo em 90 dias: {vencendo_90_dias} insumos")

            # Análise por setor
            setores_contagem = {}
            for insumo in self.insumos:
                setor = insumo.setor.value
                setores_contagem[setor] = setores_contagem.get(setor, 0) + 1

            print(f"\n🏥 DISTRIBUIÇÃO POR SETOR:")
            for setor, count in sorted(setores_contagem.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {setor}: {count} insumos")
