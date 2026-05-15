"""
📚 EXEMPLO EDUCACIONAL - ENTENDENDO O ECOMETRIC PASSO A PASSO
==============================================================

Este arquivo mostra como usar o Ecometric aprendendo cada conceito.

Estude-o na ordem:
1. Criando um veículo
2. Criando eventos
3. Calculando CO₂
4. Criando usuários
5. Calculando CapCoins
6. Sistema completo
"""

# ============================================================
# PARTE 1: ENTENDENDO CLASSES E OBJETOS
# ============================================================

print("""
╔════════════════════════════════════════════════════════════╗
║ PARTE 1: ENTENDENDO CLASSES                               ║
╚════════════════════════════════════════════════════════════╝
""")

from src.models import (
    Veiculo, TipoCombustivel, CategoriaVeiculo,
    Evento, TipoEvento,
    Usuario
)

print("📌 Uma classe é como um molde que define a estrutura de um objeto.")
print("Exemplo: A classe Veiculo tem propriedades como marca, modelo, ano, etc.")
print()

# Criando um veículo (instância da classe)
print("1️⃣ Criando um veículo:")
print("-" * 60)

meu_carro = Veiculo(
    brand="Jeep",
    model="Compass",
    year=2022,
    fuel_type=TipoCombustivel.GASOLINA,
    category=CategoriaVeiculo.SUV,
    co2_per_minute=28  # Quanto de CO₂ emite por minuto
)

print(f"✅ Veículo criado: {meu_carro.descricao()}")
print()
print(f"   Detalhes:")
print(f"   - Marca: {meu_carro.brand}")
print(f"   - Modelo: {meu_carro.model}")
print(f"   - Ano: {meu_carro.year}")
print(f"   - Combustível: {meu_carro.fuel_type.value}")
print(f"   - Categoria: {meu_carro.category.value}")
print(f"   - Emissão: {meu_carro.co2_per_minute} g/min")
print()

# ============================================================
# PARTE 2: ENTENDENDO EVENTOS
# ============================================================

print("""
╔════════════════════════════════════════════════════════════╗
║ PARTE 2: EVENTOS (Pedágio e Estacionamento)               ║
╚════════════════════════════════════════════════════════════╝
""")

print("📌 Um evento é quando você usa a Taggy (pedágio ou estacionamento).")
print()

# Evento 1: Passagem em pedágio
print("2️⃣ Criando um evento de PEDÁGIO:")
print("-" * 60)

evento_pedagio = Evento(
    tipo=TipoEvento.PEDAGIO,
    tempo_economizado_min=4.5  # Você economizou 4.5 minutos neste pedágio
)

print(f"✅ Evento criado: {evento_pedagio.descricao()}")
print()
print(f"   O que isso significa:")
print(f"   - Você passava em um pedágio e normalmente levava 4.5 minutos")
print(f"   - Com a Taggy, passou direto sem parar")
print(f"   - Resultado: Economizou 4.5 minutos de motor ligado")
print(f"   - Menos motor ligado = Menos CO₂ emitido!")
print()

# Evento 2: Entrada em estacionamento
print("3️⃣ Criando um evento de ESTACIONAMENTO:")
print("-" * 60)

evento_estacionamento = Evento(
    tipo=TipoEvento.ESTACIONAMENTO,
    tempo_economizado_min=15  # 15 minutos procurando vaga
)

print(f"✅ Evento criado: {evento_estacionamento.descricao()}")
print()
print(f"   O que isso significa:")
print(f"   - Você procurava estacionamento e levava ~15 minutos")
print(f"   - Com a Taggy, encontrou direto")
print(f"   - Resultado: Economizou 15 minutos de motor ligado")
print()

# ============================================================
# PARTE 3: CALCULANDO CO₂
# ============================================================

print("""
╔════════════════════════════════════════════════════════════╗
║ PARTE 3: ENGINE DE EMISSÕES (Calculando CO₂)              ║
╚════════════════════════════════════════════════════════════╝
""")

from src.emission_engine import EmissionEngine

print("📌 Agora vamos calcular quanto CO₂ foi EVITADO em cada evento.")
print()

# Criar o engine
motor = EmissionEngine()

print("4️⃣ Calculando CO₂ evitado no PEDÁGIO:")
print("-" * 60)

# Fórmula: CO₂ evitado = Tempo × Emissão
# CO₂ = 4.5 min × 28 g/min = 126g
co2_pedagio = motor.calcular_co2_evitado(evento_pedagio, meu_carro)

print(f"✅ CO₂ calculado: {co2_pedagio}g")
print()
print(f"   Fórmula:")
print(f"   CO₂ evitado = Tempo economizado × Emissão do veículo")
print(f"   CO₂ evitado = {evento_pedagio.tempo_economizado_min} min × {meu_carro.co2_per_minute} g/min")
print(f"   CO₂ evitado = {co2_pedagio}g")
print()
print(f"   Conversão:")
print(f"   - Em quilogramas: {motor.converter_g_para_kg(co2_pedagio)} kg")
print()

print("5️⃣ Calculando CO₂ evitado no ESTACIONAMENTO:")
print("-" * 60)

co2_estacionamento = motor.calcular_co2_evitado(evento_estacionamento, meu_carro)

print(f"✅ CO₂ calculado: {co2_estacionamento}g")
print()
print(f"   Fórmula:")
print(f"   CO₂ evitado = {evento_estacionamento.tempo_economizado_min} min × {meu_carro.co2_per_minute} g/min")
print(f"   CO₂ evitado = {co2_estacionamento}g")
print()
print(f"   Conversão:")
print(f"   - Em quilogramas: {motor.converter_g_para_kg(co2_estacionamento)} kg")
print()

print("6️⃣ Total de CO₂ evitado em ambos os eventos:")
print("-" * 60)

eventos = [evento_pedagio, evento_estacionamento]
co2_total = motor.calcular_co2_total(eventos)

print(f"✅ CO₂ total: {co2_total}g = {motor.converter_g_para_kg(co2_total)} kg")
print()
print(f"   Equivalentes:")
print(f"   - Árvores: {motor.equivalente_arvores_plantadas(co2_total):.2f} árvores plantadas/ano")
print(f"   - Km: {motor.equivalente_km_economizados(co2_total):.2f} km não rodados")
print()

# ============================================================
# PARTE 4: CRIANDO USUÁRIO
# ============================================================

print("""
╔════════════════════════════════════════════════════════════╗
║ PARTE 4: USUÁRIO E SEUS DADOS                             ║
╚════════════════════════════════════════════════════════════╝
""")

print("📌 Um usuário é uma pessoa que usa o Ecometric.")
print()

print("7️⃣ Criando um usuário:")
print("-" * 60)

usuario = Usuario(
    user_id="123",
    nome="João Silva",
    email="joao@email.com"
)

print(f"✅ Usuário criado: {usuario.nome}")
print()

print("8️⃣ Adicionando veículo ao usuário:")
print("-" * 60)

usuario.adicionar_veiculo(meu_carro)

print()

print("9️⃣ Adicionando eventos ao usuário:")
print("-" * 60)

usuario.adicionar_evento(evento_pedagio)
usuario.adicionar_evento(evento_estacionamento)

print(f"✅ {len(usuario.eventos)} eventos adicionados")
print()

# ============================================================
# PARTE 5: SISTEMA DE CAPCOIN (GAMIFICAÇÃO)
# ============================================================

print("""
╔════════════════════════════════════════════════════════════╗
║ PARTE 5: GAMIFICAÇÃO (CapCoins)                           ║
╚════════════════════════════════════════════════════════════╝
""")

from src.gamification_engine import GamificationEngine

print("📌 Agora convertemos CO₂ em CAPCOIN (moeda virtual).")
print()

game = GamificationEngine()

print("🔟 Calculando CapCoins do evento de PEDÁGIO:")
print("-" * 60)

capcoin_pedagio = game.calcular_capcoin(evento_pedagio)

print(f"✅ CapCoins ganhos: +{capcoin_pedagio}")
print()
print(f"   Regra: Cada pedágio = {capcoin_pedagio} CapCoins")
print()

print("1️⃣1️⃣ Calculando CapCoins do evento de ESTACIONAMENTO:")
print("-" * 60)

capcoin_estacionamento = game.calcular_capcoin(evento_estacionamento)

print(f"✅ CapCoins ganhos: +{capcoin_estacionamento}")
print()
print(f"   Regra: Cada estacionamento = {capcoin_estacionamento} CapCoins")
print()

print("1️⃣2️⃣ Adicionando CapCoins ao saldo do usuário:")
print("-" * 60)

# Adiciona os CapCoins ao usuário
game.adicionar_capcoin(usuario, capcoin_pedagio, "Pedágio")
game.adicionar_capcoin(usuario, capcoin_estacionamento, "Estacionamento")

print()
print(f"   Saldo atual de {usuario.nome}: {usuario.capcoin_total} CapCoins")
print()

print("1️⃣3️⃣ Aplicando BÔNUS de Streak (uso consecutivo):")
print("-" * 60)

# João usou a Taggy 7 dias seguidos
bonus_streak = game.calcular_bonus_streak(usuario, dias_consecutivos=7)

print(f"✅ Bônus streak (7 dias): +{bonus_streak} CapCoins")
print()

game.adicionar_capcoin(usuario, bonus_streak, "Bônus Streak")

print(f"   Novo saldo: {usuario.capcoin_total} CapCoins")
print()

print("1️⃣4️⃣ Listando prêmios disponíveis:")
print("-" * 60)

premios = game.listar_premios_disponiveis(usuario)

print()
for tipo, info in premios.items():
    status = "✅ DISPONÍVEL" if info['disponivel'] else "❌ INDISPONÍVEL"
    print(f"{status}")
    print(f"   {info['nome']}: {info['custo']} CapCoins")
    print(f"   {info['descricao']}")
    if not info['disponivel']:
        print(f"   Faltam: {info['saldo_faltante']} CapCoins")
    print()

# ============================================================
# PARTE 6: RESGATE DE PRÊMIOS
# ============================================================

print("""
╔════════════════════════════════════════════════════════════╗
║ PARTE 6: RESGATANDO PRÊMIOS                               ║
╚════════════════════════════════════════════════════════════╝
""")

from src.models import TipoResgate

print("📌 Com seus CapCoins, você pode resgatar prêmios ambientais.")
print()

print("1️⃣5️⃣ Tentando resgatar uma ECOBAG (custa 150 CapCoins):")
print("-" * 60)

# Verificar saldo
saldo_antes = usuario.capcoin_total

if saldo_antes >= 150:
    sucesso = game.resgatar_premio(usuario, TipoResgate.ECOBAG)
    
    print()
    if sucesso:
        print(f"🎁 SUCESSO!")
        print(f"   Saldo antes: {saldo_antes} CapCoins")
        print(f"   Custo: 150 CapCoins")
        print(f"   Saldo após: {usuario.capcoin_total} CapCoins")
else:
    print(f"❌ Saldo insuficiente!")
    print(f"   Você tem: {saldo_antes} CapCoins")
    print(f"   Precisa: 150 CapCoins")
    print(f"   Faltam: {150 - saldo_antes} CapCoins")

print()

# ============================================================
# PARTE 7: RESUMO FINAL
# ============================================================

print("""
╔════════════════════════════════════════════════════════════╗
║ RESUMO FINAL                                              ║
╚════════════════════════════════════════════════════════════╝
""")

print(usuario.resumo())

relatorio_game = game.gerar_relatorio(usuario)
print("\n🪙 RELATÓRIO DE GAMIFICAÇÃO:")
for chave, valor in relatorio_game.items():
    print(f"   {chave}: {valor}")

print("\n" + "=" * 60)
print("✅ EXEMPLO EDUCACIONAL CONCLUÍDO!".center(60))
print("=" * 60)

print("""
🎯 O QUE VOCÊ APRENDEU:

1. Classes e Objetos
   └─ Como criar instâncias (Veiculo, Evento, Usuario)

2. Cálculo de CO₂
   └─ Fórmula: CO₂ = Tempo × Emissão

3. Gamificação
   └─ Converter CO₂ em CapCoins (moeda virtual)

4. Bônus e Recompensas
   └─ Streak, Engajamento, Resgate de prêmios

5. Fluxo Completo
   └─ Usuário → Evento → CO₂ → CapCoin → Prêmio

🚀 PRÓXIMOS PASSOS:

1. Rode o main.py para ver a simulação completa
2. Modifique os valores e veja o que muda
3. Adicione MongoDB para persistência
4. Crie uma API REST
5. Desenvolva um Dashboard visual

Boa sorte! 🌱
""")