"""
🌍 MÓDULO 2: ENGINE DE EMISSÕES
================================

Este módulo contém toda a LÓGICA para calcular CO₂ evitado.

Conceito:
  CO₂ EVITADO = Tempo economizado (min) × Taxa de emissão (g/min)

Exemplos:
  1. Pedágio com fila de 4.5 minutos
     - Carro SUV: 28 g/min
     - CO₂ evitado: 4.5 × 28 = 126g

  2. Estacionamento com espera de 15 minutos
     - Carro Sedan: 24 g/min
     - CO₂ evitado: 15 × 24 = 360g
"""

from src.models import Veiculo, Evento, TipoEvento
from src.config import FATORES_EMISSAO_PADRAO
import math


class EmissionEngine:
    """
    Engine responsável por calcular emissões de CO₂.
    
    Responsabilidades:
    1. Calcular CO₂ evitado para um evento
    2. Calcular CO₂ total por período
    3. Validar dados de emissão
    4. Converter unidades (g para kg, minutos para horas, etc)
    
    Exemplo de uso:
    >>> engine = EmissionEngine()
    >>> evento = Evento(tipo=TipoEvento.PEDAGIO, tempo_economizado_min=4.5)
    >>> veiculo = Veiculo(..., co2_per_minute=28)
    >>> co2 = engine.calcular_co2_evitado(evento, veiculo)
    >>> print(f"CO₂ evitado: {co2}g")
    CO₂ evitado: 126.0g
    """
    
    def __init__(self):
        """Inicializa o engine de emissões."""
        self.historico_calculos = []  # Mantém registro de cálculos
        print("✅ Engine de Emissões iniciado")
    
    # ========================================================
    # 1. CÁLCULO PRINCIPAL DE CO₂
    # ========================================================
    
    def calcular_co2_evitado(
        self,
        evento: Evento,
        veiculo: Veiculo
    ) -> float:
        """
        Calcula a quantidade de CO₂ evitado em um evento.
        
        FÓRMULA:
            CO₂ evitado (g) = Tempo economizado (min) × Emissão do veículo (g/min)
        
        Args:
            evento (Evento): O evento de uso (pedágio/estacionamento)
            veiculo (Veiculo): O veículo utilizado
        
        Returns:
            float: Quantidade de CO₂ evitado em gramas
        
        Exemplo:
            >>> motor = EmissionEngine()
            >>> evento = Evento(TipoEvento.PEDAGIO, 4.5)
            >>> carro = Veiculo("Jeep", "Compass", 2022, ..., co2_per_minute=28)
            >>> co2 = motor.calcular_co2_evitado(evento, carro)
            >>> print(co2)
            126.0
        
        ⚠️ VALIDAÇÃO: Antes de calcular, verifica se os dados são válidos.
        """
        # Validação 1: Tempo deve ser positivo
        if evento.tempo_economizado_min <= 0:
            raise ValueError(
                f"❌ Tempo economizado deve ser > 0. Recebido: {evento.tempo_economizado_min}"
            )
        
        # Validação 2: Emissão deve ser >= 0
        if veiculo.co2_per_minute < 0:
            raise ValueError(
                f"❌ Emissão não pode ser negativa. Recebido: {veiculo.co2_per_minute}"
            )
        
        # ✅ Cálculo
        co2_evitado_g = evento.tempo_economizado_min * veiculo.co2_per_minute
        
        # Armazena no histórico (para auditoria)
        self.historico_calculos.append({
            "tipo_evento": evento.tipo.value,
            "tempo_min": evento.tempo_economizado_min,
            "co2_per_min": veiculo.co2_per_minute,
            "resultado_g": co2_evitado_g,
            "veiculo": f"{veiculo.brand} {veiculo.model}"
        })
        
        # Armazena também no evento
        evento.co2_evitado_g = co2_evitado_g
        
        return co2_evitado_g
    
    # ========================================================
    # 2. CONVERSÕES DE UNIDADES
    # ========================================================
    
    @staticmethod
    def converter_g_para_kg(gramas: float) -> float:
        """
        Converte gramas para quilogramas.
        
        Args:
            gramas (float): Valor em gramas
        
        Returns:
            float: Valor em quilogramas
        
        Exemplo:
            >>> EmissionEngine.converter_g_para_kg(1000)
            1.0
        """
        return gramas / 1000
    
    @staticmethod
    def converter_kg_para_g(quilogramas: float) -> float:
        """
        Converte quilogramas para gramas.
        
        Args:
            quilogramas (float): Valor em quilogramas
        
        Returns:
            float: Valor em gramas
        """
        return quilogramas * 1000
    
    @staticmethod
    def converter_minutos_para_horas(minutos: float) -> float:
        """
        Converte minutos para horas.
        
        Args:
            minutos (float): Tempo em minutos
        
        Returns:
            float: Tempo em horas
        """
        return minutos / 60
    
    # ========================================================
    # 3. CÁLCULOS AGREGADOS (SOMA DE MÚLTIPLOS EVENTOS)
    # ========================================================
    
    def calcular_co2_total(self, eventos: list) -> float:
        """
        Calcula o CO₂ total evitado em uma lista de eventos.
        
        Args:
            eventos (list): Lista de objetos Evento
        
        Returns:
            float: Total de CO₂ evitado em gramas
        
        Exemplo:
            >>> motor = EmissionEngine()
            >>> eventos = [evento1, evento2, evento3]
            >>> total = motor.calcular_co2_total(eventos)
            >>> print(f"Total: {total}g = {motor.converter_g_para_kg(total)}kg")
            Total: 500g = 0.5kg
        """
        # Se nenhum evento, retorna 0
        if not eventos:
            return 0
        
        # Soma todos os CO2 evitados
        total = sum(
            evento.co2_evitado_g for evento in eventos
            if evento.co2_evitado_g is not None
        )
        
        return total
    
    # ========================================================
    # 4. ANÁLISE DE IMPACTO
    # ========================================================
    
    def equivalente_arvores_plantadas(self, co2_g: float) -> float:
        """
        Converte gramas de CO₂ em número de árvores equivalentes.
        
        Assumindo que 1 árvore absorve ~20kg de CO₂ por ano.
        
        Args:
            co2_g (float): Quantidade de CO₂ em gramas
        
        Returns:
            float: Número equivalente de árvores
        
        Exemplo:
            >>> motor = EmissionEngine()
            >>> co2 = 20000  # 20kg
            >>> arvores = motor.equivalente_arvores_plantadas(co2)
            >>> print(f"Equivalente a {arvores} árvore/ano")
            Equivalente a 1.0 árvore/ano
        """
        co2_kg = self.converter_g_para_kg(co2_g)
        ABSORCAO_POR_ARVORE_KG = 20  # kg/ano por árvore
        
        return co2_kg / ABSORCAO_POR_ARVORE_KG
    
    def equivalente_km_economizados(self, co2_g: float) -> float:
        """
        Converte gramas de CO₂ em quilômetros economizados.
        
        Assumindo ~200g de CO₂ por quilômetro rodado em média.
        
        Args:
            co2_g (float): Quantidade de CO₂ em gramas
        
        Returns:
            float: Quilômetros equivalentes
        
        Exemplo:
            >>> motor = EmissionEngine()
            >>> co2 = 600  # 600g
            >>> km = motor.equivalente_km_economizados(co2)
            >>> print(f"Equivalente a {km}km não rodado")
            Equivalente a 3.0km não rodado
        """
        CO2_POR_KM = 200  # g/km (média)
        
        return co2_g / CO2_POR_KM
    
    # ========================================================
    # 5. RELATÓRIO DE EMISSÕES
    # ========================================================
    
    def gerar_relatorio(self, eventos: list, veiculo: Veiculo) -> dict:
        """
        Gera um relatório completo de emissões.
        
        Args:
            eventos (list): Lista de eventos
            veiculo (Veiculo): Veículo utilizado
        
        Returns:
            dict: Relatório com várias métricas
        
        Exemplo:
            >>> motor = EmissionEngine()
            >>> relatorio = motor.gerar_relatorio(eventos, carro)
            >>> print(relatorio["co2_total_kg"])
            0.5
        """
        co2_total_g = self.calcular_co2_total(eventos)
        co2_total_kg = self.converter_g_para_kg(co2_total_g)
        
        tempo_total_min = sum(e.tempo_economizado_min for e in eventos)
        tempo_total_horas = self.converter_minutos_para_horas(tempo_total_min)
        
        relatorio = {
            "veiculo": f"{veiculo.brand} {veiculo.model}",
            "numero_eventos": len(eventos),
            "tempo_total_economizado_min": tempo_total_min,
            "tempo_total_economizado_horas": round(tempo_total_horas, 2),
            "co2_total_evitado_g": co2_total_g,
            "co2_total_evitado_kg": round(co2_total_kg, 3),
            "equivalente_arvores": round(
                self.equivalente_arvores_plantadas(co2_total_g), 2
            ),
            "equivalente_km": round(
                self.equivalente_km_economizados(co2_total_g), 2
            ),
        }
        
        return relatorio
    
    # ========================================================
    # 6. VALIDAÇÕES
    # ========================================================
    
    @staticmethod
    def validar_fator_emissao(co2_per_minute: float) -> bool:
        """
        Valida se o fator de emissão está dentro dos limites esperados.
        
        Args:
            co2_per_minute (float): g/min
        
        Returns:
            bool: True se válido, False caso contrário
        
        Detalhes:
            - Mínimo: 0 g/min (carro elétrico)
            - Máximo: 50 g/min (caminhão pesado)
        """
        return 0 <= co2_per_minute <= 50
    
    def obter_historico(self) -> list:
        """
        Retorna o histórico de todos os cálculos realizados.
        
        Returns:
            list: Lista com histórico de cálculos
        """
        return self.historico_calculos.copy()
    
    def limpar_historico(self):
        """Limpa o histórico de cálculos."""
        self.historico_calculos.clear()
        print("🗑️ Histórico de cálculos limpado")


# ============================================================
# EXEMPLO DE USO (comentado, para referência)
# ============================================================

"""
# Criar o engine
motor = EmissionEngine()

# Criar um veículo
veiculo = Veiculo(
    brand="Jeep",
    model="Compass",
    year=2022,
    fuel_type=TipoCombustivel.GASOLINA,
    category=CategoriaVeiculo.SUV,
    co2_per_minute=28
)

# Criar um evento
evento = Evento(
    tipo=TipoEvento.PEDAGIO,
    tempo_economizado_min=4.5
)

# Calcular CO₂
co2 = motor.calcular_co2_evitado(evento, veiculo)
print(f"CO₂ evitado: {co2}g")

# Converter para kg
co2_kg = motor.converter_g_para_kg(co2)
print(f"CO₂ evitado: {co2_kg}kg")

# Equivalente a quantas árvores?
arvores = motor.equivalente_arvores_plantadas(co2)
print(f"Equivalente a {arvores} árvores plantadas")
"""

# ============================================================
# FIM DO MÓDULO 2
# ============================================================