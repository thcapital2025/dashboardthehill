import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Balcão The Hill",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Balcão The Hill")

@st.cache_data
def load_data():
    df = pd.read_excel('Base BI.xlsx')
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'])
    return df

try:
    df = load_data()
    
    st.sidebar.header("Filtros")
    
    if 'Data' in df.columns:
        min_date = df['Data'].min().date()
        max_date = df['Data'].max().date()
        
        date_range = st.sidebar.date_input(
            "Período",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df[
                (df['Data'].dt.date >= start_date) & 
                (df['Data'].dt.date <= end_date)
            ]
        else:
            df_filtered = df
    else:
        df_filtered = df
    
    if 'Assessor' in df_filtered.columns:
        assessores = ['Todos'] + sorted(df_filtered['Assessor'].dropna().unique().tolist())
        assessor_selecionado = st.sidebar.selectbox("Assessor", assessores)
        
        if assessor_selecionado != 'Todos':
            df_filtered = df_filtered[df_filtered['Assessor'] == assessor_selecionado]
    
    if 'Cliente' in df_filtered.columns:
        clientes = ['Todos'] + sorted(df_filtered['Cliente'].dropna().unique().tolist())
        cliente_selecionado = st.sidebar.selectbox("Cliente", clientes)
        
        if cliente_selecionado != 'Todos':
            df_filtered = df_filtered[df_filtered['Cliente'] == cliente_selecionado]
    
    if 'Produto' in df_filtered.columns:
        produtos = ['Todos'] + sorted(df_filtered['Produto'].dropna().unique().tolist())
        produto_selecionado = st.sidebar.selectbox("Produto", produtos)
        
        if produto_selecionado != 'Todos':
            df_filtered = df_filtered[df_filtered['Produto'] == produto_selecionado]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Volume' in df_filtered.columns:
            total_volume = df_filtered['Volume'].sum()
            st.metric("Volume Total", f"R$ {total_volume:,.2f}")
    
    with col2:
        total_operacoes = len(df_filtered)
        st.metric("Total de Operações", f"{total_operacoes:,}")
    
    with col3:
        if 'Volume' in df_filtered.columns:
            ticket_medio = df_filtered['Volume'].mean() if len(df_filtered) > 0 else 0
            st.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    
    with col4:
        if 'Cliente' in df_filtered.columns:
            total_clientes = df_filtered['Cliente'].nunique()
            st.metric("Clientes Ativos", f"{total_clientes:,}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Assessor' in df_filtered.columns and 'Volume' in df_filtered.columns:
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
        if 'Produto' in df_filtered.columns and 'Volume' in df_filtered.columns:
            st.subheader("Volume por Produto")
            volume_produto = df_filtered.groupby('Produto')['Volume'].sum()
            fig2 = px.pie(
                values=volume_produto.values,
                names=volume_produto.index,
                hole=0.4
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    if 'Data' in df_filtered.columns and 'Volume' in df_filtered.columns:
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Cliente' in df_filtered.columns and 'Volume' in df_filtered.columns:
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
        if 'Produto' in df_filtered.columns:
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
    
    st.subheader("Dados Detalhados")
    if 'Data' in df_filtered.columns:
        st.dataframe(
            df_filtered.sort_values('Data', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

except FileNotFoundError as e:
    st.error(f"Erro ao carregar arquivo: {e}")
    st.info("Certifique-se de que o arquivo Base BI.xlsx está na mesma pasta do dashboard.")
except Exception as e:
    st.error(f"Erro inesperado: {e}")