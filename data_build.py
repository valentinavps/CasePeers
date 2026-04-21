import pandas as pd
from data_treatment import load_and_clean_all

# =========================================================
# CARREGAMENTO DOS DADOS
# =========================================================
# Carrega todos os datasets já limpos pelo pipeline de tratamento
clientes, pedidos, itens, produtos, avaliacoes, tickets = load_and_clean_all()

# =========================================================
# JOIN: ITENS + PRODUTOS
# =========================================================
# Junta os itens dos pedidos com os dados dos produtos
itens_produtos = pd.merge(
    itens,
    produtos,
    left_on='produto_id',
    right_on='produto_id_pk',
    how='left'
)

# =========================================================
# CÁLCULO DE MÉTRICAS POR ITEM
# =========================================================
# Valor bruto: preço de tabela * quantidade
itens_produtos['valor_bruto'] = itens_produtos['quantidade'] * itens_produtos['preco_unitario']

# Valor líquido: preço efetivo pago * quantidade
itens_produtos['valor_liquido'] = itens_produtos['quantidade'] * itens_produtos['preco_praticado']

# Desconto aplicado
itens_produtos['desconto'] = itens_produtos['valor_bruto'] - itens_produtos['valor_liquido']

# Valor Custo
itens_produtos['custo'] = itens_produtos['custo_unitario'] * itens_produtos['quantidade']

#Lucro
itens_produtos['lucro'] = itens_produtos['valor_liquido'] - itens_produtos['custo']
# =========================================================
# CONSTRUÇÃO DA FACT TABLE (VENDAS)
# =========================================================
# Junta pedidos com os itens enriquecidos com produtos
df_vendas = pd.merge(
    pedidos,
    itens_produtos,
    left_on='pedido_id_pk',
    right_on='pedido_id',
    how='left'
)

# Garantir formato correto da data
df_vendas['data_pedido'] = pd.to_datetime(df_vendas['data_pedido'])

# =========================================================
# JOIN: VENDAS + CLIENTES (ADICIONADO)
# =========================================================
# 1. Juntar os dados do cliente na fact table
df_vendas = pd.merge(
    df_vendas,
    clientes[['cliente_id_pk', 'nome_cliente', 'segmento', 'canal_aquisicao']], 
    left_on='cliente_id',
    right_on='cliente_id_pk', 
    how='left'
)

# =========================================================
# SELEÇÃO FINAL DA FACT TABLE
# =========================================================
df_vendas = df_vendas[[
    'pedido_id_pk',
    'data_pedido',
    'cliente_id',
    'nome_cliente',
    'segmento',
    'canal_aquisicao',
    'produto_id',
    'nome_produto',
    'quantidade',
    'categoria_produto',
    'subcategoria_produto',
    'fornecedor_produto',
    'custo_unitario',
    'preco_unitario',
    'preco_praticado',
    'desconto_aplicado',
    'valor_bruto',
    'valor_liquido',
    'custo',
    'lucro',
    'desconto',
    'status',
    'canal_venda'
]]

# =========================================================
# EXPORTAÇÃO DA FACT TABLE
# =========================================================
# Guarda o dataset pronto para análise
df_vendas.to_csv("fact_vendas.csv", index=False)

print("FACT TABLE criada com sucesso: fact_vendas.csv")

# =========================================================
# TICKETS + CLIENTES + PRODUTOS
# =========================================================

# 1. juntar tickets com clientes
df_tickets_full = pd.merge(
    tickets,
    clientes[['cliente_id_pk', 'nome_cliente']],
    left_on='cliente_id',
    right_on='cliente_id_pk',
    how='left'
)

# 2. trazer produtos via pedidos + itens
df_ticket_produto = pd.merge(
    df_tickets_full,
    pedidos[['pedido_id_pk']],
    left_on='pedido_id',
    right_on='pedido_id_pk',
    how='left'
)

df_ticket_produto = pd.merge(
    df_ticket_produto,
    itens[['pedido_id', 'produto_id']],
    left_on='pedido_id',
    right_on='pedido_id',
    how='left'
)

df_ticket_produto = pd.merge(
    df_ticket_produto,
    produtos[['produto_id_pk', 'nome_produto']],
    left_on='produto_id',
    right_on='produto_id_pk',
    how='left'
)

# =========================================================
# RESULTADO FINAL
# =========================================================
df_fact_tickets = df_ticket_produto[[
    'ticket_id_pk',
    'pedido_id',
    'cliente_id',
    'nome_cliente',
    'produto_id',
    'nome_produto',
    'categoria_problema',
    'data_abertura',
    'data_resolucao',
    'status'
]]

df_fact_tickets.to_csv("fact_tickets.csv", index=False)
print("FACT TABLE de Tickets criada com sucesso: fact_tickets.csv")

# =========================================================
# AVALIAÇÕES + CLIENTES + PRODUTOS
# =========================================================

df_avaliacoes_full = pd.merge(
    avaliacoes,
    clientes[['cliente_id_pk', 'nome_cliente']],
    left_on='cliente_id',
    right_on='cliente_id_pk',
    how='left'
)

df_avaliacoes_full = pd.merge(
    df_avaliacoes_full,
    produtos[['produto_id_pk', 'nome_produto']],
    left_on='produto_id',
    right_on='produto_id_pk',
    how='left'
)

# =========================================================
# RESULTADO FINAL
# =========================================================
df_fact_avaliacoes = df_avaliacoes_full[[
    'avaliacao_id_pk',
    'pedido_id',
    'cliente_id',
    'nome_cliente',
    'produto_id',
    'nome_produto',
    'nota',
    'comentario',
    'data_avaliacao'
]]

df_fact_avaliacoes.to_csv("fact_avaliacoes.csv", index=False)
print("FACT TABLE de Avaliações criada com sucesso: fact_avaliacoes.csv")