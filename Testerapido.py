"""
✅ TESTE RÁPIDO - Verificar que tudo está funcionando
======================================================

Execute este arquivo para testar se todas as partes estão
conectadas corretamente.

    python test_rapido.py
"""

print("\n" + "="*60)
print("🔍 TESTE RÁPIDO DO ECOMETRIC".center(60))
print("="*60 + "\n")

# ============================================================
# TESTE 1: Importações
# ============================================================

print("1️⃣ Testando importações...")

try:
    from src.models import (
        Veiculo, Evento, Usuario,
        TipoCombustivel, CategoriaVeiculo, TipoEvento,
        TipoResgate, CATALOGO_RESGATES
    )
    print("   ✅ src.models importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar models: {e}")
    exit(1)

try:
    from src.config import MONGODB_URI, CAPCOIN_POR_PEDAGIO
    print("   ✅ src.config importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar config: {e}")
    exit(1)

try:
    from src.emission_engine import EmissionEngine
    print("   ✅ src.emission_engine importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar emission_engine: {e}")
    exit(1)

try:
    from src.gamification_engine import GamificationEngine
    print("   ✅ src.gamification_engine importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar gamification_engine: {e}")
    exit(1)

try:
    from src.simulator import Simulador
    print("   ✅ src.simulator importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar simulator: {e}")
    exit(1)

# ============================================================
# TESTE 2: Criar Veículo
# ============================================================

print("\n2️⃣ Testando criação de veículo...")

try:
    veiculo = Veiculo(
        brand="Toyota",
        model="Corolla",
        year=2022,
        fuel_type=TipoCombustivel.GASOLINA,
        category=CategoriaVeiculo.SEDAN,
        co2_per_minute=24
    )
    
    assert veiculo.brand == "Toyota"
    assert veiculo.co2_per_minute == 24
    
    print(f"   ✅ Veículo criado: {veiculo.descricao()}")
except Exception as e:
    print(f"   ❌ Erro ao criar veículo: {e}")
    exit(1)

# ============================================================
# TESTE 3: Criar Evento
# ============================================================

print("\n3️⃣ Testando criação de evento...")

try:
    evento = Evento(
        tipo=TipoEvento.PEDAGIO,
        tempo_economizado_min=5.0
    )
    
    assert evento.tipo == TipoEvento.PEDAGIO
    assert evento.tempo_economizado_min == 5.0
    
    print(f"   ✅ Evento criado: {evento.descricao()}")
except Exception as e:
    print(f"   ❌ Erro ao criar evento: {e}")
    exit(1)

# ============================================================
# TESTE 4: Calcular CO₂
# ============================================================

print("\n4️⃣ Testando cálculo de CO₂...")

try:
    motor = EmissionEngine()
    co2_evitado = motor.calcular_co2_evitado(evento, veiculo)
    
    # 5 min × 24 g/min = 120g
    assert co2_evitado == 120.0
    
    # Conversão
    co2_kg = motor.converter_g_para_kg(co2_evitado)
    assert co2_kg == 0.12
    
    print(f"   ✅ CO₂ evitado: {co2_evitado}g = {co2_kg}kg")
except Exception as e:
    print(f"   ❌ Erro ao calcular CO₂: {e}")
    exit(1)

# ============================================================
# TESTE 5: Criar Usuário
# ============================================================

print("\n5️⃣ Testando criação de usuário...")

try:
    usuario = Usuario(
        user_id="test_001",
        nome="Teste",
        email="teste@test.com"
    )
    
    usuario.adicionar_veiculo(veiculo)
    usuario.adicionar_evento(evento)
    
    assert len(usuario.veiculos) == 1
    assert len(usuario.eventos) == 1
    
    print(f"   ✅ Usuário criado: {usuario.nome}")
    print(f"      - Veículos: {len(usuario.veiculos)}")
    print(f"      - Eventos: {len(usuario.eventos)}")
except Exception as e:
    print(f"   ❌ Erro ao criar usuário: {e}")
    exit(1)

# ============================================================
# TESTE 6: Calcular CapCoins
# ============================================================

print("\n6️⃣ Testando cálculo de CapCoins...")

try:
    game = GamificationEngine()
    
    capcoin = game.calcular_capcoin(evento)
    # Pedágio = 5 CapCoins
    assert capcoin == 5
    
    game.adicionar_capcoin(usuario, capcoin, "Teste")
    assert usuario.capcoin_total == 5
    
    print(f"   ✅ CapCoins gerados: {capcoin}")
    print(f"      - Saldo do usuário: {usuario.capcoin_total}")
except Exception as e:
    print(f"   ❌ Erro ao calcular CapCoins: {e}")
    exit(1)

# ============================================================
# TESTE 7: Bônus
# ============================================================

print("\n7️⃣ Testando bônus...")

try:
    # Bônus streak
    bonus_streak = game.calcular_bonus_streak(usuario, 5)
    assert bonus_streak >= 0
    
    # Bônus engajamento
    bonus_engaj = game.calcular_bonus_engajamento(10)
    assert bonus_engaj >= 0
    
    print(f"   ✅ Bônus streak (5 dias): {bonus_streak} CapCoins")
    print(f"      Bônus engajamento (10 eventos): {bonus_engaj} CapCoins")
except Exception as e:
    print(f"   ❌ Erro ao calcular bônus: {e}")
    exit(1)

# ============================================================
# TESTE 8: Resgate
# ============================================================

print("\n8️⃣ Testando resgate...")

try:
    # Adicionar CapCoins para poder resgatar
    game.adicionar_capcoin(usuario, 100, "Bônus teste")
    
    # Tentar resgatar
    premios = game.listar_premios_disponiveis(usuario)
    
    # Contar quantos prêmios são acessíveis
    disponiveis = sum(1 for p in premios.values() if p['disponivel'])
    
    print(f"   ✅ Prêmios disponíveis: {disponiveis}")
    
except Exception as e:
    print(f"   ❌ Erro ao testar resgate: {e}")
    exit(1)

# ============================================================
# TESTE 9: Simulador
# ============================================================

print("\n9️⃣ Testando simulador...")

try:
    sim = Simulador()
    
    user = sim.criar_usuario("sim_001", "Simulador Teste")
    veh = sim.adicionar_veiculo(
        user, "Fiat", "Uno", 2023,
        TipoCombustivel.GASOLINA,
        CategoriaVeiculo.HATCH,
        co2_per_minute=16
    )
    
    eventos_sim = sim.simular_eventos_mensais(user, veh, numero_eventos=3)
    
    assert len(eventos_sim) > 0
    assert user.capcoin_total > 0
    
    print(f"   ✅ Simulador funcionando!")
    print(f"      - Eventos simulados: {len(eventos_sim)}")
    print(f"      - CapCoins gerados: {user.capcoin_total}")
    print(f"      - CO₂ evitado: {user.co2_total_evitado_g:.0f}g")
except Exception as e:
    print(f"   ❌ Erro no simulador: {e}")
    exit(1)

# ============================================================
# TESTE 10: Relatórios
# ============================================================

print("\n🔟 Testando relatórios...")

try:
    relatorio_motor = motor.gerar_relatorio([evento], veiculo)
    assert "co2_total_evitado_g" in relatorio_motor
    
    relatorio_game = game.gerar_relatorio(usuario)
    assert "saldo_atual" in relatorio_game
    
    print(f"   ✅ Relatórios gerados com sucesso")
    print(f"      - Emissão: {relatorio_motor['co2_total_evitado_g']}g evitado")
    print(f"      - Gamificação: {relatorio_game['saldo_atual']} CapCoins")
except Exception as e:
    print(f"   ❌ Erro ao gerar relatórios: {e}")
    exit(1)

# ============================================================
# RESULTADO FINAL
# ============================================================

print("\n" + "="*60)
print("✅ TODOS OS TESTES PASSARAM!".center(60))
print("="*60)

print("""
🎉 Parabéns! Seu ambiente está funcionando corretamente.

📚 Próximos passos:

1. Execute o exemplo educacional:
   python exemplo_educacional.py

2. Execute a simulação completa:
   python main.py

3. Explore o código:
   - Leia src/models.py
   - Leia src/emission_engine.py
   - Leia src/gamification_engine.py

4. Experimente:
   - Modifique os valores
   - Crie novos tipos de eventos
   - Adicione novas regras de bônus

Bom aprendizado! 🌱
""")