import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard Balcão The Hill",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Dashboard Balcão The Hill")

# Carregar dados
@st.cache_data
def load_data():
    df_balcao = pd.read_excel('Balcão.xlsx')
    df_balcao['Data'] = pd.to_datetime(df_balcao['Data'])
    
    df_clientes = pd.read_excel('Clientes.xlsx')
    df_assessores = pd.read_excel('Assessores.xlsx')
    
    return df_balcao, df_clientes, df_assessores

try:
    df_balcao, df_clientes, df_assessores = load_data()
    
    # Sidebar - Filtros
    st.sidebar.header("Filtros")
    
    # Filtro de data
    min_date = df_balcao['Data'].min().date()
    max_date = df_balcao['Data'].max().date()
    
    date_range = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df_balcao[
            (df_balcao['Data'].dt.date >= start_date) & 
            (df_balcao['Data'].dt.date <= end_date)
        ]
    else:
        df_filtered = df_balcao
    
    # Filtro de assessor
    assessores = ['Todos'] + sorted(df_filtered['Assessor'].unique().tolist())
    assessor_selecionado = st.sidebar.selectbox("Assessor", assessores)
    
    if assessor_selecionado != 'Todos':
        df_filtered = df_filtered[df_filtered['Assessor'] == assessor_selecionado]
    
    # Filtro de cliente
    clientes = ['Todos'] + sorted(df_filtered['Cliente'].unique().tolist())
    cliente_selecionado = st.sidebar.selectbox("Cliente", clientes)
    
    if cliente_selecionado != 'Todos':
        df_filtered = df_filtered[df_filtered['Cliente'] == cliente_selecionado]
    
    # Filtro de produto
    produtos = ['Todos'] + sorted(df_filtered['Produto'].unique().tolist())
    produto_selecionado = st.sidebar.selectbox("Produto", produtos)
    
    if produto_selecionado != 'Todos':
        df_filtered = df_filtered[df_filtered['Produto'] == produto_selecionado]
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_volume = df_filtered['Volume'].sum()
        st.metric("Volume Total", f"R$ {total_volume:,.2f}")
    
    with col2:
        total_operacoes = len(df_filtered)
        st.metric("Total de Operações", f"{total_operacoes:,}")
    
    with col3:
        ticket_medio = df_filtered['Volume'].mean() if len(df_filtered) > 0 else 0
        st.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    
    with col4:
        total_clientes = df_filtered['Cliente'].nunique()
        st.metric("Clientes Ativos", f"{total_clientes:,}")
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Volume por Assessor")
        volume_assessor = df_filtered.groupby('Assessor')['Volume'].sum().sort_values(ascending=True)
        fig1 = px.bar(
            x=volume_assessor.values,
            y=volume_assessor.index,
            orientation='h',
            labels={'x': 'Volume (R$)', 'y': 'Assessor'},
            color=volume_assessor.values,
            color_continuous_scale='Blues'
        )
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Volume por Produto")
        volume_produto = df_filtered.groupby('Produto')['Volume'].sum()
        fig2 = px.pie(
            values=volume_produto.values,
            names=volume_produto.index,
            hole=0.4
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Evolução temporal
    st.subheader("Evolução do Volume ao Longo do Tempo")
    df_temporal = df_filtered.groupby(df_filtered['Data'].dt.date)['Volume'].sum().reset_index()
    fig3 = px.line(
        df_temporal,
        x='Data',
        y='Volume',
        labels={'Volume': 'Volume (R$)', 'Data': 'Data'}
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Top clientes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Clientes por Volume")
        top_clientes = df_filtered.groupby('Cliente')['Volume'].sum().sort_values(ascending=False).head(10)
        fig4 = px.bar(
            x=top_clientes.values,
            y=top_clientes.index,
            orientation='h',
            labels={'x': 'Volume (R$)', 'y': 'Cliente'},
            color=top_clientes.values,
            color_continuous_scale='Greens'
        )
        fig4.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição de Operações por Produto")
        ops_produto = df_filtered['Produto'].value_counts()
        fig5 = px.bar(
            x=ops_produto.index,
            y=ops_produto.values,
            labels={'x': 'Produto', 'y': 'Quantidade de Operações'},
            color=ops_produto.values,
            color_continuous_scale='Oranges'
        )
        fig5.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig5, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Dados Detalhados")
    st.dataframe(
        df_filtered.sort_values('Data', ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Estatísticas adicionais
    st.divider()
    st.subheader("Estatísticas Adicionais")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Assessores", df_filtered['Assessor'].nunique())
        st.metric("Total de Produtos", df_filtered['Produto'].nunique())
    
    with col2:
        volume_max = df_filtered['Volume'].max()
        st.metric("Maior Operação", f"R$ {volume_max:,.2f}")
        volume_min = df_filtered['Volume'].min()
        st.metric("Menor Operação", f"R$ {volume_min:,.2f}")
    
    with col3:
        mediana = df_filtered['Volume'].median()
        st.metric("Mediana de Volume", f"R$ {mediana:,.2f}")
        desvio = df_filtered['Volume'].std()
        st.metric("Desvio Padrão", f"R$ {desvio:,.2f}")

except FileNotFoundError as e:
    st.error(f"Erro ao carregar arquivos: {e}")
    st.info("Certifique-se de que os arquivos Balcão.xlsx, Clientes.xlsx e Assessores.xlsx estão na mesma pasta do dashboard.")
except Exception as e:
    st.error(f"Erro inesperado: {e}")