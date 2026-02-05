import pandas as pd
import os
from openpyxl import load_workbook
import numpy as np

def criar_base_bi(arquivo_base_geral, arquivo_cri_cra, arquivo_debenture, arquivo_base_btg, arquivo_ettj, output_path='Base BI.xlsx'):
    df_base = pd.read_excel(arquivo_base_geral, usecols=['Ativo', 'Conta', 'Tipo', 'Emissor', 'Indexador', 
                                                           'Taxa Compra', 'Data Vencimento', 'Valor Total Curva', 
                                                           'Valor Total Mercado', 'Taxa Mercado'])
    
    df_final = df_base[df_base['Tipo'].isin(['CRI', 'CRA', 'Debênture'])].copy()
    df_final['Conta'] = df_final['Conta'].astype(str).str.strip().str.lstrip('0')

    if pd.api.types.is_datetime64_any_dtype(df_final['Data Vencimento']):
        df_final['Data Vencimento'] = df_final['Data Vencimento'].dt.strftime('%d/%m/%Y')

    cri_cra_taxa_indicativa = {}
    cri_cra_duration = {}
    if os.path.exists(arquivo_cri_cra):
        encodings = ['latin-1', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                df_cri_cra = pd.read_csv(arquivo_cri_cra, sep=';', encoding=encoding)
                break
            except:
                continue
        else:
            df_cri_cra = pd.read_csv(arquivo_cri_cra, sep=',', encoding='latin-1')

        df_cri_cra.columns = df_cri_cra.columns.str.strip()
        df_cri_cra['Data de Referência'] = pd.to_datetime(df_cri_cra['Data de Referência'], format='%d/%m/%Y', errors='coerce')
        df_cri_cra = df_cri_cra.sort_values('Data de Referência', ascending=False).drop_duplicates(subset=[df_cri_cra.columns[5]], keep='first')

        cri_cra_taxa_indicativa = dict(zip(df_cri_cra.iloc[:, 5], df_cri_cra.iloc[:, 10]))
        cri_cra_duration = dict(zip(df_cri_cra.iloc[:, 5], df_cri_cra.iloc[:, 14]))

    df_debenture = pd.read_excel(arquivo_debenture, usecols=[0, 6, 12])
    debenture_taxa_indicativa = dict(zip(df_debenture.iloc[:, 0], df_debenture.iloc[:, 1]))
    debenture_duration = dict(zip(df_debenture.iloc[:, 0], df_debenture.iloc[:, 2]))

    df_base_btg = pd.read_excel(arquivo_base_btg, usecols=[0, 1, 2], dtype={0: str})
    df_base_btg.iloc[:, 0] = df_base_btg.iloc[:, 0].astype(str).str.strip().str.lstrip('0')
    assessor_dict = dict(zip(df_base_btg.iloc[:, 0], df_base_btg.iloc[:, 2]))
    nome_dict = dict(zip(df_base_btg.iloc[:, 0], df_base_btg.iloc[:, 1]))

    df_final['Assessor'] = df_final['Conta'].map(assessor_dict)
    df_final['Nome'] = df_final['Conta'].map(nome_dict)
    df_final['Conta + Nome'] = df_final['Conta'] + ' ' + df_final['Nome'].fillna('')
    
    df_final['Taxa Anbima'] = df_final['Ativo'].map(cri_cra_taxa_indicativa).fillna(df_final['Ativo'].map(debenture_taxa_indicativa))
    df_final['Taxa Anbima'] = pd.to_numeric(df_final['Taxa Anbima'].astype(str).str.replace(',', '.'), errors='coerce') / 100
    df_final = df_final.dropna(subset=['Taxa Anbima'])
    
    df_final['Túnel MIN.'] = df_final['Taxa Anbima'] - 0.0045
    df_final['Túnel MAX.'] = df_final['Taxa Anbima'] + 0.0045
    
    df_final['Duration'] = df_final['Ativo'].map(cri_cra_duration).fillna(df_final['Ativo'].map(debenture_duration))
    df_final['Duration'] = pd.to_numeric(df_final['Duration'].astype(str).str.replace(',', '.'), errors='coerce')
    
    df_ettj = pd.read_excel(arquivo_ettj, usecols=[0, 3])
    df_ettj.iloc[:, 0] = pd.to_numeric(df_ettj.iloc[:, 0], errors='coerce')
    df_ettj.iloc[:, 1] = pd.to_numeric(df_ettj.iloc[:, 1], errors='coerce')
    df_ettj = df_ettj.dropna().reset_index(drop=True)
    
    ettj_values = df_ettj.iloc[:, 1].values / 100
    duration_values = df_ettj.iloc[:, 0].values
    
    def buscar_ettj_vectorized(durations):
        result = np.empty(len(durations))
        for i, dur in enumerate(durations):
            if pd.isna(dur):
                result[i] = np.nan
            else:
                idx = np.abs(duration_values - dur).argmin()
                result[i] = ettj_values[idx]
        return result
    
    df_final['ETTJ'] = buscar_ettj_vectorized(df_final['Duration'].values)
    
    df_final['Descrição'] = (df_final['Tipo'] + ' ' + df_final['Emissor'] + ' ' + 
                              df_final['Indexador'] + ' ' + 
                              (df_final['Taxa Compra'] * 100).round(2).astype(str) + '%')
    
    df_final['Duration Anos'] = df_final['Duration'] / 252
    
    df_final = df_final.dropna(subset=['Taxa Mercado'])
    
    df_final['Valor Projetado'] = (((df_final['Duration'] / 252) * ((1 + df_final['Taxa Compra']) * (1 + df_final['ETTJ']) - 1)) * df_final['Valor Total Curva']) + df_final['Valor Total Curva']
    df_final['Delta Taxa'] = df_final['Túnel MAX.'] - df_final['Taxa Mercado']
    df_final['Variacao Percentual'] = -df_final['Duration Anos'] * df_final['Delta Taxa']
    df_final['Valor Total Balcão'] = df_final['Valor Total Mercado'] * (1 + df_final['Variacao Percentual'])
    df_final['Deságio A Mercado'] = df_final['Valor Total Mercado'] - df_final['Valor Total Curva']
    df_final['Deságio Balcão'] = df_final['Valor Total Balcão'] - df_final['Valor Total Curva']
    df_final['Receita Max.'] = (0.0045 * df_final['Duration Anos']) * df_final['Valor Total Curva']
    df_final['FEE'] = df_final['Receita Max.'] / df_final['Valor Total Curva']
    df_final['FEE Comprador'] = df_final['FEE'] * 0.85
    df_final['FEE Vendedor'] = df_final['FEE'] * 0.15
    
    df_final = df_final[df_final['Indexador'].str.contains(r'IPCA\+', na=False, regex=True)]
    
    df_final = df_final[['Assessor', 'Conta', 'Nome', 'Conta + Nome', 'Ativo', 'Descrição', 'Tipo', 'Emissor', 'Indexador', 
                         'Taxa Compra', 'Data Vencimento', 'Duration', 'ETTJ',
                         'Valor Total Curva', 'Valor Projetado', 'Taxa Mercado', 'Valor Total Mercado', 
                         'Deságio A Mercado', 'Taxa Anbima', 'Túnel MIN.', 'Túnel MAX.', 'Valor Total Balcão', 
                         'Deságio Balcão', 'Receita Max.', 'FEE', 'FEE Comprador', 'FEE Vendedor']]
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        for row in range(2, len(df_final) + 2):
            worksheet[f'B{row}'].number_format = '@'
    
    print("Spreadsheet ready for use")
    return df_final

if __name__ == "__main__":
    base_path = r"C:\Users\Produtos\OneDrive\Compartilhada\Projeto - Balcão The Hill\Cofing"
    arquivo_base_geral = f"{base_path}\\Base Geral - Detalhada.xlsx"
    arquivo_cri_cra = f"{base_path}\\precos-cri-cra.csv"
    arquivo_debenture = f"{base_path}\\Debênture.xlsx"
    arquivo_base_btg = f"{base_path}\\Base BTG.xlsx"
    arquivo_ettj = f"{base_path}\\ETTJ.xlsx"
    
    criar_base_bi(arquivo_base_geral, arquivo_cri_cra, arquivo_debenture, arquivo_base_btg, arquivo_ettj, f"{base_path}\\Base BI.xlsx")