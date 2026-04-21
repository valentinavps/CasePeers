import os
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from data_treatment import load_and_clean_all  

df_clientes, df_pedidos, df_itens, df_produtos, df_avaliacoes, df_tickets = load_and_clean_all()
# =========================================================
# CARREGAMENTO DA FACT TABLE
# =========================================================
# Lê a fact table gerada no pipeline de construção
base_path = "Fact Tables"

df_vendas = pd.read_csv(os.path.join(base_path, "fact_vendas.csv"))
df_avaliacoes = pd.read_csv(os.path.join(base_path, "fact_avaliacoes.csv"))
df_tickets = pd.read_csv(os.path.join(base_path, "fact_tickets.csv"))

# Conversão de datas para formato datetime
df_vendas['data_pedido'] = pd.to_datetime(df_vendas['data_pedido'])

import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# DISTRIBUIÇÃO DE PEDIDOS POR STATUS
# =========================================================

# Contagem de pedidos por status
status_counts = (
    df_vendas['status']
    .value_counts()
    .reset_index()
)

status_counts.columns = ['status', 'total_pedidos']

# Percentagem
status_counts['percentagem'] = (
    status_counts['total_pedidos'] / status_counts['total_pedidos'].sum()
) * 100

# Ordenar
status_counts = status_counts.sort_values('total_pedidos', ascending=False)

print("\nDISTRIBUIÇÃO DE PEDIDOS POR STATUS:\n")
print(status_counts)

# Gráfico de barras
plt.figure(figsize=(9,5))

bars = plt.bar(
    status_counts['status'],
    status_counts['total_pedidos']
)

plt.title('Volume de Pedidos por Status')
plt.xlabel('Status do Pedido')
plt.ylabel('Número de Pedidos')

plt.xticks(rotation=45)

for bar, pct in zip(bars, status_counts['percentagem']):
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f'{pct:.1f}%',
        ha='center',
        va='bottom'
    )

plt.tight_layout()
plt.show()
plt.savefig('pedidos_por_status.png')

# =========================================================
# TOP PRODUTOS
# =========================================================
# Análise de produtos mais vendidos e com maior receita
top_produtos = (
    df_vendas
    .groupby(['produto_id', 'nome_produto'], as_index=False)
    .agg(
        total_quantidade=('quantidade', 'sum'),
        receita_total=('valor_liquido', 'sum')
    )
    .sort_values('total_quantidade', ascending=False)
    .head(10)
)

print("\nTOP 10 PRODUTOS:\n")
print(top_produtos)

# =========================================================
# ANÁLISE MENSAL
# =========================================================
# Agrupamento por mês para análise de tendência temporal
df_vendas['ano_mes'] = df_vendas['data_pedido'].dt.to_period('M')

resumo_mensal = (
    df_vendas
    .groupby('ano_mes', as_index=False)
    .agg(
        total_itens=('quantidade', 'sum'),
        receita_total=('valor_liquido', 'sum'),
        total_descontos=('desconto', 'sum')
    )
    .sort_values('ano_mes')
)

print("\nRESUMO MENSAL:\n")
print(resumo_mensal)

# =========================================================
# ANÁLISE POR CANAL E CLIENTES
# =========================================================

# Identificação de pedidos cancelados
df_vendas['cancelado'] = df_vendas['status'].str.lower().str.contains('cancelado')

# =========================================================
# TICKET MÉDIO POR CANAL
# =========================================================
ticket_medio = (
    df_vendas
    .groupby('canal_aquisicao', as_index=False)
    .agg(
        ticket_medio=('valor_liquido', 'mean'),
        receita_total=('valor_liquido', 'sum'),
        total_pedidos=('valor_liquido', 'count')
    )
    .sort_values('ticket_medio', ascending=False)
)

print("\nTICKET MÉDIO POR CANAL:\n")
print(ticket_medio)

# =========================================================
# TICKET MÉDIO POR SEGMENTO
# =========================================================
ticket_segmento = (
    df_vendas
    .groupby('segmento', as_index=False)
    .agg(
        ticket_medio=('valor_liquido', 'mean'),
        total_pedidos=('valor_liquido', 'count'),
        receita_total=('valor_liquido', 'sum')
    )
)

print("\nTICKET MÉDIO POR SEGMENTO:\n")
print(ticket_segmento)

# =========================================================
# TESTE ESTATÍSTICO: B2C vs B2B
# =========================================================
# Comparação estatística entre segmentos de clientes

b2c = df_vendas[df_vendas['segmento'] == 'B2C']['valor_liquido'].dropna()
b2b = df_vendas[df_vendas['segmento'] == 'B2B']['valor_liquido'].dropna()

t_stat, p_value = stats.ttest_ind(b2c, b2b, equal_var=False)

print("\nTESTE ESTATÍSTICO B2C vs B2B")
print("T-stat:", t_stat)
print("P-value:", p_value)

# =========================================================
# TAXA DE CANCELAMENTO POR CANAL
# =========================================================
cancelamento = (
    df_vendas
    .groupby('canal_aquisicao', as_index=False)
    .agg(
        total_pedidos=('pedido_id_pk', 'count'),
        pedidos_cancelados=('cancelado', 'sum')
    )
)

cancelamento['taxa_cancelamento'] = (
    cancelamento['pedidos_cancelados'] / cancelamento['total_pedidos']
) * 100

print("\nCANCELAMENTO POR CANAL:\n")
print(cancelamento)

# =========================================================
# EXTRA
# =========================================================
#Produtos com melhores avaliacoes
top_avaliados = (
    df_avaliacoes
    .groupby(['produto_id', 'nome_produto'], as_index=False)
    .agg(
        media_avaliacao=('nota', 'mean'),
        total_avaliacoes=('nota', 'count')
    )
    .sort_values('media_avaliacao', ascending=False)
    .head(10)
)
print("\nTOP 10 PRODUTOS MAIS AVALIADOS:\n")
print(top_avaliados)

#Produtos com mais tickets de suporte
top_tickets = (
    df_tickets
    .groupby(['produto_id', 'nome_produto'], as_index=False)
    .agg(
        total_tickets=('ticket_id_pk', 'count')
    )
    .sort_values('total_tickets', ascending=False)
    .head(10)
)
print("\nTOP 10 PRODUTOS COM MAIS TICKETS:\n")
print(top_tickets)

