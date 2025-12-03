import google.generativeai as genai
from app.nucleo.configuracoes import settings
from app.servicos import servico_banco_de_dados

if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)

# Link do Dashboard (Certifique-se que é o seu link atual do ngrok)
# Como não temos dois túneis, enviamos uma mensagem instruindo a olhar o telão
LINK_DASHBOARD = "O Dashboard está aberto no computador da apresentação. Acompanhe no telão! 🖥️"

# --- MEMÓRIA VOLÁTIL ---
historico_conversas = {}

CONHECIMENTO_TECNICO = """
PROJETO: "Horta Inteligente" (Sistema IoT de Horticultura de Precisão).

=== 1. TABELA DE REFERÊNCIA (Hortaliças Folhosas/Alface) ===
- Umidade: Ideal 60% a 80%. (Abaixo de 40% = Crítico/Seco).
- pH: Ideal 6.0 a 7.0.
- EC (Condutividade): 1000 a 1800 µS/cm.
- Nitrogênio (N): 150-200 mg/kg.
- Fósforo (P): 60-100 mg/kg.
- Potássio (K): 150-200 mg/kg.

=== 2. GUIA DE MANEJO RÁPIDO ===
- pH BAIXO (< 5.5): Aplicar Calcário.
- pH ALTO (> 7.5): Aplicar Enxofre.
- N BAIXO: Adubar com Ureia ou Esterco.
- P BAIXO: Adubar com Farinha de Ossos.
- K BAIXO: Adubar com Cloreto de Potássio.
- EC ALTA: Lavar o solo (irrigação excessiva controlada).
"""

def get_chat_history(chat_id):
    if chat_id not in historico_conversas:
        historico_conversas[chat_id] = []
    return historico_conversas[chat_id]

async def processar_mensagem_usuario(texto_usuario: str, chat_id: str = "default") -> str:
    print(f"[DEBUG] Mensagem de {chat_id}: {texto_usuario}")

    # --- 1. FILTRO DE SAUDAÇÃO E RESET ---
    saudacoes = ['/start', 'reset', 'reiniciar', 'começar', 'oi', 'ola', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'opa']
    
    # Verifica saudação simples
    if texto_usuario.lower().strip() in saudacoes:
        historico_conversas[chat_id] = [] # Limpa memória anterior
        return (
            "🌿 **Olá! Eu sou o Hortbot.**\n\n"
            "Sou a Inteligência Artificial do projeto **Horta Inteligente**.\n"
            "Estou aqui para monitorar sua produção e tirar dúvidas técnicas.\n\n"
            "**Como posso ajudar?**\n"
            "1️⃣ *Como está a horta?* (Diagnóstico)\n"
            "2️⃣ *Quais os dados atuais?* (Telemetria)\n"
            "3️⃣ *Quero ver gráficos* (Dashboard)\n"
        )

    # --- 2. BUSCA E TRATAMENTO DE DADOS ---
    dados = servico_banco_de_dados.buscar_ultimos_dados()
    
    if dados:
        # Tratamento de Data/Hora
        data_str = dados.get('data')
        hora_str = dados.get('hora')
        if data_str and hora_str:
            momento = f"{data_str} às {hora_str}"
        else:
            ts = dados.get('timestamp', 'Agora')
            momento = str(ts)[0:16]

        def obter_valor(chaves):
            for k in chaves:
                val = dados.get(k)
                if val is not None:
                    # Se vier dicionário do Mongo, limpa
                    if isinstance(val, dict): val = list(val.values())[0]
                    try:
                        val_float = float(val)
                        # CORREÇÃO DA UMIDADE (0.3 -> 30.0%)
                        if 'umidade' in chaves[0] or 'h' in chaves:
                            if val_float <= 1.0: val_float *= 100
                        return round(val_float, 2)
                    except:
                        return val
            return '?'

        # Contexto formatado
        contexto_sensores = (
            f"TELEMETRIA ATUAL ({momento}):\n"
            f"- Umidade: {obter_valor(['h', 'umidade'])}%\n"
            f"- Temp: {obter_valor(['temperatura', 'temp'])}°C\n"
            f"- pH: {obter_valor(['ph_solo', 'ph'])}\n"
            f"- EC: {obter_valor(['condutividade_elétrica', 'condutividade_eletrica'])} µS/cm\n"
            f"- Nitrogênio (N): {obter_valor(['nitrogênio', 'nitrogenio'])} mg/kg\n"
            f"- Fósforo (P): {obter_valor(['fósforo', 'fosforo'])} mg/kg\n"
            f"- Potássio (K): {obter_valor(['potássio', 'potassio'])} mg/kg\n"
        )
    else:
        contexto_sensores = "STATUS: Dados dos sensores indisponíveis no momento."

    # --- 3. PROMPT BLINDADO (MODO AGRO) ---
    # --- 3. PROMPT BLINDADO (MODO AGRO) ---
    prompt_completo = (
        f"IDENTIDADE: Hortbot (Assistente Técnico do projeto Horta Inteligente).\n"
        f"IDIOMA: Português do Brasil (PT-BR) OBRIGATÓRIO.\n\n"
        
        f"PROTOCOLO DE SEGURANÇA (IMPORTANTE):\n"
        f"1. SEU FOCO É EXCLUSIVO: Agronomia, Horticultura, Botânica e o projeto Horta Inteligente.\n"
        f"2. BLOQUEIO DE ASSUNTO: Se o usuário perguntar sobre futebol, política, piadas ou assuntos aleatórios, RECUSE.\n"
        f"   - Exceção: Se o usuário enviar apenas números ('1', '2', '3'), trate como escolha de menu.\n\n"

        f"DADOS DO CAMPO:\n{contexto_sensores}\n"
        f"MANUAL TÉCNICO:\n{CONHECIMENTO_TECNICO}\n\n"
        
        f"DIRETRIZES DE RESPOSTA:\n"
        f"- Se o usuário digitar '1', 'diagnóstico' ou perguntar 'como está': Faça uma análise completa cruzando dados com a tabela.\n"
        f"- Se o usuário digitar '2', 'telemetria' ou perguntar 'dados': Liste apenas os valores atuais dos sensores com emojis.\n"
        f"- Se o usuário digitar '3', 'dashboard' ou 'gráficos': Envie apenas o link: {LINK_DASHBOARD}\n"
        f"- Use emojis técnicos (🌿, 💧, ⚠️) mas não exagere. NÃO use Markdown (negrito/itálico).\n"
        f"- Seja gentil, mas profissional.\n\n"
        
        f"PERGUNTA DO USUÁRIO: {texto_usuario}"
    )

    try:
        if not settings.GOOGLE_API_KEY:
            return "⚠️ Erro: Chave API ausente."

        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Histórico
        historico_atual = get_chat_history(chat_id)
        chat = model.start_chat(history=historico_atual)
        
        response = chat.send_message(prompt_completo)
        
        # Salva histórico
        historico_conversas[chat_id] = chat.history

        return response.text

    except Exception as e:
        print(f"[ERRO IA] {e}")
        return "Hortbot indisponível no momento. Tente novamente."