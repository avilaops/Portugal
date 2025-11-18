"""
Sistema de Mapeamento de Estabelecimentos - Lisboa
Ferramenta para catalogar e analisar estabelecimentos comerciais
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class TipoNegocio(Enum):
    RESTAURANTE = "Restaurante"
    CAFE = "Café"
    BAR = "Bar"
    VAREJO = "Varejo"
    SERVICOS = "Serviços"
    HOTEL = "Hotel"
    SUPERMERCADO = "Supermercado"
    PADARIA = "Padaria"
    OUTRO = "Outro"


class NivelPresencaDigital(Enum):
    NENHUMA = "Nenhuma presença online"
    BASICA = "Apenas redes sociais"
    INTERMEDIARIA = "Site simples + redes sociais"
    AVANCADA = "Site profissional + e-commerce + redes sociais"


class PotencialCliente(Enum):
    BAIXO = "Baixo"
    MEDIO = "Médio"
    ALTO = "Alto"
    MUITO_ALTO = "Muito Alto"


@dataclass
class Estabelecimento:
    """Representa um estabelecimento mapeado"""

    nome: str
    endereco: str
    bairro: str
    tipo_negocio: str

    # Presença Digital
    tem_site: bool = False
    url_site: Optional[str] = None
    tem_instagram: bool = False
    url_instagram: Optional[str] = None
    tem_facebook: bool = False
    url_facebook: Optional[str] = None
    tem_google_business: bool = False

    # Análise Visual
    aparencia_estabelecimento: Optional[str] = (
        None  # "Moderno", "Tradicional", "Precisa reforma", etc.
    )
    movimento_aparente: Optional[str] = None  # "Alto", "Médio", "Baixo"

    # Análise de Necessidades
    nivel_presenca_digital: Optional[str] = None
    precisa_site: bool = False
    precisa_sistema_gestao: bool = False
    precisa_marketing_digital: bool = False
    precisa_sistema_reservas: bool = False
    precisa_ecommerce: bool = False

    # Oportunidades Identificadas
    oportunidades: List[str] = None
    observacoes: str = ""

    # Potencial
    potencial_cliente: Optional[str] = None
    prioridade_contato: int = 0  # 1-5, onde 5 é máxima prioridade

    # Metadata
    data_mapeamento: str = ""
    status_contato: str = (
        "Não contatado"  # "Não contatado", "Contatado", "Reunião agendada", "Proposta enviada", "Cliente"
    )

    def __post_init__(self):
        if self.oportunidades is None:
            self.oportunidades = []
        if not self.data_mapeamento:
            self.data_mapeamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class SistemaMapeamento:
    """Sistema principal para gerenciar o mapeamento de estabelecimentos"""

    def __init__(self, arquivo_dados: str = "dados/estabelecimentos.json"):
        self.arquivo_dados = arquivo_dados
        self.estabelecimentos: List[Estabelecimento] = []
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega dados existentes do arquivo JSON"""
        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.estabelecimentos = [Estabelecimento(**e) for e in dados]
            print(f"✓ {len(self.estabelecimentos)} estabelecimentos carregados")
        except FileNotFoundError:
            print("→ Nenhum dado anterior encontrado. Iniciando nova base de dados.")
            self.estabelecimentos = []

    def salvar_dados(self):
        """Salva todos os estabelecimentos no arquivo JSON"""
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(e) for e in self.estabelecimentos],
                f,
                indent=2,
                ensure_ascii=False,
            )
        print(f"✓ {len(self.estabelecimentos)} estabelecimentos salvos")

    def adicionar_estabelecimento(self, estabelecimento: Estabelecimento):
        """Adiciona um novo estabelecimento"""
        self.estabelecimentos.append(estabelecimento)
        print(f"✓ '{estabelecimento.nome}' adicionado ao mapeamento")

    def buscar_por_nome(self, nome: str) -> List[Estabelecimento]:
        """Busca estabelecimentos por nome"""
        return [e for e in self.estabelecimentos if nome.lower() in e.nome.lower()]

    def buscar_por_bairro(self, bairro: str) -> List[Estabelecimento]:
        """Busca estabelecimentos por bairro"""
        return [e for e in self.estabelecimentos if bairro.lower() in e.bairro.lower()]

    def buscar_por_tipo(self, tipo: str) -> List[Estabelecimento]:
        """Busca estabelecimentos por tipo de negócio"""
        return [
            e for e in self.estabelecimentos if tipo.lower() in e.tipo_negocio.lower()
        ]

    def filtrar_sem_site(self) -> List[Estabelecimento]:
        """Retorna estabelecimentos sem site"""
        return [e for e in self.estabelecimentos if not e.tem_site]

    def filtrar_por_potencial(self, potencial: str) -> List[Estabelecimento]:
        """Filtra por potencial de cliente"""
        return [e for e in self.estabelecimentos if e.potencial_cliente == potencial]

    def filtrar_por_prioridade(
        self, prioridade_minima: int = 3
    ) -> List[Estabelecimento]:
        """Retorna estabelecimentos com prioridade >= valor especificado"""
        return sorted(
            [
                e
                for e in self.estabelecimentos
                if e.prioridade_contato >= prioridade_minima
            ],
            key=lambda x: x.prioridade_contato,
            reverse=True,
        )

    def exportar_para_csv(self, arquivo: str = "dados/estabelecimentos.csv"):
        """Exporta dados para CSV"""
        if not self.estabelecimentos:
            print("⚠ Nenhum estabelecimento para exportar")
            return

        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            campos = list(asdict(self.estabelecimentos[0]).keys())
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            for est in self.estabelecimentos:
                writer.writerow(asdict(est))

        print(f"✓ Dados exportados para {arquivo}")

    def gerar_relatorio(self, bairro: Optional[str] = None):
        """Gera relatório estatístico"""
        estabelecimentos = self.estabelecimentos
        if bairro:
            estabelecimentos = self.buscar_por_bairro(bairro)

        if not estabelecimentos:
            print("⚠ Nenhum estabelecimento encontrado")
            return

        total = len(estabelecimentos)
        sem_site = len([e for e in estabelecimentos if not e.tem_site])
        sem_instagram = len([e for e in estabelecimentos if not e.tem_instagram])
        alta_prioridade = len(
            [e for e in estabelecimentos if e.prioridade_contato >= 4]
        )

        print("\n" + "=" * 60)
        print(f"📊 RELATÓRIO DE MAPEAMENTO")
        if bairro:
            print(f"📍 Bairro: {bairro}")
        print("=" * 60)
        print(f"Total de estabelecimentos: {total}")
        print(f"Sem website: {sem_site} ({sem_site/total*100:.1f}%)")
        print(f"Sem Instagram: {sem_instagram} ({sem_instagram/total*100:.1f}%)")
        print(
            f"Alta prioridade de contato: {alta_prioridade} ({alta_prioridade/total*100:.1f}%)"
        )

        # Distribuição por tipo
        print("\n📋 Distribuição por tipo de negócio:")
        tipos = {}
        for e in estabelecimentos:
            tipos[e.tipo_negocio] = tipos.get(e.tipo_negocio, 0) + 1
        for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {tipo}: {count}")

        print("=" * 60 + "\n")

    def listar_proximos_contatos(self, limite: int = 10):
        """Lista os próximos estabelecimentos a serem contatados"""
        nao_contatados = [
            e for e in self.estabelecimentos if e.status_contato == "Não contatado"
        ]
        prioritarios = sorted(
            nao_contatados, key=lambda x: x.prioridade_contato, reverse=True
        )[:limite]

        print(f"\n🎯 TOP {limite} PRÓXIMOS CONTATOS\n")
        for i, est in enumerate(prioritarios, 1):
            print(f"{i}. {est.nome}")
            print(f"   📍 {est.endereco} - {est.bairro}")
            print(f"   🎯 Prioridade: {est.prioridade_contato}/5")
            print(f"   💡 Oportunidades: {', '.join(est.oportunidades[:3])}")
            print()


def exemplo_uso():
    """Exemplo de como usar o sistema"""

    # Inicializar sistema
    sistema = SistemaMapeamento()

    # Adicionar um estabelecimento de exemplo
    novo_estabelecimento = Estabelecimento(
        nome="Restaurante O Fado",
        endereco="Rua do Norte, 42",
        bairro="Bairro Alto",
        tipo_negocio=TipoNegocio.RESTAURANTE.value,
        tem_site=False,
        tem_instagram=True,
        url_instagram="@restauranteofado",
        tem_google_business=False,
        aparencia_estabelecimento="Tradicional, precisa modernização",
        movimento_aparente="Alto",
        nivel_presenca_digital=NivelPresencaDigital.BASICA.value,
        precisa_site=True,
        precisa_sistema_reservas=True,
        precisa_marketing_digital=True,
        oportunidades=[
            "Website profissional com sistema de reservas",
            "Google My Business para aumentar visibilidade",
            "Cardápio digital QR Code",
            "Integração com apps de delivery",
        ],
        observacoes="Restaurante sempre cheio, fila na porta. Donos parecem receptivos a melhorias.",
        potencial_cliente=PotencialCliente.ALTO.value,
        prioridade_contato=4,
    )

    sistema.adicionar_estabelecimento(novo_estabelecimento)
    sistema.salvar_dados()

    # Gerar relatório
    sistema.gerar_relatorio(bairro="Bairro Alto")

    # Listar próximos contatos
    sistema.listar_proximos_contatos(5)


if __name__ == "__main__":
    print("🗺️  Sistema de Mapeamento de Estabelecimentos - Lisboa")
    print("=" * 60)
    exemplo_uso()
