import streamlit as st
import pandas as pd
from datetime import datetime
import os
import hashlib

st.set_page_config(
    page_title="THE HILL CAPITAL - Balcão de Ativos",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

STYLE_COLORS = {
    'primary': '#C5A04A',
    'background_dark': '#023d2e',
    'background_medium': '#034f3a',
    'background_light': '#046A4B',
    'text_white': '#ffffff',
    'text_gray': '#a0a0a0'
}

USUARIOS = {
    'antonio': 'Thc@1234',
    'vinicius': 'Thc@1234',
    'alcir': 'Thc@1234'
}

def verificar_login(usuario, senha):
    return usuario in USUARIOS and USUARIOS[usuario] == senha

def tela_login():
    st.markdown(f"""
    <div style='text-align: center; margin-top: 100px; margin-bottom: 50px;'>
        <h1 style='color: {STYLE_COLORS["primary"]}; font-size: 48px; font-weight: 600; 
                   font-family: Cinzel, serif; letter-spacing: 3px; margin-bottom: 10px; 
                   text-transform: uppercase;'>THE HILL CAPITAL</h1>
        <div style='color: {STYLE_COLORS["text_white"]}; font-size: 18px; 
                    font-family: Montserrat, sans-serif; letter-spacing: 2px; font-weight: 400;'>
            BALCÃO DE ATIVOS
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style='background-color: {STYLE_COLORS["background_medium"]}; 
                    padding: 40px; border-radius: 12px; 
                    border: 2px solid {STYLE_COLORS["primary"]}; 
                    box-shadow: 0 4px 20px rgba(197, 160, 74, 0.2);'>
            <h3 style='color: {STYLE_COLORS["primary"]}; text-align: center; 
                       font-family: Montserrat, sans-serif; margin-bottom: 30px;'>
                🔐 LOGIN
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        usuario = st.text_input("👤 Usuário", key="login_usuario")
        senha = st.text_input("🔑 Senha", type="password", key="login_senha")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("ENTRAR", use_container_width=True, type="primary"):
                if verificar_login(usuario, senha):
                    st.session_state.autenticado = True
                    st.session_state.usuario_logado = usuario
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Cinzel:wght@400;600&display=swap');
        
        .stApp {{
            background-color: {STYLE_COLORS['background_dark']};
            font-family: 'Montserrat', sans-serif;
        }}
        
        h1, h2, h3 {{
            font-family: 'Cinzel', serif;
            color: {STYLE_COLORS['primary']};
        }}
        
        .stTextInput > div > div > input {{
            background-color: {STYLE_COLORS['background_light']};
            color: {STYLE_COLORS['text_white']};
            border: 1px solid {STYLE_COLORS['primary']};
        }}
        
        .stButton > button {{
            background-color: {STYLE_COLORS['primary']};
            color: {STYLE_COLORS['background_dark']};
            font-weight: 600;
            border: none;
            padding: 12px;
            font-family: 'Montserrat', sans-serif;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    tela_login()
    st.stop()

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Cinzel:wght@400;600&display=swap');
    
    .stApp {{
        background-color: {STYLE_COLORS['background_dark']};
        font-family: 'Montserrat', sans-serif;
    }}
    
    h1, h2, h3 {{
        font-family: 'Cinzel', serif;
        color: {STYLE_COLORS['primary']};
    }}
    
    .stSelectbox, .stTextInput {{
        background-color: {STYLE_COLORS['background_medium']};
    }}
    
    .stDataFrame {{
        background-color: {STYLE_COLORS['background_medium']};
    }}
    
    div[data-testid="stMetricValue"] {{
        color: {STYLE_COLORS['primary']};
        font-size: 32px;
        font-weight: 700;
    }}
    
    div[data-testid="stMetricLabel"] {{
        color: {STYLE_COLORS['text_gray']};
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel('Base BI.xlsx')
        df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'], format='%d/%m/%Y', errors='coerce')
        df = df.reset_index(drop=False)
        df = df.rename(columns={'index': 'row_id'})
        return df
    except:
        return pd.DataFrame()

if 'df_balcao' not in st.session_state:
    st.session_state.df_balcao = carregar_dados()

if 'df_disponibilidade' not in st.session_state:
    st.session_state.df_disponibilidade = pd.DataFrame()

if 'selecionados_balcao' not in st.session_state:
    st.session_state.selecionados_balcao = []

if 'selecionados_disponibilidade' not in st.session_state:
    st.session_state.selecionados_disponibilidade = []

col_header1, col_header2 = st.columns([0.9, 0.1])

with col_header1:
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 50px; padding-top: 20px;'>
        <h1 style='color: {STYLE_COLORS["primary"]}; font-size: 38px; font-weight: 600; 
                   font-family: Cinzel, serif; letter-spacing: 3px; margin-bottom: 5px; 
                   text-transform: uppercase;'>THE HILL CAPITAL</h1>
        <div style='color: {STYLE_COLORS["text_white"]}; font-size: 16px; 
                    font-family: Montserrat, sans-serif; letter-spacing: 2px; font-weight: 400;'>
            BALCÃO DE ATIVOS
        </div>
        <div style='color: {STYLE_COLORS["primary"]}; font-size: 13px; font-weight: 600; 
                    margin-top: 20px;'>
            Última atualização: {datetime.now().strftime('%d/%m - %H:%M')}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 20px;'>
        <div style='color: {STYLE_COLORS["text_white"]}; font-size: 12px; margin-bottom: 5px;'>
            👤 {st.session_state.usuario_logado}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Sair", type="secondary"):
        st.session_state.autenticado = False
        st.session_state.usuario_logado = None
        st.rerun()

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    assessores = [''] + sorted(st.session_state.df_balcao['Assessor'].dropna().unique().tolist()) if not st.session_state.df_balcao.empty else ['']
    assessor_selecionado = st.selectbox("🔹 SELECIONE O ASSESSOR", assessores, key='assessor')

with col2:
    if assessor_selecionado:
        clientes = [''] + sorted(st.session_state.df_balcao[st.session_state.df_balcao['Assessor'] == assessor_selecionado]['Conta + Nome'].dropna().unique().tolist())
    else:
        clientes = ['']
    cliente_selecionado = st.selectbox("🔹 SELECIONE O CLIENTE", clientes, key='cliente')

with col3:
    busca_ativo = st.text_input("🔹 BUSCAR ATIVO", placeholder="Digite o código do ativo...")

df_filtrado = st.session_state.df_balcao.copy()

if assessor_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Assessor'] == assessor_selecionado]

if cliente_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Conta + Nome'] == cliente_selecionado]

if busca_ativo:
    df_filtrado = df_filtrado[df_filtrado['Ativo'].str.contains(busca_ativo, case=False, na=False)]

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Balcão", "✅ Disponibilidade"])

with tab1:
    st.markdown("### Balcão de Ativos")
    
    if not df_filtrado.empty:
        colunas_exibir = ['Assessor', 'Conta + Nome', 'Ativo', 'Descrição', 'Data Vencimento',
                          'Valor Total Curva', 'Taxa Mercado', 'Deságio A Mercado', 'Taxa Anbima', 
                          'Túnel MIN.', 'Túnel MAX.', 'Deságio Balcão', 'Receita Max.', 'FEE']
        
        colunas_disponiveis = [col for col in colunas_exibir if col in df_filtrado.columns]
        df_exibir = df_filtrado[['row_id'] + colunas_disponiveis].copy()
        
        if 'Data Vencimento' in df_exibir.columns:
            df_exibir['Data Vencimento'] = df_exibir['Data Vencimento'].dt.strftime('%d/%m/%Y')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for idx, row in df_exibir.iterrows():
            col_check, col_dados = st.columns([0.05, 0.95])
            
            with col_check:
                checkbox_key = f"balcao_{row['row_id']}"
                if st.checkbox("", key=checkbox_key, label_visibility="collapsed"):
                    if row['row_id'] not in st.session_state.selecionados_balcao:
                        st.session_state.selecionados_balcao.append(row['row_id'])
                else:
                    if row['row_id'] in st.session_state.selecionados_balcao:
                        st.session_state.selecionados_balcao.remove(row['row_id'])
            
            with col_dados:
                row_display = row.drop('row_id').to_dict()
                st.dataframe(pd.DataFrame([row_display]), hide_index=True, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("➡️ Transferir Selecionados para Disponibilidade", type="primary"):
            if st.session_state.selecionados_balcao:
                linhas_transferir = st.session_state.df_balcao[st.session_state.df_balcao['row_id'].isin(st.session_state.selecionados_balcao)]
                
                if st.session_state.df_disponibilidade.empty:
                    st.session_state.df_disponibilidade = linhas_transferir.copy()
                else:
                    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, linhas_transferir], ignore_index=True)
                
                st.session_state.df_balcao = st.session_state.df_balcao[~st.session_state.df_balcao['row_id'].isin(st.session_state.selecionados_balcao)]
                st.session_state.selecionados_balcao = []
                st.success(f"✅ {len(linhas_transferir)} linha(s) transferida(s) para Disponibilidade!")
                st.rerun()
            else:
                st.warning("⚠️ Nenhuma linha selecionada!")
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("🔍 VER AUDITORIA DE ATIVO SELECIONADO"):
        if not df_filtrado.empty and 'row_id' in df_filtrado.columns:
            ativos_opcoes = df_filtrado.apply(
                lambda row: f"{row['Ativo']} - {row['Conta + Nome']}" if 'Ativo' in row and 'Conta + Nome' in row else str(row.get('Ativo', '')), 
                axis=1
            ).tolist()
            
            ativo_selecionado = st.selectbox("Selecione um ativo:", [''] + ativos_opcoes)
            
            if ativo_selecionado:
                idx = ativos_opcoes.index(ativo_selecionado)
                row_completa = df_filtrado.iloc[idx]
                
                campos_auditoria = {
                    'Conta': row_completa.get('Conta', 'N/A'),
                    'Ativo': row_completa.get('Ativo', 'N/A'),
                    'Emissor': row_completa.get('Emissor', 'N/A'),
                    'Tipo': row_completa.get('Tipo', 'N/A'),
                    'Indexador': row_completa.get('Indexador', 'N/A'),
                    'Taxa Compra': f"{row_completa.get('Taxa Compra', 0) * 100:.2f}%" if 'Taxa Compra' in row_completa else 'N/A',
                    'Data Vencimento': pd.to_datetime(row_completa.get('Data Vencimento')).strftime('%d/%m/%Y') if 'Data Vencimento' in row_completa else 'N/A',
                    'Saldo Bruto Aprox.': f"R$ {row_completa.get('Valor Total Mercado', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if 'Valor Total Mercado' in row_completa else 'N/A'
                }
                
                texto_auditoria = f"""Para darmos continuidade às movimentações em sua conta BTG, solicito sua autorização neste e-mail. Abaixo seguem os detalhes das operações:

Conta: {campos_auditoria['Conta']}
Ativo: {campos_auditoria['Ativo']}
Emissor: {campos_auditoria['Emissor']}
Tipo: {campos_auditoria['Tipo']}
Indexador: {campos_auditoria['Indexador']}
Taxa Compra: {campos_auditoria['Taxa Compra']}
Data Vencimento: {campos_auditoria['Data Vencimento']}
Saldo Bruto Aprox.: {campos_auditoria['Saldo Bruto Aprox.']}

Atenciosamente"""
                
                st.text_area("Texto da Auditoria:", texto_auditoria, height=300)

with tab2:
    st.markdown("### Disponibilidade")
    
    if not st.session_state.df_disponibilidade.empty:
        colunas_disponibilidade = ['Conta + Nome', 'Descrição', 'Valor Total Curva', 'Túnel MIN.', 'Túnel MAX.', 'Receita Max.', 'FEE']
        colunas_disponiveis = [col for col in colunas_disponibilidade if col in st.session_state.df_disponibilidade.columns]
        df_disp_exibir = st.session_state.df_disponibilidade[['row_id'] + colunas_disponiveis].copy()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for idx, row in df_disp_exibir.iterrows():
            col_check, col_dados = st.columns([0.05, 0.95])
            
            with col_check:
                checkbox_key = f"disp_{row['row_id']}"
                if st.checkbox("", key=checkbox_key, label_visibility="collapsed"):
                    if row['row_id'] not in st.session_state.selecionados_disponibilidade:
                        st.session_state.selecionados_disponibilidade.append(row['row_id'])
                else:
                    if row['row_id'] in st.session_state.selecionados_disponibilidade:
                        st.session_state.selecionados_disponibilidade.remove(row['row_id'])
            
            with col_dados:
                row_display = row.drop('row_id').to_dict()
                st.dataframe(pd.DataFrame([row_display]), hide_index=True, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🗑️ Remover Selecionados", type="secondary"):
            if st.session_state.selecionados_disponibilidade:
                linhas_remover = len(st.session_state.selecionados_disponibilidade)
                st.session_state.df_disponibilidade = st.session_state.df_disponibilidade[~st.session_state.df_disponibilidade['row_id'].isin(st.session_state.selecionados_disponibilidade)]
                st.session_state.selecionados_disponibilidade = []
                st.success(f"✅ {linhas_remover} linha(s) removida(s)!")
                st.rerun()
            else:
                st.warning("⚠️ Nenhuma linha selecionada!")
    else:
        st.info("📋 Nenhum ativo em disponibilidade. Transfira ativos da aba Balcão.")

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align: center; margin-top: 50px; padding-bottom: 30px;'>
    <span style='color: {STYLE_COLORS["primary"]}; font-size: 16px; 
                 font-family: Cinzel, serif; letter-spacing: 2px; 
                 font-weight: 600; margin-right: 30px;'>
        THE HILL CAPITAL
    </span>
    <span style='color: {STYLE_COLORS["text_white"]}; font-size: 13px; 
                 font-family: Montserrat, sans-serif; font-weight: 400;'>
        O zelo e a segurança dos seus investimentos
    </span>
</div>
""", unsafe_allow_html=True)