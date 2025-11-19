import streamlit as st
import pandas as pd
from datetime import datetime
import os

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

df = carregar_dados()

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

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    assessores = [''] + sorted(df['Assessor'].dropna().unique().tolist()) if not df.empty else ['']
    assessor_selecionado = st.selectbox("🔹 SELECIONE O ASSESSOR", assessores, key='assessor')

with col2:
    if assessor_selecionado:
        clientes = [''] + sorted(df[df['Assessor'] == assessor_selecionado]['Conta + Nome'].dropna().unique().tolist())
    else:
        clientes = ['']
    cliente_selecionado = st.selectbox("🔹 SELECIONE O CLIENTE", clientes, key='cliente')

with col3:
    busca_ativo = st.text_input("🔹 BUSCAR ATIVO", placeholder="Digite o código do ativo...")

df_filtrado = df.copy()

if assessor_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Assessor'] == assessor_selecionado]

if cliente_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Conta + Nome'] == cliente_selecionado]

if busca_ativo:
    df_filtrado = df_filtrado[df_filtrado['Ativo'].str.contains(busca_ativo, case=False, na=False)]

st.markdown("<br>", unsafe_allow_html=True)

potencial_receita = df_filtrado['Receita Max.'].sum() if not df_filtrado.empty and 'Receita Max.' in df_filtrado.columns else 0

col_kpi = st.columns(1)[0]
with col_kpi:
    st.markdown(f"""
    <div style='background-color: {STYLE_COLORS["background_medium"]}; 
                padding: 30px; border-radius: 12px; 
                border: 1.5px solid {STYLE_COLORS["primary"]}; 
                box-shadow: 0 4px 15px rgba(197, 160, 74, 0.15); 
                text-align: center;'>
        <div style='color: {STYLE_COLORS["text_gray"]}; font-size: 12px; 
                    letter-spacing: 1.5px; font-weight: 600; 
                    text-transform: uppercase; margin-bottom: 10px;'>
            POTENCIAL RECEITA
        </div>
        <div style='color: {STYLE_COLORS["primary"]}; font-size: 32px; 
                    font-weight: 700; letter-spacing: 1px;'>
            R$ {potencial_receita:,.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

if not df_filtrado.empty:
    colunas_exibir = ['Assessor', 'Conta + Nome', 'Ativo', 'Descrição', 'Data Vencimento',
                      'Valor Total Curva', 'Taxa Mercado', 'Deságio A Mercado', 'Taxa Anbima', 
                      'Túnel MIN.', 'Túnel MAX.', 'Deságio Balcão', 'Receita Max.', 'FEE']
    
    colunas_disponiveis = [col for col in colunas_exibir if col in df_filtrado.columns]
    df_exibir = df_filtrado[colunas_disponiveis].copy()
    
    if 'Data Vencimento' in df_exibir.columns:
        df_exibir['Data Vencimento'] = df_exibir['Data Vencimento'].dt.strftime('%d/%m/%Y')
    
    st.markdown(f"""
    <div style='background-color: {STYLE_COLORS["background_medium"]}; 
                padding: 20px; border-radius: 12px; 
                border: 1.5px solid {STYLE_COLORS["primary"]};'>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df_exibir,
        use_container_width=True,
        hide_index=True,
        height=600
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("🔍 VER AUDITORIA DE ATIVO SELECIONADO"):
        if 'row_id' in df_filtrado.columns:
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
else:
    st.warning("Nenhum dado disponível com os filtros selecionados.")

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