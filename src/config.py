"""
⚙️ MÓDULO: CONFIGURAÇÕES
========================

Este arquivo centraliza todas as CONFIGURAÇÕES do sistema:
- Conexão com MongoDB
- Variáveis de ambiente
- Constantes do sistema

Benefício: ao invés de espalhar valores "mágicos" pelo código,
deixamos em um único lugar. Fácil de alterar depois.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# ============================================================
# 1. MONGODB - CONFIGURAÇÃO DE BANCO DE DADOS
# ============================================================

# URL de conexão com MongoDB
# Por enquanto usaremos a URL padrão local
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

# Nome do banco de dados
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ecometric")

# Nome das coleções (tabelas no MongoDB)
MONGODB_COLLECTION_USUARIOS = "usuarios"
MONGODB_COLLECTION_VEICULOS = "veiculos"
MONGODB_COLLECTION_EVENTOS = "eventos"
MONGODB_COLLECTION_RESGATES = "resgates"

# ============================================================
# 2. CONFIGURAÇÕES DE NEGÓCIO
# ============================================================

# 🪙 REGRAS DE CAPCOIN - Quanto você ganha por cada evento
CAPCOIN_POR_PEDAGIO = 5  # CapCoins por passagem em pedágio
CAPCOIN_POR_ESTACIONAMENTO = 3  # CapCoins por estacionamento
CAPCOIN_BONUS_MENSAL = 100  # Bônus mensal máximo
CAPCOIN_BONUS_STREAK = 80  # Bônus por streak ativo
CAPCOIN_BONUS_ENGAJAMENTO = 50  # Bônus por engajamento

# 🌍 FATORES DE EMISSÃO PADRÃO (g/min)
# Esses são valores médios baseados no escopo
FATORES_EMISSAO_PADRAO = {
    "Hatch": 20,        # Carros pequenos emitem menos
    "Sedan": 24,        # Carros médios
    "SUV": 28,          # Carros maiores emitem mais
    "Pickup": 32,       # Caminhonetes
    "Elétrico": 0,      # Carro elétrico não emite
}

# ⏰ DURAÇÕES PADRÃO DE EVENTOS (em minutos)
# Usados na simulação quando não há tempo específico
TEMPO_MEDIO_PEDAGIO = 4.5  # Minutos de espera no pedágio
TEMPO_MEDIO_ESTACIONAMENTO = 15  # Minutos de entrada em estacionamento

# ✅ REGRAS ANTI-FRAUDE
DIAS_EXPIRACAO_CAPCOIN = 365  # CapCoins expiram após 1 ano
DIAS_MINIMOS_PARA_INDICACAO = 30  # Novo usuário precisa de 30 dias para indicar
INTERVALO_MINIMO_EVENTOS_MIN = 1  # Mínimo de 1 minuto entre eventos do mesmo usuário

# 📊 SIMULAÇÃO
EVENTOS_SIMULACAO_POR_MES = 20  # Média de eventos por mês do usuário
DIAS_SIMULACAO = 30  # Simular 30 dias

# ============================================================
# 3. VARIÁVEIS DE AMBIENTE
# ============================================================

# Ambiente (desenvolvimento ou produção)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Log level
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================================
# 4. FUNÇÕES AUXILIARES
# ============================================================

def obter_fator_emissao(categoria: str) -> float:
    """
    Retorna o fator de emissão (g/min) para uma categoria de veículo.
    
    Args:
        categoria (str): Categoria do veículo (ex: "SUV")
    
    Returns:
        float: Gramas de CO2 por minuto
    
    Exemplo:
        >>> fator = obter_fator_emissao("SUV")
        >>> print(fator)
        28
    """
    # Se a categoria existe no dicionário, retorna o valor
    # Senão, retorna um valor padrão (24)
    return FATORES_EMISSAO_PADRAO.get(categoria, 24)


def validar_configuracao():
    """
    Valida se as configurações estão corretas.
    
    Levanta uma exceção se algo estiver errado.
    """
    # Verifica se MongoDB URI está configurada
    if not MONGODB_URI:
        raise ValueError("❌ MONGODB_URI não configurada!")
    
    # Verifica se valores de CapCoin são positivos
    if CAPCOIN_POR_PEDAGIO <= 0:
        raise ValueError("❌ CAPCOIN_POR_PEDAGIO deve ser > 0")
    
    print("✅ Configurações validadas com sucesso!")


# ============================================================
# FIM DO MÓDULO
# ============================================================