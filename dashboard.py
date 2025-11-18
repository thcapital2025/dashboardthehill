import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime
import os
import dash_auth

BASE_PATH = r"C:\Users\Tratamento de dados\OneDrive\Compartilhada\Projeto - Balcão The Hill\Cofing"
ARQUIVO_BASE_BI = os.path.join(BASE_PATH, "Base BI.xlsx")

def carregar_dados():
    try:
        print(f"Tentando carregar arquivo: {ARQUIVO_BASE_BI}")
        if not os.path.exists(ARQUIVO_BASE_BI):
            print(f"ERRO: Arquivo não encontrado em {ARQUIVO_BASE_BI}")
            return pd.DataFrame()
        
        df = pd.read_excel(ARQUIVO_BASE_BI)
        print(f"Dados carregados com sucesso! Total de linhas: {len(df)}")
        print(f"Colunas encontradas: {list(df.columns)}")
        df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'], format='%d/%m/%Y', errors='coerce').dt.date
        df = df.reset_index(drop=False)
        df = df.rename(columns={'index': 'row_id'})
        return df
    except Exception as e:
        print(f"ERRO ao carregar dados: {str(e)}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()
    except Exception as e:
        print(f"[ERRO] Falha ao carregar dados: {str(e)}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

df = carregar_dados()

COLUNAS_TABELA_OPORTUNIDADES = [
    {'name': 'Assessor', 'id': 'Assessor'},
    {'name': 'Conta + Nome', 'id': 'Conta + Nome'},
    {'name': 'Ativo', 'id': 'Ativo'},
    {'name': 'Descrição', 'id': 'Descrição'},
    {'name': 'Data Vencimento', 'id': 'Data Vencimento'},
    {'name': 'Disponibilidade', 'id': 'Valor Total Curva', 'type': 'numeric', 'format': {'specifier': ',.2f', 'locale': {'symbol': ['R$ ', '']}}},
    {'name': 'Taxa Mercado', 'id': 'Taxa Mercado', 'type': 'numeric', 'format': {'specifier': '.2%'}},
    {'name': 'Deságio A Mercado', 'id': 'Deságio A Mercado', 'type': 'numeric', 'format': {'specifier': ',.2f', 'locale': {'symbol': ['R$ ', '']}}},
    {'name': 'Taxa Anbima', 'id': 'Taxa Anbima', 'type': 'numeric', 'format': {'specifier': '.2%'}},
    {'name': 'Túnel MIN.', 'id': 'Túnel MIN.', 'type': 'numeric', 'format': {'specifier': '.2%'}},
    {'name': 'Túnel MAX.', 'id': 'Túnel MAX.', 'type': 'numeric', 'format': {'specifier': '.2%'}},
    {'name': 'Deságio Balcão', 'id': 'Deságio Balcão', 'type': 'numeric', 'format': {'specifier': ',.2f', 'locale': {'symbol': ['R$ ', '']}}},
    {'name': 'Receita Max.', 'id': 'Receita Max.', 'type': 'numeric', 'format': {'specifier': ',.2f', 'locale': {'symbol': ['R$ ', '']}}},
    {'name': 'FEE', 'id': 'FEE', 'type': 'numeric', 'format': {'specifier': '.2%'}},
    {'name': 'Auditoria', 'id': 'Auditoria', 'presentation': 'markdown'}
]

COLUNAS_TABELA_BALCAO = [
    {'name': 'Assessor', 'id': 'Assessor'},
    {'name': 'Conta + Nome', 'id': 'Conta + Nome'},
    {'name': 'Ativo', 'id': 'Ativo'},
    {'name': 'Descrição', 'id': 'Descrição'},
    {'name': 'Taxa Sugerida', 'id': 'Túnel MAX.', 'type': 'numeric', 'format': {'specifier': '.2%'}},
    {'name': 'Data Vencimento', 'id': 'Data Vencimento'},
    {'name': 'Disponibilidade', 'id': 'Valor Total Curva', 'type': 'numeric', 'format': {'specifier': ',.2f', 'locale': {'symbol': ['R$ ', '']}}},
    {'name': 'FEE', 'id': 'FEE', 'type': 'numeric', 'format': {'specifier': '.2%'}}
]

STYLE_COLORS = {
    'primary': '#C5A04A',
    'background_dark': '#023d2e',
    'background_medium': '#034f3a',
    'background_light': '#046A4B',
    'text_white': '#ffffff',
    'text_gray': '#a0a0a0'
}

CSS_CUSTOM = f'''
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Cinzel:wght@400;600&display=swap');

.Select-control {{
    background-color: {STYLE_COLORS['background_medium']} !important;
    border: 1.5px solid {STYLE_COLORS['primary']} !important;
    color: {STYLE_COLORS['text_white']} !important;
    border-radius: 8px !important;
}}
.Select-menu-outer {{
    background-color: {STYLE_COLORS['background_medium']} !important;
    border: 1.5px solid {STYLE_COLORS['primary']} !important;
    border-radius: 8px !important;
}}
.Select-option {{
    background-color: {STYLE_COLORS['background_medium']} !important;
    color: {STYLE_COLORS['text_white']} !important;
}}
.Select-option:hover {{
    background-color: {STYLE_COLORS['background_light']} !important;
    color: {STYLE_COLORS['primary']} !important;
}}
.Select-value-label {{
    color: {STYLE_COLORS['text_white']} !important;
}}
.Select-placeholder {{
    color: {STYLE_COLORS['text_gray']} !important;
}}
.Select-input > input {{
    color: {STYLE_COLORS['text_white']} !important;
}}

.modal-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}}

.modal-content {{
    background-color: {STYLE_COLORS['background_medium']};
    border: 2px solid {STYLE_COLORS['primary']};
    border-radius: 12px;
    padding: 30px;
    max-width: 800px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 40px rgba(197, 160, 74, 0.3);
}}
'''

app = dash.Dash(__name__, suppress_callback_exceptions=True)

VALID_USERNAME_PASSWORD_PAIRS = {
    'antonio': 'Thc@1234',
    'vinicius': 'Thc@1234',
    'alcir': 'Thc@1234'
}

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server

app.index_string = f'''
<!DOCTYPE html>
<html>
<head>
{{%metas%}}
<title>{{%title%}}</title>
{{%favicon%}}
{{%css%}}
<style>{CSS_CUSTOM}</style>
</head>
<body>
{{%app_entry%}}
<footer>
{{%config%}}
{{%scripts%}}
{{%renderer%}}
</footer>
</body>
</html>
'''

app.layout = html.Div([
    html.Div([
        html.H1("THE HILL CAPITAL", style={
            'color': STYLE_COLORS['primary'],
            'fontSize': 38,
            'fontWeight': '600',
            'fontFamily': 'Cinzel, serif',
            'letterSpacing': '3px',
            'marginBottom': 5,
            'textTransform': 'uppercase',
            'textAlign': 'center'
        }),
        html.Div("BALCÃO DE ATIVOS", style={
            'color': STYLE_COLORS['text_white'],
            'fontSize': 16,
            'fontFamily': 'Montserrat, sans-serif',
            'letterSpacing': '2px',
            'fontWeight': '400',
            'textAlign': 'center'
        })
    ], style={'marginBottom': 30, 'paddingTop': 20}),
    
    dcc.Tabs(id='tabs-principal', value='oportunidades', children=[
        dcc.Tab(label='Oportunidades', value='oportunidades', style={
            'backgroundColor': STYLE_COLORS['background_medium'],
            'color': STYLE_COLORS['text_white'],
            'border': f"1.5px solid {STYLE_COLORS['primary']}",
            'borderRadius': '8px 8px 0 0',
            'padding': '15px 40px',
            'fontFamily': 'Montserrat, sans-serif',
            'fontWeight': '600',
            'fontSize': 14
        }, selected_style={
            'backgroundColor': STYLE_COLORS['primary'],
            'color': STYLE_COLORS['background_dark'],
            'border': f"1.5px solid {STYLE_COLORS['primary']}",
            'borderRadius': '8px 8px 0 0',
            'padding': '15px 40px',
            'fontFamily': 'Montserrat, sans-serif',
            'fontWeight': '700',
            'fontSize': 14
        }),
        dcc.Tab(label='Balcão', value='balcao', style={
            'backgroundColor': STYLE_COLORS['background_medium'],
            'color': STYLE_COLORS['text_white'],
            'border': f"1.5px solid {STYLE_COLORS['primary']}",
            'borderRadius': '8px 8px 0 0',
            'padding': '15px 40px',
            'fontFamily': 'Montserrat, sans-serif',
            'fontWeight': '600',
            'fontSize': 14
        }, selected_style={
            'backgroundColor': STYLE_COLORS['primary'],
            'color': STYLE_COLORS['background_dark'],
            'border': f"1.5px solid {STYLE_COLORS['primary']}",
            'borderRadius': '8px 8px 0 0',
            'padding': '15px 40px',
            'fontFamily': 'Montserrat, sans-serif',
            'fontWeight': '700',
            'fontSize': 14
        })
    ], style={'marginBottom': 30, 'padding': '0 30px'}),
    
    html.Div(id='conteudo-tabs'),
    
    html.Div(id='modal-auditoria', style={'display': 'none'}, children=[
        html.Div(className='modal-overlay', children=[
            html.Div(className='modal-content', children=[
                html.H3("Auditoria do Ativo", style={'color': STYLE_COLORS['primary'], 'fontFamily': 'Montserrat, sans-serif', 'marginBottom': 20}),
                html.Div(id='modal-body', style={'color': STYLE_COLORS['text_white'], 'fontFamily': 'Montserrat, sans-serif', 'marginBottom': 20}),
                html.Button("Fechar", id="fechar-modal", n_clicks=0, style={
                    'backgroundColor': STYLE_COLORS['primary'],
                    'color': STYLE_COLORS['background_dark'],
                    'border': 'none',
                    'padding': '10px 30px',
                    'borderRadius': '8px',
                    'fontSize': 14,
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'fontFamily': 'Montserrat, sans-serif'
                })
            ])
        ])
    ]),
    
    html.Div([
        html.Div("THE HILL CAPITAL", style={
            'color': STYLE_COLORS['primary'],
            'fontSize': 16,
            'fontFamily': 'Cinzel, serif',
            'letterSpacing': '2px',
            'fontWeight': '600',
            'display': 'inline-block',
            'marginRight': '30px'
        }),
        html.Div("O zelo e a segurança dos seus investimentos", style={
            'color': STYLE_COLORS['text_white'],
            'fontSize': 13,
            'fontFamily': 'Montserrat, sans-serif',
            'fontWeight': '400',
            'display': 'inline-block'
        })
    ], style={'textAlign': 'center', 'marginTop': 50, 'paddingBottom': 30}),
    
    dcc.Store(id='store-df-completo', data=df.to_dict('records') if not df.empty else []),
    dcc.Store(id='store-balcao', data=[]),
    dcc.Store(id='store-selected-oportunidades', data=[]),
    dcc.Store(id='store-selected-balcao', data=[])
], style={
    'fontFamily': 'Montserrat, sans-serif',
    'padding': '30px',
    'backgroundColor': STYLE_COLORS['background_dark'],
    'minHeight': '100vh'
})

@app.callback(
    Output('conteudo-tabs', 'children'),
    Input('tabs-principal', 'value')
)
def render_conteudo_tab(tab):
    if tab == 'oportunidades':
        return html.Div([
            html.Div([
                html.Div([
                    html.Label("Selecione o Assessor:", style={
                        'fontWeight': '600',
                        'fontSize': 13,
                        'color': STYLE_COLORS['primary'],
                        'marginBottom': 10,
                        'fontFamily': 'Montserrat, sans-serif'
                    }),
                    dcc.Dropdown(
                        id='filtro-assessor',
                        options=[{'label': a, 'value': a} for a in sorted(df['Assessor'].dropna().unique())] if not df.empty else [],
                        placeholder="Selecione um assessor..."
                    )
                ], style={
                    'backgroundColor': STYLE_COLORS['background_medium'],
                    'padding': '25px',
                    'borderRadius': '12px',
                    'border': f"1.5px solid {STYLE_COLORS['primary']}",
                    'width': '32%',
                    'display': 'inline-block',
                    'marginRight': '1%'
                }),
                
                html.Div([
                    html.Label("Selecione o Cliente:", style={
                        'fontWeight': '600',
                        'fontSize': 13,
                        'color': STYLE_COLORS['primary'],
                        'marginBottom': 10,
                        'fontFamily': 'Montserrat, sans-serif'
                    }),
                    dcc.Dropdown(
                        id='filtro-cliente',
                        options=[],
                        placeholder="Selecione um cliente..."
                    )
                ], style={
                    'backgroundColor': STYLE_COLORS['background_medium'],
                    'padding': '25px',
                    'borderRadius': '12px',
                    'border': f"1.5px solid {STYLE_COLORS['primary']}",
                    'width': '32%',
                    'display': 'inline-block',
                    'marginRight': '1%'
                }),
                
                html.Div([
                    html.Label("Buscar Ativo:", style={
                        'fontWeight': '600',
                        'fontSize': 13,
                        'color': STYLE_COLORS['primary'],
                        'marginBottom': 10,
                        'fontFamily': 'Montserrat, sans-serif'
                    }),
                    dcc.Input(
                        id='busca-ativo',
                        type='text',
                        placeholder='Digite o código do ativo...',
                        style={
                            'width': '100%',
                            'padding': '12px',
                            'fontSize': 14,
                            'backgroundColor': STYLE_COLORS['background_medium'],
                            'color': STYLE_COLORS['text_white'],
                            'border': f"1.5px solid {STYLE_COLORS['primary']}",
                            'borderRadius': '8px',
                            'fontFamily': 'Montserrat, sans-serif'
                        }
                    )
                ], style={
                    'backgroundColor': STYLE_COLORS['background_medium'],
                    'padding': '25px',
                    'borderRadius': '12px',
                    'border': f"1.5px solid {STYLE_COLORS['primary']}",
                    'width': '32%',
                    'display': 'inline-block'
                })
            ], style={'marginBottom': 45, 'padding': '0 30px'}),
            
            html.Div([
                html.Button("Transferir Selecionados para Balcão", id='btn-transferir', n_clicks=0, style={
                    'backgroundColor': STYLE_COLORS['primary'],
                    'color': STYLE_COLORS['background_dark'],
                    'border': 'none',
                    'padding': '15px 40px',
                    'borderRadius': '8px',
                    'fontSize': 14,
                    'fontWeight': '700',
                    'cursor': 'pointer',
                    'fontFamily': 'Montserrat, sans-serif',
                    'letterSpacing': '1px',
                    'textTransform': 'uppercase',
                    'boxShadow': '0 4px 15px rgba(197, 160, 74, 0.3)'
                })
            ], style={'textAlign': 'center', 'marginBottom': 30, 'padding': '0 30px'}),
            
            html.Div([
                dash_table.DataTable(
                    id='tabela-oportunidades',
                    columns=COLUNAS_TABELA_OPORTUNIDADES,
                    data=[],
                    row_selectable='multi',
                    selected_rows=[],
                    style_table={'overflowX': 'auto', 'backgroundColor': STYLE_COLORS['background_dark'], 'borderRadius': '12px'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '15px',
                        'fontSize': 13,
                        'fontFamily': 'Montserrat, sans-serif',
                        'backgroundColor': STYLE_COLORS['background_medium'],
                        'color': STYLE_COLORS['text_white'],
                        'border': f"1px solid {STYLE_COLORS['background_light']}"
                    },
                    style_header={
                        'backgroundColor': STYLE_COLORS['background_dark'],
                        'color': STYLE_COLORS['primary'],
                        'fontWeight': '700',
                        'textAlign': 'center',
                        'border': f"1.5px solid {STYLE_COLORS['primary']}",
                        'textTransform': 'uppercase',
                        'letterSpacing': '1px',
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontSize': 12,
                        'padding': '18px'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': STYLE_COLORS['background_light']},
                        {'if': {'state': 'active'}, 'backgroundColor': '#056B4C', 'border': f"1.5px solid {STYLE_COLORS['primary']}"}
                    ],
                    sort_action='native',
                    page_size=20
                )
            ], style={
                'padding': '0 30px',
                'backgroundColor': STYLE_COLORS['background_dark'],
                'borderRadius': '12px',
                'boxShadow': '0 6px 25px rgba(0, 0, 0, 0.3)',
                'border': f"1.5px solid {STYLE_COLORS['primary']}",
                'margin': '0 30px'
            })
        ])
    else:
        return html.Div([
            html.Div([
                html.H3("BALCÃO - Ativos Transferidos", style={
                    'color': STYLE_COLORS['primary'],
                    'fontSize': 18,
                    'fontWeight': '700',
                    'padding': '0 30px',
                    'fontFamily': 'Montserrat, sans-serif'
                })
            ], style={'marginBottom': 20}),
            
            html.Div([
                html.Button("Remover Selecionados", id='btn-remover', n_clicks=0, style={
                    'backgroundColor': '#8B0000',
                    'color': STYLE_COLORS['text_white'],
                    'border': 'none',
                    'padding': '15px 40px',
                    'borderRadius': '8px',
                    'fontSize': 14,
                    'fontWeight': '700',
                    'cursor': 'pointer',
                    'fontFamily': 'Montserrat, sans-serif',
                    'letterSpacing': '1px',
                    'textTransform': 'uppercase',
                    'boxShadow': '0 4px 15px rgba(139, 0, 0, 0.3)'
                })
            ], style={'textAlign': 'center', 'marginBottom': 30, 'padding': '0 30px'}),
            
            html.Div([
                dash_table.DataTable(
                    id='tabela-balcao',
                    columns=COLUNAS_TABELA_BALCAO,
                    data=[],
                    row_selectable='multi',
                    selected_rows=[],
                    style_table={'overflowX': 'auto', 'backgroundColor': STYLE_COLORS['background_dark'], 'borderRadius': '12px'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '15px',
                        'fontSize': 13,
                        'fontFamily': 'Montserrat, sans-serif',
                        'backgroundColor': STYLE_COLORS['background_medium'],
                        'color': STYLE_COLORS['text_white'],
                        'border': f"1px solid {STYLE_COLORS['background_light']}"
                    },
                    style_header={
                        'backgroundColor': STYLE_COLORS['background_dark'],
                        'color': STYLE_COLORS['primary'],
                        'fontWeight': '700',
                        'textAlign': 'center',
                        'border': f"1.5px solid {STYLE_COLORS['primary']}",
                        'textTransform': 'uppercase',
                        'letterSpacing': '1px',
                        'fontFamily': 'Montserrat, sans-serif',
                        'fontSize': 12,
                        'padding': '18px'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': STYLE_COLORS['background_light']},
                        {'if': {'state': 'active'}, 'backgroundColor': '#056B4C', 'border': f"1.5px solid {STYLE_COLORS['primary']}"}
                    ],
                    sort_action='native',
                    page_size=20
                )
            ], style={
                'padding': '0 30px',
                'backgroundColor': STYLE_COLORS['background_dark'],
                'borderRadius': '12px',
                'boxShadow': '0 6px 25px rgba(0, 0, 0, 0.3)',
                'border': f"1.5px solid {STYLE_COLORS['primary']}",
                'margin': '0 30px'
            })
        ])

@app.callback(
    Output('store-selected-oportunidades', 'data'),
    Input('tabela-oportunidades', 'selected_rows')
)
def salvar_selecao_oportunidades(selected_rows):
    return selected_rows if selected_rows else []

@app.callback(
    Output('store-selected-balcao', 'data'),
    Input('tabela-balcao', 'selected_rows')
)
def salvar_selecao_balcao(selected_rows):
    return selected_rows if selected_rows else []

@app.callback(
    Output('filtro-cliente', 'options'),
    Input('filtro-assessor', 'value'),
    State('store-df-completo', 'data')
)
def atualizar_clientes_por_assessor(assessor, dados):
    if not dados:
        return []
    df_local = pd.DataFrame(dados)
    if assessor:
        clientes = sorted(df_local[df_local['Assessor'] == assessor]['Conta + Nome'].dropna().unique())
    else:
        clientes = sorted(df_local['Conta + Nome'].dropna().unique())
    return [{'label': c, 'value': c} for c in clientes]

@app.callback(
    Output('tabela-oportunidades', 'data'),
    Input('filtro-assessor', 'value'),
    Input('filtro-cliente', 'value'),
    Input('busca-ativo', 'value'),
    State('store-df-completo', 'data')
)
def atualizar_tabela_oportunidades(assessor, cliente, busca_ativo, dados):
    if not dados:
        return []
    df_local = pd.DataFrame(dados)
    if assessor:
        df_local = df_local[df_local['Assessor'] == assessor]
    if cliente:
        df_local = df_local[df_local['Conta + Nome'] == cliente]
    if busca_ativo:
        termo = str(busca_ativo).strip().lower()
        mask = df_local['Ativo'].astype(str).str.lower().str.contains(termo)
        df_local = df_local[mask]
    if 'Data Vencimento' in df_local.columns:
        df_local['Data Vencimento'] = df_local['Data Vencimento'].apply(
            lambda x: x.strftime('%d/%m/%Y') if hasattr(x, 'strftime') else (str(x) if pd.notnull(x) else ''))
    df_local['Auditoria'] = '📋 Ver'
    return df_local.to_dict('records')

@app.callback(
    [Output('store-balcao', 'data'),
     Output('tabela-oportunidades', 'selected_rows')],
    Input('btn-transferir', 'n_clicks'),
    [State('store-selected-oportunidades', 'data'),
     State('tabela-oportunidades', 'data'),
     State('store-balcao', 'data')],
    prevent_initial_call=True
)
def transferir_para_balcao(n_clicks, selected_rows, data_oportunidades, balcao_data):
    if not selected_rows or not data_oportunidades:
        raise dash.exceptions.PreventUpdate
    
    df_oportunidades = pd.DataFrame(data_oportunidades)
    selecionados = df_oportunidades.iloc[selected_rows].to_dict('records')
    
    if balcao_data:
        df_balcao = pd.DataFrame(balcao_data)
        df_novo = pd.concat([df_balcao, pd.DataFrame(selecionados)], ignore_index=True)
    else:
        df_novo = pd.DataFrame(selecionados)
    
    if all(c in df_novo.columns for c in ['Ativo', 'Conta + Nome', 'Data Vencimento']):
        df_novo = df_novo.drop_duplicates(subset=['Ativo', 'Conta + Nome', 'Data Vencimento'])
    
    return df_novo.to_dict('records'), []

@app.callback(
    Output('tabela-balcao', 'data'),
    Input('store-balcao', 'data')
)
def atualizar_tabela_balcao(dados_balcao):
    if not dados_balcao:
        return []
    df_local = pd.DataFrame(dados_balcao)
    if 'Data Vencimento' in df_local.columns:
        df_local['Data Vencimento'] = df_local['Data Vencimento'].apply(
            lambda x: x.strftime('%d/%m/%Y') if hasattr(x, 'strftime') else (str(x) if pd.notnull(x) else ''))
    
    colunas_balcao = ['Assessor', 'Conta + Nome', 'Ativo', 'Descrição', 'Túnel MAX.', 'Data Vencimento', 'Valor Total Curva', 'FEE']
    colunas_existentes = [col for col in colunas_balcao if col in df_local.columns]
    df_local = df_local[colunas_existentes]
    
    return df_local.to_dict('records')

@app.callback(
    [Output('store-balcao', 'data', allow_duplicate=True),
     Output('tabela-balcao', 'selected_rows')],
    Input('btn-remover', 'n_clicks'),
    [State('store-selected-balcao', 'data'),
     State('store-balcao', 'data')],
    prevent_initial_call=True
)
def remover_do_balcao(n_clicks, selected_rows, balcao_data):
    if not selected_rows or not balcao_data:
        raise dash.exceptions.PreventUpdate
    
    df_balcao = pd.DataFrame(balcao_data)
    df_balcao = df_balcao.drop(df_balcao.index[selected_rows]).reset_index(drop=True)
    
    return df_balcao.to_dict('records'), []

@app.callback(
    Output("modal-auditoria", "style"),
    Input('tabela-oportunidades', 'active_cell'),
    Input("fechar-modal", "n_clicks"),
    State("modal-auditoria", "style"),
    State('tabela-oportunidades', 'data'),
    prevent_initial_call=True
)
def toggle_modal(active_cell, n_clicks, current_style, data):
    ctx = callback_context
    if not ctx.triggered:
        return {'display': 'none'}

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'tabela-oportunidades' and active_cell and active_cell['column_id'] == 'Auditoria':
        return {'display': 'block'}
    elif trigger_id == 'fechar-modal':
        return {'display': 'none'}

    return current_style if current_style else {'display': 'none'}

@app.callback(
    Output('modal-body', 'children'),
    Input('tabela-oportunidades', 'active_cell'),
    State('tabela-oportunidades', 'data'),
    State('store-df-completo', 'data'),
    prevent_initial_call=True
)
def atualizar_modal(active_cell, data_tabela, df_completo_dict):
    if active_cell and active_cell['column_id'] == 'Auditoria' and df_completo_dict and data_tabela:
        row_tabela = data_tabela[active_cell['row']]
        row_id = row_tabela.get('row_id')

        if row_id is None:
            return "Dados não disponíveis."

        df_completo = pd.DataFrame(df_completo_dict)
        matching_rows = df_completo[df_completo['row_id'] == row_id]

        if matching_rows.empty:
            return "Dados não encontrados."

        row_completa = matching_rows.iloc[0]

        conta = row_completa.get('Conta', 'N/A')
        ativo = row_completa.get('Ativo', 'N/A')
        emissor = row_completa.get('Emissor', 'N/A')
        tipo = row_completa.get('Tipo', 'N/A')
        indexador = row_completa.get('Indexador', 'N/A')
        taxa_compra = row_completa.get('Taxa Compra', 0)
        data_vencimento_raw = row_completa.get('Data Vencimento')
        valor_total_mercado = row_completa.get('Valor Total Mercado', 0)

        if pd.notnull(data_vencimento_raw) and hasattr(data_vencimento_raw, 'strftime'):
            data_vencimento = data_vencimento_raw.strftime('%d/%m/%Y')
        else:
            data_vencimento = str(data_vencimento_raw) if data_vencimento_raw else 'N/A'

        taxa_compra_formatada = f"{taxa_compra * 100:.2f}%" if pd.notnull(taxa_compra) else 'N/A'
        valor_total_mercado_formatado = f"R$ {valor_total_mercado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notnull(valor_total_mercado) else 'N/A'

        texto_auditoria = f"""Para darmos continuidade às movimentações em sua conta BTG, solicito sua autorização neste e-mail. Abaixo seguem os detalhes das operações:

Conta: {conta}
Ativo: {ativo}
Emissor: {emissor}
Tipo: {tipo}
Indexador: {indexador}
Taxa Compra: {taxa_compra_formatada}
Data Vencimento: {data_vencimento}
Saldo Bruto Aprox.: {valor_total_mercado_formatado}

Atenciosamente"""

        return html.Pre(texto_auditoria, style={'whiteSpace': 'pre-wrap', 'lineHeight': '1.8', 'fontSize': 14})

    return "Selecione um item para ver os detalhes."

if __name__ == '__main__':
    app.run(debug=True, port=8050)