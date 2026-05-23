# ============================================
# MEETING AI ASSISTANT
# STREAMLIT + GROQ
# ============================================
#
# Instalar:
# pip install streamlit groq
#
# Rodar:
# streamlit run app.py
#
# IMPORTANTE:
# Crie o arquivo:
# .streamlit/secrets.toml
#
# Conteúdo:
#
# GROQ_API_KEY = "sua_chave_aqui"
#
# ============================================

import streamlit as st
from groq import Groq
from datetime import datetime

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================

st.set_page_config(
    page_title="Meeting AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# CSS
# ============================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3, p, label {
    color: white;
}

.stTextArea textarea {
    background-color: #111827;
    color: white;
    border-radius: 12px;
    border: 1px solid #334155;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #111827;
    border-radius: 12px;
    border: 1px solid #334155;
}

.result-box {
    background: #111827;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #334155;
    line-height: 1.8;
    white-space: pre-wrap;
}

.metric-box {
    background: #111827;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #334155;
    text-align: center;
}

.metric-box h3 {
    color: #cbd5e1;
}

.metric-box h1 {
    font-size: 42px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# CHAVE GROQ (SECRETS)
# ============================================

try:

    api_key = st.secrets["GROQ_API_KEY"]

except:

    st.error("""
Erro: chave GROQ_API_KEY não encontrada.

Crie:

.streamlit/secrets.toml

E adicione:

GROQ_API_KEY = "sua_chave"
""")

    st.stop()

# ============================================
# CLIENTE GROQ
# ============================================

client = Groq(api_key=api_key)

# ============================================
# HEADER
# ============================================

st.title("🤖 Meeting AI Assistant")

st.markdown("""
Ferramenta inteligente para análise de reuniões utilizando IA.

### Recursos:
- Resumo automático
- Extração de tarefas
- Decisões importantes
- Plano de ação
- Próximos passos
- Organização profissional
""")

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.header("⚙️ Configurações")

    modelo = st.selectbox(
        "Modelo",
        [
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
    )

    temperatura = st.slider(
        "Criatividade",
        0.0,
        1.0,
        0.4
    )

# ============================================
# INPUT
# ============================================

st.subheader("📝 Transcrição da Reunião")

texto = st.text_area(
    "Cole a reunião abaixo:",
    height=350,
    placeholder="""
Exemplo:

João:
Precisamos melhorar o sistema de vendas.

Maria:
A equipe comercial precisa de um dashboard.

Carlos:
Vou entregar até sexta-feira.
"""
)

# ============================================
# BOTÕES
# ============================================

col1, col2, col3 = st.columns(3)

with col1:

    analisar = st.button(
        "🚀 Analisar Reunião",
        use_container_width=True
    )

with col2:

    limpar = st.button(
        "🧹 Limpar",
        use_container_width=True
    )

with col3:

    exportar = st.button(
        "📄 Exportar Relatório",
        use_container_width=True
    )

# ============================================
# LIMPAR
# ============================================

if limpar:
    st.rerun()

# ============================================
# ANÁLISE
# ============================================

if analisar:

    if not texto.strip():

        st.warning("Digite a reunião.")

        st.stop()

    with st.spinner("Analisando reunião com IA..."):

        try:

            prompt = f"""
Você é um especialista em reuniões corporativas.

Analise a reunião abaixo e gere:

1. RESUMO EXECUTIVO
2. PRINCIPAIS DECISÕES
3. TAREFAS IDENTIFICADAS
4. RESPONSÁVEIS
5. PRAZOS
6. RISCOS
7. PRÓXIMOS PASSOS
8. PLANO DE AÇÃO

Organize de forma clara e profissional.

REUNIÃO:
{texto}
"""

            resposta = client.chat.completions.create(

                model=modelo,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=temperatura

            )

            resultado = resposta.choices[0].message.content

            st.session_state["resultado"] = resultado

            # ============================================
            # MÉTRICAS
            # ============================================

            st.subheader("📊 Estatísticas")

            c1, c2, c3 = st.columns(3)

            with c1:

                st.markdown(f"""
                <div class="metric-box">
                    <h3>Palavras</h3>
                    <h1>{len(texto.split())}</h1>
                </div>
                """, unsafe_allow_html=True)

            with c2:

                st.markdown(f"""
                <div class="metric-box">
                    <h3>Caracteres</h3>
                    <h1>{len(texto)}</h1>
                </div>
                """, unsafe_allow_html=True)

            with c3:

                st.markdown(f"""
                <div class="metric-box">
                    <h3>Data</h3>
                    <h1>{datetime.now().strftime('%d/%m')}</h1>
                </div>
                """, unsafe_allow_html=True)

            # ============================================
            # RESULTADO
            # ============================================

            st.subheader("🤖 Resultado da IA")

            st.markdown(
                f"""
<div class="result-box">
{resultado}
</div>
                """,
                unsafe_allow_html=True
            )

        except Exception as erro:

            st.error(f"Erro: {erro}")

# ============================================
# EXPORTAR
# ============================================

if exportar:

    if "resultado" not in st.session_state:

        st.warning("Gere uma análise primeiro.")

    else:

        st.download_button(
            label="⬇️ Download Relatório",
            data=st.session_state["resultado"],
            file_name="relatorio_reuniao.txt",
            mime="text/plain",
            use_container_width=True
        )