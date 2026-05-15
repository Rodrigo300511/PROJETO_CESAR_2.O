"""
🪙 MÓDULO 3: ENGINE DE GAMIFICAÇÃO (CapCoins)
==============================================

Este módulo implementa o sistema de RECOMPENSAS do Ecometric.

Conceito:
  Convertemos CO₂ evitado em uma moeda virtual: CAPCOIN

Regras:
  - Pedágio: +5 CapCoins
  - Estacionamento: +3 CapCoins
  - Bônus mensal: até +100 CapCoins
  - Streak (uso consecutivo): até +80 CapCoins
  - Engajamento: até +50 CapCoins

A ideia é GAMIFICAR o comportamento ambiental,
tornando divertido economizar CO₂.
"""

from src.models import Evento, Usuario, TipoEvento, TipoResgate, CATALOGO_RESGATES
from src.config import (
    CAPCOIN_POR_PEDAGIO,
    CAPCOIN_POR_ESTACIONAMENTO,
    CAPCOIN_BONUS_MENSAL,
    CAPCOIN_BONUS_STREAK,
    CAPCOIN_BONUS_ENGAJAMENTO,
    DIAS_MINIMOS_PARA_INDICACAO
)
from datetime import datetime, timedelta


class GamificationEngine:
    """
    Engine responsável por gerenciar a gamificação (CapCoins).
    
    Responsabilidades:
    1. Calcular CapCoins por evento
    2. Aplicar bônus (streak, engajamento, mensal)
    3. Gerenciar resgate de prêmios
    4. Validar regras anti-fraude
    5. Gerar relatórios de pontuação
    
    Exemplo de uso:
    >>> game = GamificationEngine()
    >>> usuario = Usuario("001", "João")
    >>> evento = Evento(TipoEvento.PEDAGIO, 4.5)
    >>> capcoin = game.calcular_capcoin(evento)
    >>> print(f"Ganhou {capcoin} CapCoins!")
    Ganhou 5 CapCoins!
    """
    
    def __init__(self):
        """Inicializa o engine de gamificação."""
        self.historico_transacoes = []  # Histórico de movimentações
        self.resgates_pendentes = {}  # Resgates aguardando aprovação
        print("✅ Engine de Gamificação iniciado")
    
    # ========================================================
    # 1. CÁLCULO PRINCIPAL DE CAPCOIN
    # ========================================================
    
    def calcular_capcoin(self, evento: Evento) -> int:
        """
        Calcula quantos CapCoins são ganhos em um evento.
        
        Regra:
            - Pedágio: +5 CapCoins
            - Estacionamento: +3 CapCoins
        
        Args:
            evento (Evento): O evento realizado
        
        Returns:
            int: Quantidade de CapCoins ganhos
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> evento_pedagio = Evento(TipoEvento.PEDAGIO, 4.5)
            >>> capcoin = game.calcular_capcoin(evento_pedagio)
            >>> print(capcoin)
            5
        
        ⚠️ NOTA: Este é o cálculo BASE. Os bônus são aplicados depois.
        """
        # Define quantos CapCoins por tipo de evento
        if evento.tipo == TipoEvento.PEDAGIO:
            capcoin = CAPCOIN_POR_PEDAGIO
        elif evento.tipo == TipoEvento.ESTACIONAMENTO:
            capcoin = CAPCOIN_POR_ESTACIONAMENTO
        else:
            raise ValueError(f"❌ Tipo de evento desconhecido: {evento.tipo}")
        
        # Armazena no evento
        evento.capcoin_gerado = capcoin
        
        # Registra no histórico
        self._registrar_transacao(
            tipo="GANHO",
            quantidade=capcoin,
            motivo=f"Evento: {evento.tipo.value}",
            timestamp=evento.timestamp
        )
        
        return capcoin
    
    # ========================================================
    # 2. BÔNUS (Multiplicadores)
    # ========================================================
    
    def calcular_bonus_streak(self, usuario: Usuario, dias_consecutivos: int) -> int:
        """
        Calcula bônus por STREAK (uso consecutivo).
        
        Lógica:
            - Máximo de +80 CapCoins
            - Proporcional aos dias de uso consecutivo
        
        Args:
            usuario (Usuario): O usuário
            dias_consecutivos (int): Quantos dias seguidos de uso
        
        Returns:
            int: Bônus em CapCoins
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> user = Usuario("001", "João")
            >>> bonus = game.calcular_bonus_streak(user, 7)
            >>> print(f"Bônus streak: +{bonus} CapCoins")
            Bônus streak: +10 CapCoins
        
        💡 Quanto mais dias, maior o bônus (até o máximo de 80).
        """
        # Valida dias consecutivos
        if dias_consecutivos < 0:
            return 0
        
        # Cálculo proporcional
        # 30 dias = 80 CapCoins (máximo)
        # X dias = ? CapCoins
        bonus = int((dias_consecutivos / 30) * CAPCOIN_BONUS_STREAK)
        
        # Limita ao máximo
        bonus = min(bonus, CAPCOIN_BONUS_STREAK)
        
        self._registrar_transacao(
            tipo="BONUS",
            quantidade=bonus,
            motivo=f"Streak: {dias_consecutivos} dias"
        )
        
        return bonus
    
    def calcular_bonus_engajamento(
        self,
        numero_eventos_mes: int
    ) -> int:
        """
        Calcula bônus por ENGAJAMENTO (número de eventos no mês).
        
        Lógica:
            - Quanto mais eventos, maior o bônus
            - Máximo de +50 CapCoins por mês
        
        Args:
            numero_eventos_mes (int): Quantos eventos no mês
        
        Returns:
            int: Bônus em CapCoins
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> bonus = game.calcular_bonus_engajamento(20)
            >>> print(f"Bônus engajamento: +{bonus} CapCoins")
            Bônus engajamento: +50 CapCoins
        
        💡 Objetivo: incentivar uso frequente (20 eventos/mês = bônus máximo).
        """
        # 20 eventos = 50 CapCoins (máximo)
        # X eventos = ? CapCoins
        bonus = int((numero_eventos_mes / 20) * CAPCOIN_BONUS_ENGAJAMENTO)
        
        # Limita ao máximo
        bonus = min(bonus, CAPCOIN_BONUS_ENGAJAMENTO)
        
        self._registrar_transacao(
            tipo="BONUS",
            quantidade=bonus,
            motivo=f"Engajamento: {numero_eventos_mes} eventos"
        )
        
        return bonus
    
    def calcular_bonus_mensal(self, usuario: Usuario) -> int:
        """
        Calcula bônus mensal automático.
        
        Lógica:
            - Usuários ativos recebem até +100 CapCoins por mês
            - Depende do número de eventos no mês
        
        Args:
            usuario (Usuario): O usuário
        
        Returns:
            int: Bônus mensal em CapCoins
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> user = Usuario("001", "João")
            >>> bonus = game.calcular_bonus_mensal(user)
            >>> print(f"Bônus mensal: +{bonus} CapCoins")
            Bônus mensal: +100 CapCoins
        """
        # Conta eventos do mês atual
        agora = datetime.now()
        eventos_este_mes = [
            e for e in usuario.eventos
            if e.timestamp.month == agora.month
            and e.timestamp.year == agora.year
        ]
        
        # Se teve eventos, recebe bônus
        if eventos_este_mes:
            bonus = CAPCOIN_BONUS_MENSAL
        else:
            bonus = 0
        
        self._registrar_transacao(
            tipo="BONUS",
            quantidade=bonus,
            motivo=f"Bônus mensal ({len(eventos_este_mes)} eventos)"
        )
        
        return bonus
    
    # ========================================================
    # 3. CÁLCULO TOTAL (Base + Bônus)
    # ========================================================
    
    def calcular_capcoin_total_com_bonus(
        self,
        evento: Evento,
        usuario: Usuario,
        dias_streak: int = 0
    ) -> dict:
        """
        Calcula os CapCoins TOTAIS incluindo todos os bônus.
        
        FÓRMULA:
            Total = Base + Bonus_Streak + Bonus_Engajamento
        
        Args:
            evento (Evento): O evento realizado
            usuario (Usuario): O usuário
            dias_streak (int): Dias consecutivos de uso
        
        Returns:
            dict: Breakdown dos CapCoins com detalhes
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> resultado = game.calcular_capcoin_total_com_bonus(
            ...     evento, usuario, dias_streak=7
            ... )
            >>> print(resultado)
            {
                'base': 5,
                'bonus_streak': 10,
                'bonus_engajamento': 15,
                'total': 30
            }
        """
        # Base
        base = self.calcular_capcoin(evento)
        
        # Bônus
        bonus_streak = self.calcular_bonus_streak(usuario, dias_streak)
        bonus_engajamento = self.calcular_bonus_engajamento(len(usuario.eventos))
        
        # Total
        total = base + bonus_streak + bonus_engajamento
        
        resultado = {
            "base": base,
            "bonus_streak": bonus_streak,
            "bonus_engajamento": bonus_engajamento,
            "total": total,
            "descricao": f"Base({base}) + Streak({bonus_streak}) + Engajamento({bonus_engajamento}) = {total}"
        }
        
        return resultado
    
    # ========================================================
    # 4. GERENCIAMENTO DE SALDO
    # ========================================================
    
    def adicionar_capcoin(
        self,
        usuario: Usuario,
        quantidade: int,
        motivo: str = ""
    ):
        """
        Adiciona CapCoins ao saldo do usuário.
        
        Args:
            usuario (Usuario): O usuário
            quantidade (int): Quantos CapCoins adicionar
            motivo (str): Por que está adicionando
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> user = Usuario("001", "João")
            >>> game.adicionar_capcoin(user, 50, "Prêmio especial")
            >>> print(user.capcoin_total)
            50
        """
        if quantidade < 0:
            raise ValueError("❌ Quantidade não pode ser negativa!")
        
        usuario.capcoin_total += quantidade
        
        self._registrar_transacao(
            tipo="CREDITO",
            quantidade=quantidade,
            motivo=motivo,
            usuario_id=usuario.user_id
        )
        
        print(f"✅ {usuario.nome} recebeu +{quantidade} CapCoins ({motivo})")
    
    def remover_capcoin(
        self,
        usuario: Usuario,
        quantidade: int,
        motivo: str = ""
    ) -> bool:
        """
        Remove CapCoins do saldo do usuário (para resgate).
        
        Args:
            usuario (Usuario): O usuário
            quantidade (int): Quantos CapCoins remover
            motivo (str): Por que está removendo (ex: "Resgate de árvore")
        
        Returns:
            bool: True se bem-sucedido, False se saldo insuficiente
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> sucesso = game.remover_capcoin(user, 100, "Árvore plantada")
            >>> if sucesso:
            ...     print("Resgate realizado!")
        """
        # Valida saldo
        if usuario.capcoin_total < quantidade:
            print(f"❌ Saldo insuficiente! Tem {usuario.capcoin_total}, precisa de {quantidade}")
            return False
        
        usuario.capcoin_total -= quantidade
        
        self._registrar_transacao(
            tipo="DEBITO",
            quantidade=quantidade,
            motivo=motivo,
            usuario_id=usuario.user_id
        )
        
        print(f"✅ {usuario.nome} resgatou {quantidade} CapCoins ({motivo})")
        return True
    
    # ========================================================
    # 5. RESGATE DE PRÊMIOS
    # ========================================================
    
    def resgatar_premio(
        self,
        usuario: Usuario,
        tipo_resgate: TipoResgate
    ) -> bool:
        """
        Permite ao usuário resgatar um prêmio usando seus CapCoins.
        
        Args:
            usuario (Usuario): O usuário
            tipo_resgate (TipoResgate): Qual prêmio deseja
        
        Returns:
            bool: True se bem-sucedido
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> sucesso = game.resgatar_premio(user, TipoResgate.ARVORE_PLANTADA)
            >>> if sucesso:
            ...     print("Parabéns! Uma árvore foi plantada em seu nome!")
        """
        # Obtém o prêmio do catálogo
        if tipo_resgate not in CATALOGO_RESGATES:
            print(f"❌ Prêmio não encontrado: {tipo_resgate}")
            return False
        
        premio = CATALOGO_RESGATES[tipo_resgate]
        custo = premio.custo_capcoin
        
        # Tenta remover CapCoins
        if not self.remover_capcoin(usuario, custo, f"Resgate: {tipo_resgate.value}"):
            return False
        
        # Sucesso!
        self.resgates_pendentes[usuario.user_id] = {
            "tipo": tipo_resgate,
            "data_resgate": datetime.now(),
            "status": "pendente"
        }
        
        print(f"🎁 {usuario.nome} resgatou: {tipo_resgate.value}")
        return True
    
    def listar_premios_disponiveis(self, usuario: Usuario) -> dict:
        """
        Lista todos os prêmios disponíveis e se o usuário pode resgatá-los.
        
        Args:
            usuario (Usuario): O usuário
        
        Returns:
            dict: Lista de prêmios com status de disponibilidade
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> premios = game.listar_premios_disponiveis(user)
            >>> for tipo, info in premios.items():
            ...     print(f"{tipo.value}: {info['custo']} CapCoins - "
            ...           f"{'✅ Disponível' if info['disponivel'] else '❌ Indisponível'}")
        """
        premios_info = {}
        
        for tipo, premio in CATALOGO_RESGATES.items():
            premios_info[tipo] = {
                "nome": tipo.value,
                "descricao": premio.descricao,
                "custo": premio.custo_capcoin,
                "disponivel": usuario.capcoin_total >= premio.custo_capcoin,
                "saldo_faltante": max(0, premio.custo_capcoin - usuario.capcoin_total)
            }
        
        return premios_info
    
    # ========================================================
    # 6. REGRAS ANTI-FRAUDE
    # ========================================================
    
    def validar_evento(
        self,
        usuario: Usuario,
        novo_evento: Evento
    ) -> bool:
        """
        Valida se um evento pode ser registrado (anti-fraude).
        
        Regras:
            1. Mínimo de 1 minuto entre eventos
            2. Tempo máximo razoável (ex: max 60 min por pedágio)
        
        Args:
            usuario (Usuario): O usuário
            novo_evento (Evento): O novo evento a validar
        
        Returns:
            bool: True se evento é válido
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> is_valid = game.validar_evento(user, novo_evento)
            >>> if is_valid:
            ...     print("Evento válido!")
        """
        if not usuario.eventos:
            # Primeiro evento sempre é válido
            return True
        
        # Pega o último evento
        ultimo = usuario.eventos[-1]
        
        # Calcula diferença de tempo
        diferenca = novo_evento.timestamp - ultimo.timestamp
        segundos_diferenca = diferenca.total_seconds()
        
        # Regra 1: Mínimo de 60 segundos (1 minuto) entre eventos
        if segundos_diferenca < 60:
            print(f"❌ Eventos muito próximos! Aguarde pelo menos 1 minuto.")
            return False
        
        # Regra 2: Tempo economizado não deve ser absurdo
        if novo_evento.tempo_economizado_min > 60:
            print(f"❌ Tempo economizado muito alto! Máximo: 60 minutos.")
            return False
        
        return True
    
    # ========================================================
    # 7. HISTÓRICO E RELATÓRIOS
    # ========================================================
    
    def _registrar_transacao(
        self,
        tipo: str,
        quantidade: int,
        motivo: str = "",
        usuario_id: str = "",
        timestamp: datetime = None
    ):
        """
        Registra uma transação no histórico.
        
        Args:
            tipo (str): GANHO, BONUS, CREDITO, DEBITO
            quantidade (int): Quantidade de CapCoins
            motivo (str): Por quê
            usuario_id (str): Qual usuário
            timestamp (datetime): Quando
        """
        self.historico_transacoes.append({
            "tipo": tipo,
            "quantidade": quantidade,
            "motivo": motivo,
            "usuario_id": usuario_id,
            "timestamp": timestamp or datetime.now()
        })
    
    def obter_historico_usuario(self, usuario: Usuario) -> list:
        """
        Retorna o histórico de transações de um usuário.
        
        Args:
            usuario (Usuario): O usuário
        
        Returns:
            list: Histórico de transações
        """
        return [
            t for t in self.historico_transacoes
            if t["usuario_id"] == usuario.user_id
        ]
    
    def gerar_relatorio(self, usuario: Usuario) -> dict:
        """
        Gera um relatório completo de gamificação do usuário.
        
        Args:
            usuario (Usuario): O usuário
        
        Returns:
            dict: Relatório detalhado
        
        Exemplo:
            >>> game = GamificationEngine()
            >>> relatorio = game.gerar_relatorio(user)
            >>> print(relatorio["saldo_atual"])
            150
        """
        return {
            "usuario": usuario.nome,
            "saldo_atual": usuario.capcoin_total,
            "total_ganho": sum(
                t["quantidade"] for t in self.obter_historico_usuario(usuario)
                if t["tipo"] in ["GANHO", "BONUS", "CREDITO"]
            ),
            "total_resgatado": sum(
                t["quantidade"] for t in self.obter_historico_usuario(usuario)
                if t["tipo"] == "DEBITO"
            ),
            "numero_eventos": len(usuario.eventos),
            "premios_resgatados": len(
                [r for r in self.resgates_pendentes.values()
                 if r["status"] == "completado"]
            ),
        }


# ============================================================
# FIM DO MÓDULO 3
# ============================================================