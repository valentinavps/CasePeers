# 📊 Data Analytics Pipeline — E-commerce Sales Project

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

---

## 🧠 Visão Geral do Projeto

Este projeto implementa um pipeline completo de **Data Engineering + Data Analytics** aplicado a um cenário de e-commerce.

O objetivo é transformar dados brutos em estruturas analíticas e gerar **insights acionáveis de negócio**, incluindo:

- desempenho de vendas
- comportamento de clientes
- análise de produtos
- suporte ao cliente (tickets)
- satisfação (avaliações)

---

# 🏗️ Estrutura do Projeto

O projeto está dividido em 3 módulos principais:

- `data_treatment.py` → limpeza e preparação
- `data_build.py` → modelação e criação de fact tables
- `analysis.py` → análises e insights

---

# 🧹 1. data_treatment.py (Camada de Limpeza)

## 🎯 Objetivo
Preparar os dados brutos para análise.

## ⚙️ O que faz:
- limpeza e normalização
- tratamento de nulos
- conversão de tipos
- padronização de colunas

## 📌 Output:
- `df_clientes`
- `df_pedidos`
- `df_itens`
- `df_produtos`
- `df_avaliacoes`
- `df_tickets`

---

# 🏗️ 2. data_build.py (ETL / Modelação)

## 🎯 Objetivo
Criar tabelas analíticas (fact tables).

## 🧱 Fact Tables

### 📦 fact_vendas
Contém:
- pedidos
- produtos
- clientes
- métricas financeiras

### ⚠️ fact_tickets
- tickets de suporte
- categorias de problema
- tempos de resolução

### ⭐ fact_avaliacoes
- avaliações de clientes
- notas e comentários

---

## 📊 Métricas Criadas

- valor_bruto
- valor_liquido
- desconto
- (opcional) lucro

---

## 📤 Outputs

- `fact_vendas.csv`
- `fact_tickets.csv`
- `fact_avaliacoes.csv`

---

# 📊 3. analysis.py (Camada Analítica)

## 🎯 Objetivo
Gerar insights de negócio a partir das fact tables.

---

# 📈 INSIGHTS DE NEGÓCIO (RESULTADOS REAIS)

## 📦 Distribuição de Pedidos

- **66% dos pedidos são entregues**
- **17% são cancelados** ⚠️ (valor elevado)
- ~16% estão em trânsito ou devolvidos

👉 Indica espaço para melhoria operacional.

---

## 🏆 Produtos

- Produtos como **tênis, notebooks e roupas íntimas** dominam receita e volume
- Forte concentração → padrão **Pareto (80/20)**

👉 Poucos produtos geram grande parte da receita.

---

## 📅 Sazonalidade

- Pico extremo em **Novembro (Black Friday)**  
- Receita ~4x maior que meses normais

👉 Negócio altamente dependente de campanhas.

---

## 💰 Ticket Médio

### Por canal:
- Todos os canais têm ticket parecido (~4800€)
- Diferença não é significativa

👉 Receita depende mais de volume do que valor por cliente.

---

## 👥 Segmentação (B2B vs B2C)

- B2B tem ticket ligeiramente maior
- Teste estatístico:
  - **p-value = 0.55**
  - ❌ Sem diferença significativa

👉 Segmentos comportam-se de forma semelhante.

---

## ❌ Cancelamento por Canal

- **Paid Search: 30% (crítico 🚨)**
- Outros canais: ~12%

👉 Forte problema de qualidade de leads pagos.

---

## ⭐ Avaliações

- Produtos mais avaliados têm média alta (~4.1–4.4)

👉 Satisfação geral positiva.

---

## ⚠️ Tickets de Suporte

- Produtos com mais tickets:
  - Material escolar
  - Tênis
  - Eletrónicos

👉 Possível relação com:
- qualidade
- logística
- expectativas do cliente

---

# 🧠 PRINCIPAIS CONCLUSÕES

✔ Receita concentrada em poucos produtos  
✔ Forte dependência de sazonalidade (Novembro)  
✔ Canal pago gera muitos cancelamentos  
✔ B2B ≈ B2C (sem diferença estatística)  
✔ Boa satisfação geral, mas com problemas em alguns produtos  

---

# 🧱 Arquitetura do Pipeline
RAW DATA
↓
data_treatment.py
↓
CLEAN DATA
↓
data_build.py
↓
FACT TABLES (CSV)
↓
analysis.py
↓
INSIGHTS

---

# 📊 Business Intelligence

O dashboard foi desenvolvido com base nos CSVs gerados:

- `fact_vendas.csv`
- `fact_tickets.csv`
- `fact_avaliacoes.csv`

👉 Integração direta com Power BI

---

# 📊 Tecnologias

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib

---

## 🔧 Melhorias Futuras

- Criar dashboard interativo (Power BI)
- Implementar modelo star schema
- Adicionar validação de dados

---

# 👨‍💻 Autora

Valentina Perpetuo dos Santos
