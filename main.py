"""
🌱 ECOMETRIC - MAIN
===================

Este é o arquivo PRINCIPAL que demonstra todo o sistema funcionando.

Aqui você verá:
1. Criação de usuários
2. Adição de veículos
3. Simulação de eventos
4. Cálculo de CO₂ e CapCoins
5. Resgate de prêmios
6. Relatórios finais

Para executar:
    python main.py
"""

from src.models import TipoCombustivel, CategoriaVeiculo, TipoResgate
from src.simulator import Simulador
from datetime import datetime


def main():
    """
    Função principal - Executa a demonstração completa.
    """
    
    print("\n" + "=" * 80)
    print("🌱 BEM-VINDO AO ECOMETRIC".center(80))
    print("Transformando mobilidade urbana em impacto ambiental".center(80))
    print("=" * 80 + "\n")
    
    # ========================================================
    # PASSO 1: INICIALIZAR O SIMULADOR
    # ========================================================
    
    print("📌 PASSO 1: Inicializando o sistema...")
    print("-" * 80)
    
    simulador = Simulador()
    
    # ========================================================
    # PASSO 2: CRIAR USUÁRIOS
    # ========================================================
    
    print("\n📌 PASSO 2: Criando usuários...")
    print("-" * 80)
    
    usuario1 = simulador.criar_usuario(
        user_id="001",
        nome="João Silva",
        email="joao@example.com"
    )
    
    usuario2 = simulador.criar_usuario(
        user_id="002",
        nome="Maria Santos",
        email="maria@example.com"
    )
    
    usuario3 = simulador.criar_usuario(
        user_id="003",
        nome="Pedro Costa",
        email="pedro@example.com"
    )
    
    # ========================================================
    # PASSO 3: ADICIONAR VEÍCULOS
    # ========================================================
    
    print("\n📌 PASSO 3: Registrando veículos...")
    print("-" * 80)
    
    # Veículo do João (SUV - maior emissão)
    veiculo_joao = simulador.adicionar_veiculo(
        usuario=usuario1,
        brand="Jeep",
        model="Compass",
        year=2022,
        fuel_type=TipoCombustivel.GASOLINA,
        category=CategoriaVeiculo.SUV,
        co2_per_minute=28  # SUV emite mais
    )
    
    # Veículo da Maria (Sedan - emissão média)
    veiculo_maria = simulador.adicionar_veiculo(
        usuario=usuario2,
        brand="Toyota",
        model="Corolla",
        year=2021,
        fuel_type=TipoCombustivel.HIBRIDO,
        category=CategoriaVeiculo.SEDAN,
        co2_per_minute=18  # Híbrido emite menos
    )
    
    # Veículo do Pedro (Hatch - menor emissão)
    veiculo_pedro = simulador.adicionar_veiculo(
        usuario=usuario3,
        brand="Fiat",
        model="Uno",
        year=2023,
        fuel_type=TipoCombustivel.GASOLINA,
        category=CategoriaVeiculo.HATCH,
        co2_per_minute=16  # Hatch é pequeno
    )
    
    # ========================================================
    # PASSO 4: SIMULAR EVENTOS
    # ========================================================
    
    print("\n📌 PASSO 4: Simulando eventos do mês...")
    print("-" * 80)
    
    # João: 20 eventos (uso frequente)
    eventos_joao = simulador.simular_eventos_mensais(
        usuario=usuario1,
        veiculo=veiculo_joao,
        numero_eventos=20
    )
    
    # Maria: 15 eventos (uso moderado)
    eventos_maria = simulador.simular_eventos_mensais(
        usuario=usuario2,
        veiculo=veiculo_maria,
        numero_eventos=15
    )
    
    # Pedro: 25 eventos (uso muito frequente)
    eventos_pedro = simulador.simular_eventos_mensais(
        usuario=usuario3,
        veiculo=veiculo_pedro,
        numero_eventos=25
    )
    
    # ========================================================
    # PASSO 5: APLICAR BÔNUS
    # ========================================================
    
    print("\n📌 PASSO 5: Aplicando bônus de engajamento...")
    print("-" * 80)
    
    # João: streak de 10 dias
    bonus_streak_joao = simulador.gamification_engine.calcular_bonus_streak(
        usuario1, dias_consecutivos=10
    )
    simulador.gamification_engine.adicionar_capcoin(
        usuario1, bonus_streak_joao, f"Bônus Streak: {10} dias"
    )
    
    # Maria: bônus mensal
    bonus_mensal_maria = simulador.gamification_engine.calcular_bonus_mensal(usuario2)
    simulador.gamification_engine.adicionar_capcoin(
        usuario2, bonus_mensal_maria, "Bônus Mensal"
    )
    
    # Pedro: bônus de engajamento
    bonus_engaj_pedro = simulador.gamification_engine.calcular_bonus_engajamento(25)
    simulador.gamification_engine.adicionar_capcoin(
        usuario3, bonus_engaj_pedro, "Bônus Engajamento"
    )
    
    # ========================================================
    # PASSO 6: RESGATAR PRÊMIOS
    # ========================================================
    
    print("\n📌 PASSO 6: Resgatando prêmios...")
    print("-" * 80)
    
    # João resgata uma árvore
    if usuario1.capcoin_total >= 300:
        print(f"\n🎁 {usuario1.nome} está resgatando uma árvore...")
        simulador.processar_resgate(usuario1, TipoResgate.ARVORE_PLANTADA)
    
    # Maria resgata uma ecobag
    if usuario2.capcoin_total >= 150:
        print(f"\n🎁 {usuario2.nome} está resgatando uma ecobag...")
        simulador.processar_resgate(usuario2, TipoResgate.ECOBAG)
    
    # Pedro resgata múltiplos prêmios
    if usuario3.capcoin_total >= 150:
        print(f"\n🎁 {usuario3.nome} está resgatando uma lavagem ecológica...")
        simulador.processar_resgate(usuario3, TipoResgate.LAVAGEM_ECOLOGICA)
    
    # ========================================================
    # PASSO 7: GERAR RELATÓRIOS
    # ========================================================
    
    print("\n📌 PASSO 7: Gerando relatórios...")
    print("-" * 80)
    
    # Relatório individual de João
    print("\n")
    simulador.relatorio_usuario(usuario1)
    
    # Relatório individual de Maria
    print("\n")
    simulador.relatorio_usuario(usuario2)
    
    # Relatório individual de Pedro
    print("\n")
    simulador.relatorio_usuario(usuario3)
    
    # Relatório geral
    simulador.relatorio_todos_usuarios()
    
    # ========================================================
    # PASSO 8: ANÁLISES FINAIS
    # ========================================================
    
    print("\n📌 PASSO 8: Análises e insights...")
    print("-" * 80)
    
    print("\n💡 INSIGHTS DO MÊS:")
    print()
    
    # Qual usuário tem mais CO₂ evitado?
    usuarios_ordenados = sorted(
        simulador.usuarios.values(),
        key=lambda u: u.co2_total_evitado_g,
        reverse=True
    )
    
    print(f"🏆 Maior impacto ambiental: {usuarios_ordenados[0].nome}")
    print(f"   CO₂ evitado: {usuarios_ordenados[0].co2_total_evitado_g/1000:.3f} kg")
    
    # Qual usuário tem mais CapCoins?
    usuarios_capcoin = sorted(
        simulador.usuarios.values(),
        key=lambda u: u.capcoin_total,
        reverse=True
    )
    
    print(f"\n🪙 Maior pontuação: {usuarios_capcoin[0].nome}")
    print(f"   CapCoins: {usuarios_capcoin[0].capcoin_total}")
    
    # Qual tem mais eventos?
    usuarios_eventos = sorted(
        simulador.usuarios.values(),
        key=lambda u: len(u.eventos),
        reverse=True
    )
    
    print(f"\n📍 Mais engajado: {usuarios_eventos[0].nome}")
    print(f"   Eventos: {len(usuarios_eventos[0].eventos)}")
    
    # ========================================================
    # RESUMO FINAL
    # ========================================================
    
    print("\n" + "=" * 80)
    print("✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!".center(80))
    print("=" * 80)
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("""
1. Explore os arquivos em src/:
   - models.py: Estrutura de dados
   - emission_engine.py: Cálculo de CO₂
   - gamification_engine.py: Sistema de CapCoins
   - simulator.py: Simulação de eventos

2. Modifique os parâmetros:
   - Número de eventos
   - Tipos de veículos
   - Emissões
   - Regras de gamificação

3. Adicione MongoDB:
   - Criar database.py para persistência
   - Salvar usuários, eventos, resgate

4. Crie uma API ou Dashboard:
   - Visualizar em tempo real
   - Integrar com dados reais da Taggy
   
Boa sorte! 🚀
    """)


if __name__ == "__main__":
    main()