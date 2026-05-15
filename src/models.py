"""
📌 MÓDULO 1: MODELOS DE DADOS
================================

Este arquivo define as CLASSES (moldes de dados) do Ecometric.

Uma classe é como um "formulário" que padroniza como salvamos informações.
Por exemplo: todo veículo tem marca, modelo, ano, combustível, etc.

Benefícios:
- Organização: dados estruturados
- Reutilização: usar a mesma classe várias vezes
- Validação: garantir que os dados estejam corretos
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum


# ============================================================
# 1. TIPOS DE COMBUSTÍVEL
# ============================================================
class TipoCombustivel(Enum):
    """
    Um Enum é uma lista de valores pré-definidos.
    
    Exemplo: só existem alguns tipos de combustível.
    Ao invés de permitir qualquer string, limitamos às opções válidas.
    
    Vantagem: não há erros de digitação ou dados inválidos.
    """
    GASOLINA = "Gasolina"
    DIESEL = "Diesel"
    ELETRICO = "Elétrico"
    HIBRIDO = "Híbrido"
    GNV = "GNV"


# ============================================================
# 2. CATEGORIA DO VEÍCULO
# ============================================================
class CategoriaVeiculo(Enum):
    """
    Define categorias de veículos.
    Cada categoria tem diferentes fatores de emissão.
    
    Um SUV emite mais que um hatch, por exemplo.
    """
    HATCH = "Hatch"
    SEDAN = "Sedan"
    SUV = "SUV"
    PICKUP = "Pickup"
    ELETRICO = "Elétrico"


# ============================================================
# 3. CLASSE PRINCIPAL: VEÍCULO
# ============================================================
class Veiculo:
    """
    Representa um veículo no sistema.
    
    O __init__ é o "construtor" - quando você cria um Veiculo,
    ele precisa de certas informações.
    
    Exemplo de uso:
    >>> meu_carro = Veiculo(
    ...     brand="Jeep",
    ...     model="Compass",
    ...     year=2022,
    ...     fuel_type=TipoCombustivel.GASOLINA,
    ...     category=CategoriaVeiculo.SUV,
    ...     co2_per_minute=28
    ... )
    >>> print(meu_carro.descricao())
    """
    
    def __init__(
        self,
        brand: str,
        model: str,
        year: int,
        fuel_type: TipoCombustivel,
        category: CategoriaVeiculo,
        co2_per_minute: float
    ):
        """
        Inicializa um novo veículo.
        
        Args:
            brand (str): Marca do veículo (ex: "Jeep")
            model (str): Modelo do veículo (ex: "Compass")
            year (int): Ano de fabricação (ex: 2022)
            fuel_type (TipoCombustivel): Tipo de combustível
            category (CategoriaVeiculo): Categoria do veículo
            co2_per_minute (float): Gramas de CO2 emitido por minuto
        """
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel_type = fuel_type
        self.category = category
        self.co2_per_minute = co2_per_minute  # g/min
        self.data_criacao = datetime.now()
    
    def descricao(self) -> str:
        """
        Retorna uma descrição legível do veículo.
        
        Returns:
            str: Descrição formatada
            
        Exemplo:
            >>> v = Veiculo(...)
            >>> print(v.descricao())
            Jeep Compass (2022) - SUV - Gasolina - 28 g/min CO2
        """
        return (
            f"{self.brand} {self.model} ({self.year}) - "
            f"{self.category.value} - {self.fuel_type.value} - "
            f"{self.co2_per_minute} g/min CO2"
        )
    
    def para_dicionario(self) -> dict:
        """
        Converte o veículo para um dicionário (útil para MongoDB).
        
        Returns:
            dict: Representação do veículo em dicionário
        """
        return {
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "fuel_type": self.fuel_type.value,
            "category": self.category.value,
            "co2_per_minute": self.co2_per_minute,
            "data_criacao": self.data_criacao
        }


# ============================================================
# 4. TIPOS DE EVENTOS
# ============================================================
class TipoEvento(Enum):
    """
    Define os tipos de eventos que geram CO2 evitado.
    
    - PEDAGIO: Passagem em pedágio
    - ESTACIONAMENTO: Entrada em estacionamento
    """
    PEDAGIO = "Pedágio"
    ESTACIONAMENTO = "Estacionamento"


# ============================================================
# 5. CLASSE: EVENTO
# ============================================================
class Evento:
    """
    Representa um evento de uso (passagem em pedágio ou estacionamento).
    
    Cada evento tem:
    - tipo (pedágio ou estacionamento)
    - tempo economizado (em minutos)
    - timestamp (quando aconteceu)
    
    Exemplo:
    >>> evento = Evento(
    ...     tipo=TipoEvento.PEDAGIO,
    ...     tempo_economizado_min=4.5
    ... )
    """
    
    def __init__(
        self,
        tipo: TipoEvento,
        tempo_economizado_min: float,
        timestamp: Optional[datetime] = None
    ):
        """
        Inicializa um novo evento.
        
        Args:
            tipo (TipoEvento): Tipo de evento
            tempo_economizado_min (float): Tempo economizado em minutos
            timestamp (datetime, optional): Quando o evento ocorreu
        """
        self.tipo = tipo
        self.tempo_economizado_min = tempo_economizado_min
        self.timestamp = timestamp or datetime.now()
        self.co2_evitado_g = None  # Será calculado depois
        self.capcoin_gerado = None  # Será gerado depois
    
    def descricao(self) -> str:
        """Descrição do evento."""
        return (
            f"{self.tipo.value} - "
            f"Tempo: {self.tempo_economizado_min} min - "
            f"Data: {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
        )
    
    def para_dicionario(self) -> dict:
        """Converte o evento para dicionário."""
        return {
            "tipo": self.tipo.value,
            "tempo_economizado_min": self.tempo_economizado_min,
            "co2_evitado_g": self.co2_evitado_g,
            "capcoin_gerado": self.capcoin_gerado,
            "timestamp": self.timestamp
        }


# ============================================================
# 6. CLASSE: USUÁRIO
# ============================================================
class Usuario:
    """
    Representa um usuário no sistema Ecometric.
    
    Um usuário tem:
    - Um ou mais veículos
    - Um histórico de eventos
    - Pontuação de CapCoins
    - Dados de engajamento
    
    Exemplo:
    >>> user = Usuario(user_id="123", nome="João")
    >>> user.adicionar_veiculo(meu_carro)
    """
    
    def __init__(
        self,
        user_id: str,
        nome: str,
        email: Optional[str] = None
    ):
        """
        Inicializa um novo usuário.
        
        Args:
            user_id (str): ID único do usuário
            nome (str): Nome do usuário
            email (str, optional): Email do usuário
        """
        self.user_id = user_id
        self.nome = nome
        self.email = email
        self.veiculos: List[Veiculo] = []  # Lista de veículos
        self.eventos: List[Evento] = []  # Histórico de eventos
        self.capcoin_total = 0  # Total de CapCoins
        self.co2_total_evitado_g = 0  # Total de CO2 evitado
        self.data_criacao = datetime.now()
        self.streaks_ativos = 0  # Dias consecutivos ativos
    
    def adicionar_veiculo(self, veiculo: Veiculo):
        """
        Adiciona um veículo à lista do usuário.
        
        Args:
            veiculo (Veiculo): O veículo a adicionar
        """
        self.veiculos.append(veiculo)
        print(f"✅ Veículo '{veiculo.descricao()}' adicionado!")
    
    def adicionar_evento(self, evento: Evento):
        """
        Adiciona um evento ao histórico do usuário.
        
        Args:
            evento (Evento): O evento a adicionar
        """
        self.eventos.append(evento)
    
    def get_veiculo_principal(self) -> Optional[Veiculo]:
        """
        Retorna o primeiro veículo cadastrado (veículo principal).
        
        Returns:
            Veiculo: O veículo principal, ou None se não houver
        """
        return self.veiculos[0] if self.veiculos else None
    
    def resumo(self) -> str:
        """Retorna um resumo do perfil do usuário."""
        return (
            f"\n{'='*50}\n"
            f"👤 PERFIL DO USUÁRIO\n"
            f"{'='*50}\n"
            f"Nome: {self.nome}\n"
            f"ID: {self.user_id}\n"
            f"Veículos: {len(self.veiculos)}\n"
            f"Eventos: {len(self.eventos)}\n"
            f"CapCoins: {self.capcoin_total}\n"
            f"CO₂ Evitado: {self.co2_total_evitado_g:.0f}g\n"
            f"Streaks: {self.streaks_ativos}\n"
            f"{'='*50}\n"
        )
    
    def para_dicionario(self) -> dict:
        """Converte o usuário para dicionário (para MongoDB)."""
        return {
            "user_id": self.user_id,
            "nome": self.nome,
            "email": self.email,
            "capcoin_total": self.capcoin_total,
            "co2_total_evitado_g": self.co2_total_evitado_g,
            "streaks_ativos": self.streaks_ativos,
            "data_criacao": self.data_criacao,
            "numero_veiculos": len(self.veiculos),
            "numero_eventos": len(self.eventos)
        }


# ============================================================
# 7. CLASSE: RESGATE (Reward)
# ============================================================
class TipoResgate(Enum):
    """Define os tipos de resgates disponíveis."""
    DOACAO_AMBIENTAL = "Doação Ambiental"
    ECOBAG = "Ecobag Sustentável"
    LAVAGEM_ECOLOGICA = "Lavagem Ecológica"
    MOBILIDADE_VERDE = "Mobilidade Verde"
    ARVORE_PLANTADA = "Árvore Plantada"
    PRODUTOS_ORGANICOS = "Produtos Orgânicos"


class Resgate:
    """
    Representa um resgate de CapCoins por um prêmio.
    
    Exemplo:
    >>> resgate = Resgate(
    ...     tipo=TipoResgate.ARVORE_PLANTADA,
    ...     custo_capcoin=300
    ... )
    """
    
    def __init__(
        self,
        tipo: TipoResgate,
        custo_capcoin: int,
        descricao: str = ""
    ):
        """
        Inicializa um resgate.
        
        Args:
            tipo (TipoResgate): Tipo de prêmio
            custo_capcoin (int): Quanto custa em CapCoins
            descricao (str): Descrição do prêmio
        """
        self.tipo = tipo
        self.custo_capcoin = custo_capcoin
        self.descricao = descricao
        self.timestamp_criacao = datetime.now()
    
    def para_dicionario(self) -> dict:
        """Converte o resgate para dicionário."""
        return {
            "tipo": self.tipo.value,
            "custo_capcoin": self.custo_capcoin,
            "descricao": self.descricao,
            "timestamp_criacao": self.timestamp_criacao
        }


# ============================================================
# 8. CATÁLOGO DE RESGATES
# ============================================================
CATALOGO_RESGATES = {
    TipoResgate.DOACAO_AMBIENTAL: Resgate(
        tipo=TipoResgate.DOACAO_AMBIENTAL,
        custo_capcoin=100,
        descricao="Doação para projetos ambientais"
    ),
    TipoResgate.ECOBAG: Resgate(
        tipo=TipoResgate.ECOBAG,
        custo_capcoin=150,
        descricao="Ecobag reutilizável sustentável"
    ),
    TipoResgate.LAVAGEM_ECOLOGICA: Resgate(
        tipo=TipoResgate.LAVAGEM_ECOLOGICA,
        custo_capcoin=150,
        descricao="Voucher de lavagem ecológica"
    ),
    TipoResgate.MOBILIDADE_VERDE: Resgate(
        tipo=TipoResgate.MOBILIDADE_VERDE,
        custo_capcoin=200,
        descricao="Crédito de mobilidade verde"
    ),
    TipoResgate.ARVORE_PLANTADA: Resgate(
        tipo=TipoResgate.ARVORE_PLANTADA,
        custo_capcoin=300,
        descricao="Uma árvore plantada em seu nome"
    ),
    TipoResgate.PRODUTOS_ORGANICOS: Resgate(
        tipo=TipoResgate.PRODUTOS_ORGANICOS,
        custo_capcoin=400,
        descricao="Voucher de produtos orgânicos"
    ),
}


# ============================================================
# FIM DO MÓDULO 1
# ============================================================
# 
# RESUMO: Criamos as classes que definem a estrutura de dados
# do Ecometric: Veículo, Evento, Usuário e Resgate.
#
# No próximo módulo, vamos criar a LÓGICA que usa essas classes
# para calcular CO₂ evitado e gerar CapCoins.
#
# ============================================================