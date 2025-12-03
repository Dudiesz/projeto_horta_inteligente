import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime, date

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Horta Analytics | Multicultura",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar variáveis de ambiente
load_dotenv("api_backend/.env")

# --- 2. DESIGN SYSTEM & CSS ---
COLORS = {
    "primary": "#2E7D32",      # Verde Folha
    "secondary": "#81C784",    # Verde Claro
    "accent": "#F9A825",       # Amarelo (Atenção)
    "danger": "#D32F2F",       # Vermelho (Crítico)
    "neutral": "#263238",
    "bg_card": "#FFFFFF",
    "chart_colors": {          # Mapeamento fixo de cores para consistência
        "temperatura": "#F9A825", # Laranja/Amarelo
        "umidade": "#2E7D32",     # Verde
        "ph": "#5C6BC0",          # Indigo
        "condutividade": "#26A69A", # Teal
        "nitrogenio": "#66BB6A",
        "fosforo": "#FFEE58",
        "potassio": "#8D6E63"
    }
}

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 3rem; }
        
        /* Cards de Métricas */
        div[data-testid="metric-container"] {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            padding: 10px 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. REGRAS AGRONÔMICAS (BANCO DE CONHECIMENTO) ---
DB_CULTURAS = {
    "Alface Americana": {
        "icon": "🥬",
        "temp": {"min": 15, "max": 24, "ideal": 20},
        "umid": {"min": 60, "max": 80, "ideal": 70},
        "ph":   {"min": 6.0, "max": 7.0},
        "desc": "Sensível ao calor excessivo. Precisa de solo sempre úmido."
    },
    "Rúcula": {
        "icon": "🥗",
        "temp": {"min": 15, "max": 22, "ideal": 18},
        "umid": {"min": 50, "max": 70, "ideal": 60},
        "ph":   {"min": 6.0, "max": 7.0},
        "desc": "Ciclo rápido. Evitar encharcamento para não gerar fungos."
    },
    "Couve Manteiga": {
        "icon": "🍃",
        "temp": {"min": 10, "max": 28, "ideal": 22},
        "umid": {"min": 60, "max": 75, "ideal": 68},
        "ph":   {"min": 6.0, "max": 7.5},
        "desc": "Alta exigência de nitrogênio. Resistente a variações."
    }
}

def gerar_diagnostico(df, regras):
    """Calcula saúde da planta baseada nas regras da cultura selecionada."""
    dicas = []
    status = "Ideal"
    
    if df.empty: return [], "Sem Dados"

    m = df.mean() # Médias do período

    # 1. Temperatura
    if m['temperatura'] < regras['temp']['min']:
        dicas.append(f"❄️ Temperatura média ({m['temperatura']:.1f}°C) abaixo do ideal.")
        status = "Atenção"
    elif m['temperatura'] > regras['temp']['max']:
        dicas.append(f"🔥 Temperatura média ({m['temperatura']:.1f}°C) muito alta. Risco de estresse.")
        status = "Atenção"
    else:
        dicas.append("✅ Temperatura dentro da faixa ideal.")

    # 2. Umidade
    if m['umidade'] < regras['umid']['min']:
        dicas.append(f"🌵 Umidade ({m['umidade']:.1f}%) baixa. Aumentar irrigação.")
        status = "Atenção" if status != "Alerta" else "Alerta"
    elif m['umidade'] > regras['umid']['max']:
        dicas.append(f"💧 Umidade ({m['umidade']:.1f}%) excessiva. Risco de doenças.")
        status = "Alerta"
    else:
        dicas.append("✅ Irrigação adequada.")

    # 3. pH
    if not (regras['ph']['min'] <= m['ph'] <= regras['ph']['max']):
        dicas.append(f"⚖️ pH ({m['ph']:.1f}) fora da faixa ({regras['ph']['min']}-{regras['ph']['max']}).")
        status = "Atenção"

    return dicas, status

# --- 4. CONEXÃO E DADOS ---

@st.cache_resource
def init_connection():
    try:
        uri = os.getenv("MONGODB_URI")
        if not uri: st.error("URI MongoDB não configurada."); st.stop()
        return MongoClient(uri)
    except Exception as e: st.error(f"Erro Conexão: {e}"); st.stop()

@st.cache_data(ttl=60)
def load_data():
    client = init_connection()
    db = client["horta_inteligente"]
    collection = db["dados_sinteticos"]

    projection = {
        "_id": 0, "umidade": 1, "temperatura": 1, "ph": 1, "condutividade": 1,
        "nitrogenio": 1, "fosforo": 1, "potassio": 1, "timestamp": 1
    }
    
    cursor = collection.find({}, projection).sort("timestamp", -1)
    data = list(cursor)

    if not data: return pd.DataFrame()
    df = pd.DataFrame(data)

    cols = ["umidade", "temperatura", "ph", "condutividade", "nitrogenio", "fosforo", "potassio"]
    for c in cols: 
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')
    
    if 'umidade' in df.columns:
        df['umidade'] = df['umidade'].apply(lambda x: x * 100 if x <= 1.0 else x)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    
    return df.dropna(subset=['timestamp'])

# --- 5. INTERFACE (SIDEBAR) ---
st.sidebar.title("⚙️ Configuração")

# 5.1 SELETOR DE CULTURA
st.sidebar.markdown("### 🌱 Cultura Monitorada")
cultura_selecionada = st.sidebar.selectbox(
    "Selecione o canteiro:",
    list(DB_CULTURAS.keys())
)
REGRAS_ATUAIS = DB_CULTURAS[cultura_selecionada]

st.sidebar.divider()

# 5.2 Filtros de Data
df_raw = load_data()
if df_raw.empty: st.warning("Sem dados."); st.stop()

min_d, max_d = df_raw["timestamp"].min().date(), df_raw["timestamp"].max().date()
st.sidebar.markdown("### 📅 Período de Análise")
c1, c2 = st.sidebar.columns(2)
start = c1.date_input("Início", min_d, min_value=min_d, max_value=max_d)
end = c2.date_input("Fim", max_d, min_value=min_d, max_value=max_d)

# 5.3 SELETOR DE SENSORES (RESTAURADO!)
st.sidebar.divider()
st.sidebar.markdown("### 🌡️ Sensores no Gráfico")
variaveis_opcoes = ["temperatura", "umidade", "ph", "condutividade"]
variaveis_selecionadas = st.sidebar.multiselect(
    "Escolha para visualizar:",
    options=variaveis_opcoes,
    default=["temperatura", "umidade"], # Padrão
    format_func=lambda x: x.capitalize()
)

mask = (df_raw["timestamp"].dt.date >= start) & (df_raw["timestamp"].dt.date <= end)
df_filtered = df_raw.loc[mask].sort_values("timestamp")

st.sidebar.divider()
st.sidebar.download_button("📥 Exportar Dados", df_filtered.to_csv(index=False).encode('utf-8'), "dados_horta.csv", "text/csv")

# --- 6. DASHBOARD PRINCIPAL ---

st.title(f"{REGRAS_ATUAIS['icon']} Painel: {cultura_selecionada}")
st.markdown(f"**Perfil da Cultura:** {REGRAS_ATUAIS['desc']}")

if df_filtered.empty:
    st.error("Sem dados para o filtro selecionado.")
else:
    # --- CÁLCULO DE DIAGNÓSTICO ---
    dicas, status_saude = gerar_diagnostico(df_filtered, REGRAS_ATUAIS)
    
    if status_saude == "Ideal": cor_status = COLORS["primary"]
    elif status_saude == "Atenção": cor_status = COLORS["accent"]
    else: cor_status = COLORS["danger"]

    # Banner Status
    st.markdown(f"""
    <div style="background-color: white; padding: 15px 20px; border-radius: 10px; border-left: 8px solid {cor_status}; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;">
        <h3 style="margin:0; color: #444;">Estado Atual: <span style="color:{cor_status}; font-weight:bold;">{status_saude.upper()}</span></h3>
    </div>
    """, unsafe_allow_html=True)

    # --- KPIS ---
    m_temp = df_filtered['temperatura'].mean()
    m_umid = df_filtered['umidade'].mean()
    m_ph = df_filtered['ph'].mean()
    
    target_temp = REGRAS_ATUAIS['temp']['ideal']
    target_umid = REGRAS_ATUAIS['umid']['ideal']

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Temperatura", f"{m_temp:.1f} °C", delta=f"{m_temp - target_temp:.1f} °C (vs Ideal)", delta_color="inverse")
    k2.metric("Umidade Solo", f"{m_umid:.1f} %", delta=f"{m_umid - target_umid:.1f} % (vs Ideal)", delta_color="inverse")
    k3.metric("pH Solo", f"{m_ph:.1f}", delta="Faixa OK" if REGRAS_ATUAIS['ph']['min'] <= m_ph <= REGRAS_ATUAIS['ph']['max'] else "Ajustar", delta_color="normal")
    k4.metric("Condutividade", f"{df_filtered['condutividade'].mean():.2f} µS")

    st.divider()

    # --- GRÁFICO CENTRAL ---
    c_graph, c_tips = st.columns([2.5, 1])

    with c_graph:
        st.subheader("📈 Comportamento Ambiental (Suavizado)")
        
        if variaveis_selecionadas:
            # Usa as variáveis selecionadas no filtro lateral
            df_smooth = df_filtered.set_index('timestamp')[variaveis_selecionadas].rolling(window=12, min_periods=1).mean().reset_index()
            
            fig = px.line(df_smooth, x='timestamp', y=variaveis_selecionadas, 
                          color_discrete_map=COLORS["chart_colors"], # Usa o mapa de cores fixo
                          template="plotly_white")
            
            fig.update_layout(height=350, xaxis_title=None, yaxis_title="Valor", legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Selecione pelo menos um sensor na barra lateral para visualizar o gráfico.")

    with c_tips:
        st.subheader("🤖 Recomendações")
        for dica in dicas:
            if "✅" in dica: st.success(dica)
            elif "❄️" in dica or "🔥" in dica: st.warning(dica)
            elif "🌵" in dica or "💧" in dica: st.info(dica)
            else: st.error(dica)
            
        st.caption("ℹ️ Dicas ajustadas para a cultura selecionada.")

    # --- ABAS INFERIORES ---
    st.divider()
    t1, t2, t3 = st.tabs(["📊 Comparativo Mensal", "🧬 Nutrientes (NPK)", "🔬 Dados Brutos"])

    with t1:
        if variaveis_selecionadas:
            df_m = df_filtered.set_index('timestamp')[variaveis_selecionadas].resample('ME').mean().reset_index()
            df_m['mes'] = df_m['timestamp'].dt.strftime('%b/%Y')
            
            fig_m = px.bar(df_m, x='mes', y=variaveis_selecionadas, barmode='group',
                           color_discrete_map=COLORS["chart_colors"],
                           template="plotly_white")
            st.plotly_chart(fig_m, use_container_width=True)
        else:
            st.info("Selecione sensores para ver o comparativo mensal.")

    with t2:
        cols_npk = ['nitrogenio', 'fosforo', 'potassio']
        if all(c in df_filtered.columns for c in cols_npk):
            df_npk = df_filtered[cols_npk].mean().reset_index()
            df_npk.columns = ['Elemento', 'Valor']
            df_npk['Elemento'] = df_npk['Elemento'].map({'nitrogenio': 'Nitrogênio (N)', 'fosforo': 'Fósforo (P)', 'potassio': 'Potássio (K)'})
            
            fig_npk = px.bar(df_npk, x='Elemento', y='Valor', color='Elemento', text_auto='.0f',
                             color_discrete_sequence=["#66BB6A", "#FFEE58", "#8D6E63"], template="plotly_white")
            fig_npk.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_npk, use_container_width=True)
        else:
            st.info("Sensores NPK desconectados.")

    with t3:
        st.dataframe(df_filtered.sort_values('timestamp', ascending=False).head(100), use_container_width=True)