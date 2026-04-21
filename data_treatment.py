import pandas as pd
import os

# Configurações opcionais de exibição
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)

# ==========================================
# 1. FUNÇÕES AUXILIARES (Correções Universais)
# ==========================================

def standardize_columns(df):
    """Remove espaços em branco e converte todos os nomes de colunas para minúsculas."""
    df.columns = df.columns.str.strip().str.lower()
    return df

def clean_text_column(series):
    """Remove espaços em branco, quebras de linha e converte o texto para minúsculas."""
    return series.fillna('').astype(str).str.strip().str.lower().str.replace('\n', ' ')

# ==========================================
# 2. FUNÇÕES DE LIMPEZA ESPECÍFICAS POR TABELA
# ==========================================

def clean_clientes(df):
    df = standardize_columns(df)
    
    # Trata o problema específico de dupla codificação nos nomes das cidades
    df['cidade'] = df['cidade'].fillna('')
    try:
        df['cidade'] = df['cidade'].str.encode('latin1').str.decode('utf-8')
    except Exception:
        pass # Se já estiver corrigido na origem, isso ignora o erro
    
    df['cidade'] = df['cidade'].str.strip().str.title()
    df['email'] = df['email'].fillna('').str.strip().str.lower()
    
    # Formatação e exclusões de nulos/vazios
    df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], errors='coerce')
    df = df.dropna(subset=['id', 'email'])
    df = df[df['email'] != '']
    df['id'] = df['id'].astype(int)

    # Renomeando colunas para maior clareza e para evitar confusão no merge
    df = df.rename(columns={
        'id': 'cliente_id_pk',
        'nome': 'nome_cliente'
    })
    
    return df.drop_duplicates(subset=['cliente_id_pk'], keep='last')

def clean_pedidos(df):
    df = standardize_columns(df)
    df = df.dropna(subset=['id', 'cliente_id', 'data_pedido'])
    
    df['id'] = df['id'].astype(int)
    df['cliente_id'] = df['cliente_id'].astype(int)
    df['data_pedido'] = pd.to_datetime(df['data_pedido'], errors='coerce')
    df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')
    
    df['status'] = clean_text_column(df['status'])
    df['canal_venda'] = clean_text_column(df['canal_venda'])
    
    # Converte 'sim'/'não' para Booleano (Verdadeiro/Falso)
    df['cupom_desconto'] = df['cupom_desconto'].str.strip().str.lower() == 'sim'
    
    # Renomeando colunas para maior clareza
    df = df.rename(columns={'id': 'pedido_id_pk'})

    return df.drop_duplicates(subset=['pedido_id_pk'], keep='last')

def clean_itens(df):
    df = standardize_columns(df)
    df = df.dropna(subset=['id', 'pedido_id', 'produto_id'])
    
    # Trata descontos ausentes preenchendo com zero
    df['desconto_aplicado'] = df['desconto_aplicado'].fillna(0.0)
    
    df['id'] = df['id'].astype(int)
    df['pedido_id'] = df['pedido_id'].astype(int)
    df['produto_id'] = df['produto_id'].astype(int)
    df['quantidade'] = df['quantidade'].astype(int)
    
    df['preco_praticado'] = pd.to_numeric(df['preco_praticado'], errors='coerce')
    df['desconto_aplicado'] = pd.to_numeric(df['desconto_aplicado'], errors='coerce')
    
    # Restrições lógicas
    df = df[df['quantidade'] > 0]
    df = df[df['preco_praticado'] >= 0]
    
    # Renomeando colunas para maior clareza
    df = df.rename(columns={'id': 'item_id_pk'})

    return df.drop_duplicates(subset=['item_id_pk'], keep='last')

def clean_produtos(df):
    df = standardize_columns(df)
    df = df.dropna(subset=['id'])
    
    df['id'] = df['id'].astype(int)
    
    df['categoria'] = df['categoria'].fillna('desconhecido').str.strip().str.lower()
    df['subcategoria'] = df['subcategoria'].fillna('desconhecido').str.strip().str.lower()
    df['fornecedor'] = df['fornecedor'].fillna('desconhecido').str.strip()
    df['nome'] = df['nome'].fillna('').str.strip()
    
    df['preco_unitario'] = pd.to_numeric(df['preco_unitario'], errors='coerce')
    df['custo_unitario'] = pd.to_numeric(df['custo_unitario'], errors='coerce')
    
    # Restrições lógicas
    df = df[(df['preco_unitario'] >= 0) & (df['custo_unitario'] >= 0)]
    
    # Renomeando colunas para maior clareza e para evitar confusão no merge
    df = df.rename(columns={
        'id': 'produto_id_pk',
        'nome': 'nome_produto',
        'categoria': 'categoria_produto',
        'subcategoria': 'subcategoria_produto',
        'fornecedor': 'fornecedor_produto'
    })

    return df.drop_duplicates(subset=['produto_id_pk'], keep='last')

def clean_avaliacoes(df):
    df = standardize_columns(df)
    df = df.dropna(subset=['id', 'pedido_id', 'produto_id', 'cliente_id'])
    
    df['id'] = df['id'].astype(int)
    df['pedido_id'] = df['pedido_id'].astype(int)
    df['produto_id'] = df['produto_id'].astype(int)
    df['cliente_id'] = df['cliente_id'].astype(int)
    
    # Limpa a avaliação e impõe a escala de 1 a 5
    df['nota'] = pd.to_numeric(df['nota'], errors='coerce').fillna(0).astype(int)
    df = df[df['nota'].between(1, 5)]
    
    df['data_avaliacao'] = pd.to_datetime(df['data_avaliacao'], errors='coerce')
    df['comentario'] = clean_text_column(df['comentario'])
    
    # Renomeando colunas para maior clareza
    df = df.rename(columns={'id': 'avaliacao_id_pk'})

    return df.drop_duplicates(subset=['avaliacao_id_pk'], keep='last')

def clean_tickets(df):
    df = standardize_columns(df)
    df = df.dropna(subset=['id', 'pedido_id', 'cliente_id'])
    
    df['id'] = df['id'].astype(int)
    df['pedido_id'] = df['pedido_id'].astype(int)
    df['cliente_id'] = df['cliente_id'].astype(int)
    
    df['data_abertura'] = pd.to_datetime(df['data_abertura'], errors='coerce')
    df['data_resolucao'] = pd.to_datetime(df['data_resolucao'], errors='coerce')
    
    df['categoria_problema'] = clean_text_column(df['categoria_problema'])
    df['status'] = clean_text_column(df['status'])
    
    # Verificação Lógica: Mantém se a data de resolução estiver ausente OU for válida (>= abertura)
    valido = df['data_resolucao'].isna() | (df['data_resolucao'] >= df['data_abertura'])
    df = df[valido]
    
    # Renomeando colunas para maior clareza
    df = df.rename(columns={'id': 'ticket_id_pk'})

    return df.drop_duplicates(subset=['ticket_id_pk'], keep='last')


# ==========================================
# 3. MOTOR DE EXECUÇÃO PRINCIPAL
# ==========================================

def load_and_clean_all(bases_path="./Bases Case Digital"):
    """Carrega os dados brutos, executa o pipeline de limpeza e retorna os DataFrames limpos."""
    print("Carregando dados brutos...")
    raw_clientes = pd.read_csv(os.path.join(bases_path, "clientes.csv"), encoding="utf-8")
    raw_pedidos = pd.read_csv(os.path.join(bases_path, "pedidos.csv"), encoding="utf-8")
    raw_itens = pd.read_csv(os.path.join(bases_path, "itens_pedido.csv"), encoding="utf-8")
    raw_produtos = pd.read_csv(os.path.join(bases_path, "produtos.csv"), encoding="utf-8")
    raw_avaliacoes = pd.read_csv(os.path.join(bases_path, "avaliacoes.csv"), encoding="utf-8")
    raw_tickets = pd.read_csv(os.path.join(bases_path, "tickets_suporte.csv"), encoding="utf-8")
    
    print("Executando pipeline de limpeza...")
    df_clientes = clean_clientes(raw_clientes)
    df_pedidos = clean_pedidos(raw_pedidos)
    df_itens = clean_itens(raw_itens)
    df_produtos = clean_produtos(raw_produtos)
    df_avaliacoes = clean_avaliacoes(raw_avaliacoes)
    df_tickets = clean_tickets(raw_tickets)
    
    print("Pipeline concluído! Todos os dataframes foram limpos com sucesso e estão prontos para análise.")
    
    # Retorna os dataframes como uma tupla
    return df_clientes, df_pedidos, df_itens, df_produtos, df_avaliacoes, df_tickets

# ==========================================
# 4. TESTE LOCAL
# ==========================================

if __name__ == "__main__":
    # Este bloco só é executado se você rodar este arquivo específico diretamente.
    # Ele NÃO será executado quando você importar a função em outro arquivo.
    
    clientes, pedidos, itens, produtos, avaliacoes, tickets = load_and_clean_all()
    
    print(clientes.info())
    print("-----------------------------------")

    print(pedidos.info())
    print("-----------------------------------")

    print(itens.info())
    print("-----------------------------------")

    print(produtos.info())
    print("-----------------------------------")

    print(avaliacoes.info())
    print("-----------------------------------")

    print(tickets.info())
    print("-----------------------------------")