"""
🚀 COMEÇAR AQUI - GUIA RÁPIDO DO ECOMETRIC
===========================================

Bem-vindo! Este arquivo explica como começar.
"""

print("""

╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🌱 ECOMETRIC - Plataforma de Impacto Ambiental Gamificada    ║
║                                                                  ║
║   Transformando mobilidade urbana em CO₂ evitado + Prêmios     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝


📋 ESTRUTURA DO PROJETO
════════════════════════════════════════════════════════════════════

ecometric/
├── 📚 APRENDER (Comece por aqui!)
│   ├── exemplo_educacional.py    ⭐ COMECE AQUI! (5 min)
│   ├── test_rapido.py             ✅ Teste se tudo funciona
│   └── README.md                  📖 Guia completo
│
├── 💻 CÓDIGO PRINCIPAL (Estruturado para aprender)
│   └── src/
│       ├── models.py              🏗️ Classes (Veículo, Evento, Usuario)
│       ├── emission_engine.py      🌍 Cálculo de CO₂
│       ├── gamification_engine.py  🪙 Sistema de CapCoins
│       ├── simulator.py            🎮 Simular eventos
│       └── config.py               ⚙️ Configurações
│
├── 🏃 EXECUTAR
│   ├── main.py                    🚀 Simulação completa (1-2 min)
│   └── exemplo_educacional.py     📚 Aula interativa
│
└── ⚙️ SETUP
    ├── .env                       🔐 Variáveis de ambiente
    ├── requirements.txt           📦 Dependências
    └── README.md                  📘 Documentação

════════════════════════════════════════════════════════════════════


🎯 PASSO 1: INSTALAÇÃO
════════════════════════════════════════════════════════════════════

1. Abra o terminal/prompt na pasta ecometric

2. Crie um ambiente virtual (RECOMENDADO):
   
   Windows:
   python -m venv venv
   venv\\Scripts\\activate
   
   macOS/Linux:
   python -m venv venv
   source venv/bin/activate

3. Instale as dependências:
   pip install -r requirements.txt

════════════════════════════════════════════════════════════════════


📚 PASSO 2: APRENDER (INÍCIO RECOMENDADO!)
════════════════════════════════════════════════════════════════════

Primeiro: Execute o EXEMPLO EDUCACIONAL

   python exemplo_educacional.py

Este arquivo mostra:
   ✅ Como criar um veículo
   ✅ Como criar eventos (pedágio/estacionamento)
   ✅ Como calcular CO₂ evitado
   ✅ Como gerar CapCoins
   ✅ Como resgatar prêmios

TEMPO: ~5 minutos | DIFICULDADE: Fácil

════════════════════════════════════════════════════════════════════


✅ PASSO 3: VERIFICAR QUE TUDO FUNCIONA
════════════════════════════════════════════════════════════════════

Execute o teste rápido:

   python test_rapido.py

Ele vai verificar que todas as partes estão funcionando.

TEMPO: ~30 segundos | Esperado: "TODOS OS TESTES PASSARAM!"

════════════════════════════════════════════════════════════════════


🚀 PASSO 4: SIMULAÇÃO COMPLETA
════════════════════════════════════════════════════════════════════

Agora rode a simulação completa com múltiplos usuários:

   python main.py

Você verá:
   🎮 Simulação de 3 usuários
   🚗 Múltiplos veículos
   📍 Dezenas de eventos
   🌍 Impacto ambiental total
   🪙 CapCoins gerados
   🎁 Prêmios resgatados
   📊 Relatórios detalhados

TEMPO: ~1-2 minutos

════════════════════════════════════════════════════════════════════


📖 PASSO 5: ESTUDAR O CÓDIGO
════════════════════════════════════════════════════════════════════

Agora leia cada arquivo na ordem:

1️⃣ src/models.py
   └─ Entenda como os dados são organizados
   └─ Classes: Veículo, Evento, Usuario
   └─ ~400 linhas com comentários

2️⃣ src/emission_engine.py
   └─ Aprenda como calcular CO₂ evitado
   └─ Fórmula: CO₂ = Tempo × Emissão
   └─ Conversões e equivalências
   └─ ~350 linhas

3️⃣ src/gamification_engine.py
   └─ Sistema de CapCoins
   └─ Bônus (Streak, Engajamento)
   └─ Anti-fraude e Resgates
   └─ ~400 linhas

4️⃣ src/simulator.py
   └─ Integração de tudo
   └─ Simulação realista
   └─ ~300 linhas

5️⃣ main.py
   └─ Como usar tudo junto
   └─ ~200 linhas

════════════════════════════════════════════════════════════════════


💡 ENTENDENDO A LÓGICA
════════════════════════════════════════════════════════════════════

O Ecometric funciona assim:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. USUÁRIO usa Taggy em um PEDÁGIO                            │
│                                                                 │
│     Normal: espera 4.5 min em fila                             │
│     Com Taggy: passa direto!                                   │
│     → Economiza: 4.5 minutos                                   │
│                                                                 │
│  2. EMISSION ENGINE calcula CO₂ EVITADO                        │
│                                                                 │
│     CO₂ = 4.5 min × 28 g/min = 126g                           │
│                                                                 │
│  3. GAMIFICATION ENGINE gera CAPCOIN                           │
│                                                                 │
│     Pedágio = +5 CapCoins                                      │
│     + Bonus Streak (5 dias) = +8 CapCoins                     │
│     + Bonus Engajamento (20 eventos) = +12 CapCoins           │
│     = TOTAL: 25 CapCoins                                       │
│                                                                 │
│  4. USUÁRIO RESGATA PRÊMIO                                     │
│                                                                 │
│     300 CapCoins → 1 árvore plantada                           │
│     150 CapCoins → Ecobag sustentável                          │
│     Etc...                                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════════════════


🎮 EXPERIMENTAR E MODIFICAR
════════════════════════════════════════════════════════════════════

Depois de entender o código, experimente:

1. Modifique VALORES em src/config.py:
   └─ Mude CAPCOIN_POR_PEDAGIO de 5 para 10
   └─ Teste: python main.py
   └─ Veja como muda o resultado

2. Crie um NOVO TIPO DE EVENTO:
   └─ Adicione em TipoEvento (models.py)
   └─ Crie a lógica de CapCoins (gamification_engine.py)
   └─ Teste no simulador

3. ADICIONE UM NOVO BÔNUS:
   └─ Ex: Bônus social (amigos usando Taggy)
   └─ Implemente em gamification_engine.py
   └─ Integrate no simulator.py

════════════════════════════════════════════════════════════════════


❓ DÚVIDAS FREQUENTES
════════════════════════════════════════════════════════════════════

P: Quanto conhecimento de Python preciso?
R: Mínimo: variáveis, funções, listas, dicionários.
   O resto você aprende pelo código comentado.

P: Quanto tempo leva para aprender?
R: 5 min (exemplo) + 30 min (código) + tempo experimental.
   Acumulativo: ~2-4 horas para dominar.

P: Posso mudar o código?
R: SIM! Essa é a melhor forma de aprender.

P: Quando adiciono MongoDB?
R: Depois de entender a lógica em memória.
   Então crie src/database.py

P: Como conectar com dados reais da Taggy?
R: Em src/simulator.py, substitua a simulação
   por chamadas à API Taggy.

════════════════════════════════════════════════════════════════════


📚 RECURSOS
════════════════════════════════════════════════════════════════════

Dentro do projeto:
   ├── README.md          → Documentação completa
   ├── exemplo_educacional.py → Tutorial passo a passo
   └── src/*/              → Código super comentado

Fora do projeto:
   └── Python.org         → Documentação oficial Python

════════════════════════════════════════════════════════════════════


🎯 ROTEIRO DE APRENDIZADO (Semana a semana)
════════════════════════════════════════════════════════════════════

SEGUNDA-FEIRA:
   [ ] Instalar e rodar exemplo_educacional.py
   [ ] Rodar test_rapido.py
   [ ] Ler src/models.py

TERÇA-FEIRA:
   [ ] Ler src/emission_engine.py
   [ ] Modificar valores de emissão
   [ ] Testar conversões

QUARTA-FEIRA:
   [ ] Ler src/gamification_engine.py
   [ ] Entender bônus
   [ ] Modificar regras de CapCoins

QUINTA-FEIRA:
   [ ] Ler src/simulator.py
   [ ] Rodar main.py completo
   [ ] Analisar relatórios

SEXTA-FEIRA:
   [ ] Criar seus próprios desafios
   [ ] Adicionar novo tipo de evento
   [ ] Implementar novo bônus

════════════════════════════════════════════════════════════════════


✨ COMEÇAR AGORA!
════════════════════════════════════════════════════════════════════

No terminal, execute:

   python exemplo_educacional.py

E veja o Ecometric em ação! 🚀

════════════════════════════════════════════════════════════════════

Boa sorte! 🌱💚
Aproveite o aprendizado!

""")