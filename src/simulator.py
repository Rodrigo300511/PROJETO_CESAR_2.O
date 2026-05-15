"""
🎮 MÓDULO 4: SIMULADOR
======================

Este módulo simula eventos reais do Ecometric.

Funcionalidade:
  - Criar usuários
  - Simular múltiplos eventos (pedágio/estacionamento)
  - Calcular CO₂ e CapCoins automaticamente
  - Gerar relatórios

Objetivo: Testar o sistema sem depender da API Taggy.
"""

import random
from datetime import datetime, timedelta
from src.models import (
    Veiculo, Evento, Usuario, TipoCombustivel, CategoriaVeiculo,
    TipoEvento, TipoResgate
)
from src.emission_engine import EmissionEngine
from src.gamification_engine import GamificationEngine
from src.config import (
    TEMPO_MEDIO_PEDAGIO,
    TEMPO_MEDIO_ESTACIONAMENTO,
    EVENTOS_SIMULACAO_POR_MES,
    DIAS_SIMULACAO
)


class Simulador:
    """
    Simula o comportamento do Ecometric.
    
    Responsabilidades:
    1. Criar usuários e veículos
    2. Gerar eventos simulados
    3. Processar eventos (calcular CO₂ e CapCoins)
    4. Gerar relatórios
    5. Permitir resgate de prêmios
    
    Exemplo de uso:
    >>> sim = Simulador()
    >>> user = sim.criar_usuario("001", "João Silva")
    >>> veiculo = sim.adicionar_veiculo(user, "Jeep", "Compass", 2022, ...)
    >>> sim.simular_eventos(user, 20)  # 20 eventos aleatórios
    >>> sim.relatorio_final(user)
    """
    
    def __init__(self):
        """Inicializa o simulador com os engines."""
        self.emission_engine = EmissionEngine()
        self.gamification_engine = GamificationEngine()
        self.usuarios = {}  # Dicionário de usuários
        print("✅ Simulador inicializado")
    
    # ========================================================
    # 1. CRIAÇÃO DE USUÁRIOS
    # ========================================================
    
    def criar_usuario(self, user_id: str, nome: str, email: str = "") -> Usuario:
        """
        Cria um novo usuário.
        
        Args:
            user_id (str): ID único
            nome (str): Nome do usuário
            email (str): Email (opcional)
        
        Returns:
            Usuario: Novo usuário criado
        
        Exemplo:
            >>> sim = Simulador()
            >>> user = sim.criar_usuario("001", "João Silva")
            >>> print(user.nome)
            João Silva
        """
        usuario = Usuario(user_id=user_id, nome=nome, email=email)
        self.usuarios[user_id] = usuario
        print(f"✅ Usuário criado: {nome}")
        return usuario
    
    # ========================================================
    # 2. CRIAÇÃO DE VEÍCULOS
    # ========================================================
    
    def adicionar_veiculo(
        self,
        usuario: Usuario,
        brand: str,
        model: str,
        year: int,
        fuel_type: TipoCombustivel,
        category: CategoriaVeiculo,
        co2_per_minute: float
    ) -> Veiculo:
        """
        Adiciona um veículo ao usuário.
        
        Args:
            usuario (Usuario): O usuário dono do veículo
            brand (str): Marca (ex: "Jeep")
            model (str): Modelo (ex: "Compass")
            year (int): Ano (ex: 2022)
            fuel_type (TipoCombustivel): Tipo de combustível
            category (CategoriaVeiculo): Categoria (ex: "SUV")
            co2_per_minute (float): Emissão em g/min
        
        Returns:
            Veiculo: Novo veículo
        
        Exemplo:
            >>> user = sim.criar_usuario("001", "João")
            >>> veiculo = sim.adicionar_veiculo(
            ...     user,
            ...     brand="Jeep",
            ...     model="Compass",
            ...     year=2022,
            ...     fuel_type=TipoCombustivel.GASOLINA,
            ...     category=CategoriaVeiculo.SUV,
            ...     co2_per_minute=28
            ... )
        """
        veiculo = Veiculo(
            brand=brand,
            model=model,
            year=year,
            fuel_type=fuel_type,
            category=category,
            co2_per_minute=co2_per_minute
        )
        
        usuario.adicionar_veiculo(veiculo)
        return veiculo
    
    # ========================================================
    # 3. SIMULAÇÃO DE EVENTOS
    # ========================================================
    
    def simular_evento_aleatorio(
        self,
        usuario: Usuario,
        veiculo: Veiculo,
        timestamp: datetime = None
    ) -> Evento:
        """
        Simula um evento aleatório (pedágio ou estacionamento).
        
        Args:
            usuario (Usuario): Usuário
            veiculo (Veiculo): Veículo usado
            timestamp (datetime): Quando ocorreu (opcional)
        
        Returns:
            Evento: Evento simulado e processado
        
        Exemplo:
            >>> sim = Simulador()
            >>> user = sim.criar_usuario("001", "João")
            >>> veiculo = sim.adicionar_veiculo(user, ...)
            >>> evento = sim.simular_evento_aleatorio(user, veiculo)
            >>> print(f"CO₂ evitado: {evento.co2_evitado_g}g")
            CO₂ evitado: 126.0g
        """
        # Escolhe aleatoriamente entre pedágio ou estacionamento
        tipo = random.choice([TipoEvento.PEDAGIO, TipoEvento.ESTACIONAMENTO])
        
        # Define tempo economizado baseado no tipo
        if tipo == TipoEvento.PEDAGIO:
            # Pedágio: 3 a 6 minutos (média 4.5)
            tempo_min = random.uniform(3, 6)
        else:
            # Estacionamento: 10 a 20 minutos (média 15)
            tempo_min = random.uniform(10, 20)
        
        # Cria o evento
        evento = Evento(
            tipo=tipo,
            tempo_economizado_min=tempo_min,
            timestamp=timestamp or datetime.now()
        )
        
        # Valida (anti-fraude)
        if not self.gamification_engine.validar_evento(usuario, evento):
            print("⚠️ Evento rejeitado por validação anti-fraude")
            return None
        
        # Calcula CO₂
        co2_evitado = self.emission_engine.calcular_co2_evitado(evento, veiculo)
        
        # Calcula CapCoins
        capcoin = self.gamification_engine.calcular_capcoin(evento)
        
        # Adiciona ao usuário
        usuario.adicionar_evento(evento)
        self.gamification_engine.adicionar_capcoin(
            usuario,
            capcoin,
            f"Evento: {evento.tipo.value}"
        )
        
        # Atualiza totalizadores do usuário
        usuario.co2_total_evitado_g += co2_evitado
        
        print(
            f"📍 {evento.tipo.value}: "
            f"{tempo_min:.1f}min → {co2_evitado:.0f}g CO₂ → +{capcoin} CapCoins"
        )
        
        return evento
    
    def simular_eventos_mensais(
        self,
        usuario: Usuario,
        veiculo: Veiculo,
        numero_eventos: int = None,
        data_inicio: datetime = None
    ) -> list:
        """
        Simula múltiplos eventos distribuídos ao longo do mês.
        
        Args:
            usuario (Usuario): Usuário
            veiculo (Veiculo): Veículo
            numero_eventos (int): Quantos eventos simular (padrão: 20)
            data_inicio (datetime): Data inicial (padrão: hoje)
        
        Returns:
            list: Lista de eventos criados
        
        Exemplo:
            >>> sim = Simulador()
            >>> user = sim.criar_usuario("001", "João")
            >>> veiculo = sim.adicionar_veiculo(user, ...)
            >>> eventos = sim.simular_eventos_mensais(user, veiculo, 20)
            >>> print(f"{len(eventos)} eventos simulados")
            20 eventos simulados
        """
        numero_eventos = numero_eventos or EVENTOS_SIMULACAO_POR_MES
        data_inicio = data_inicio or datetime.now()
        
        eventos = []
        
        print(f"\n🎮 Simulando {numero_eventos} eventos para {usuario.nome}...")
        print("=" * 60)
        
        # Distribui eventos ao longo de 30 dias
        for i in range(numero_eventos):
            # Escolhe um dia aleatório
            dias_offset = random.randint(0, 29)
            
            # Escolhe uma hora aleatória do dia
            hora = random.randint(6, 22)  # Entre 6h e 22h
            minuto = random.randint(0, 59)
            
            # Cria timestamp
            timestamp = data_inicio + timedelta(
                days=dias_offset,
                hours=hora,
                minutes=minuto
            )
            
            # Simula o evento
            evento = self.simular_evento_aleatorio(usuario, veiculo, timestamp)
            
            if evento:
                eventos.append(evento)
            
            # Pequeno delay para não parecer artificial
            # (em produção, não teríamos isso)
        
        print("=" * 60)
        return eventos
    
    # ========================================================
    # 4. PROCESSAMENTO E CÁLCULOS
    # ========================================================
    
    def processar_resgate(
        self,
        usuario: Usuario,
        tipo_resgate: TipoResgate
    ) -> bool:
        """
        Processa o resgate de um prêmio.
        
        Args:
            usuario (Usuario): Usuário
            tipo_resgate (TipoResgate): Qual prêmio
        
        Returns:
            bool: True se bem-sucedido
        
        Exemplo:
            >>> sim = Simulador()
            >>> sucesso = sim.processar_resgate(user, TipoResgate.ARVORE_PLANTADA)
            >>> if sucesso:
            ...     print("🎁 Prêmio resgatado!")
        """
        return self.gamification_engine.resgatar_premio(usuario, tipo_resgate)
    
    # ========================================================
    # 5. RELATÓRIOS
    # ========================================================
    
    def relatorio_usuario(self, usuario: Usuario) -> None:
        """
        Imprime um relatório completo do usuário.
        
        Args:
            usuario (Usuario): O usuário
        
        Exemplo:
            >>> sim = Simulador()
            >>> sim.relatorio_usuario(user)
        """
        print(usuario.resumo())
        
        # Relatório de emissões
        relatorio_emissao = self.emission_engine.gerar_relatorio(
            usuario.eventos,
            usuario.get_veiculo_principal()
        )
        
        print("\n🌍 IMPACTO AMBIENTAL")
        print("=" * 60)
        print(f"Veículo: {relatorio_emissao['veiculo']}")
        print(f"Eventos: {relatorio_emissao['numero_eventos']}")
        print(f"Tempo economizado: {relatorio_emissao['tempo_total_economizado_horas']:.1f} horas")
        print(f"CO₂ evitado: {relatorio_emissao['co2_total_evitado_kg']:.3f} kg")
        print(f"Equivalente a: {relatorio_emissao['equivalente_arvores']:.2f} árvores/ano")
        print(f"              ou {relatorio_emissao['equivalente_km']:.1f} km não rodados")
        
        # Relatório de gamificação
        relatorio_game = self.gamification_engine.gerar_relatorio(usuario)
        
        print("\n🪙 GAMIFICAÇÃO")
        print("=" * 60)
        print(f"Saldo atual: {relatorio_game['saldo_atual']} CapCoins")
        print(f"Total ganho: {relatorio_game['total_ganho']} CapCoins")
        print(f"Total resgatado: {relatorio_game['total_resgatado']} CapCoins")
        print(f"Prêmios resgatados: {relatorio_game['premios_resgatados']}")
        
        # Prêmios disponíveis
        print("\n🎁 PRÊMIOS DISPONÍVEIS")
        print("=" * 60)
        premios = self.gamification_engine.listar_premios_disponiveis(usuario)
        for tipo, info in premios.items():
            status = "✅" if info['disponivel'] else "❌"
            print(
                f"{status} {info['nome']}: {info['custo']} CapCoins "
                f"({info['descricao']})"
            )
            if not info['disponivel']:
                print(f"   Faltam: {info['saldo_faltante']} CapCoins")
    
    def relatorio_todos_usuarios(self) -> None:
        """
        Imprime relatório resumido de todos os usuários.
        
        Exemplo:
            >>> sim = Simulador()
            >>> sim.relatorio_todos_usuarios()
        """
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO GERAL - TODOS OS USUÁRIOS")
        print("=" * 80)
        
        if not self.usuarios:
            print("❌ Nenhum usuário cadastrado")
            return
        
        # Cabeçalho da tabela
        print(
            f"{'Nome':<20} {'Eventos':<10} {'CO₂ (kg)':<12} "
            f"{'CapCoins':<12} {'Prêmios':<10}"
        )
        print("-" * 80)
        
        # Linhas da tabela
        for usuario in self.usuarios.values():
            co2_kg = usuario.co2_total_evitado_g / 1000
            num_eventos = len(usuario.eventos)
            
            print(
                f"{usuario.nome:<20} {num_eventos:<10} {co2_kg:<12.3f} "
                f"{usuario.capcoin_total:<12} {0:<10}"
            )
        
        # Total geral
        print("-" * 80)
        total_usuarios = len(self.usuarios)
        total_co2_g = sum(u.co2_total_evitado_g for u in self.usuarios.values())
        total_capcoin = sum(u.capcoin_total for u in self.usuarios.values())
        
        print(
            f"{'TOTAL':<20} {'':<10} {total_co2_g/1000:<12.3f} "
            f"{total_capcoin:<12}"
        )
        print("=" * 80)
        
        # Estatísticas
        print("\n📈 ESTATÍSTICAS")
        print(f"Usuários ativos: {total_usuarios}")
        print(f"CO₂ total evitado: {total_co2_g/1000:.3f} kg")
        print(f"CapCoins totais emitidos: {total_capcoin}")
        print(f"Média por usuário: {total_capcoin/total_usuarios:.0f} CapCoins")


# ============================================================
# FIM DO MÓDULO 4
# ============================================================