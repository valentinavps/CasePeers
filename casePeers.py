import pandas as pd
import os

# Optional display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)

BASES_PATH = "./Bases Case Digital"

# 1. Load data (Adjust encoding if accents are broken)
clientes = pd.read_csv(os.path.join(BASES_PATH, "clientes.csv"), encoding="utf-8")
pedidos = pd.read_csv(os.path.join(BASES_PATH, "pedidos.csv"), encoding="utf-8")
itens = pd.read_csv(os.path.join(BASES_PATH, "itens_pedido.csv"), encoding="utf-8")
produtos = pd.read_csv(os.path.join(BASES_PATH, "produtos.csv"), encoding="utf-8")
avaliacoes = pd.read_csv(os.path.join(BASES_PATH, "avaliacoes.csv"), encoding="utf-8")
tickets = pd.read_csv(os.path.join(BASES_PATH, "tickets_suporte.csv"), encoding="utf-8")

# 2. Standardize column names
clientes.columns = clientes.columns.str.strip().str.lower()

# 3. Clean and transform columns
clientes['id'] = pd.to_numeric(clientes['id'], errors='coerce')
clientes['data_cadastro'] = pd.to_datetime(clientes['data_cadastro'], errors='coerce')

# Handle strings safely in case of remaining NaNs
clientes['cidade'] = clientes['cidade'].fillna('').str.strip().str.title()
clientes['email'] = clientes['email'].fillna('').str.strip().str.lower()

# 4. Drop invalid rows and duplicates
clientes = clientes.dropna(subset=['id', 'email'])
clientes = clientes[clientes['email'] != ''] # Drop if email was just whitespace
clientes = clientes.drop_duplicates()

# 5. Final type conversions
clientes['id'] = clientes['id'].astype(int)

# print(clientes.info())
# print("-----------------------------------")
# print(clientes.head(50))

print(tickets.info())
print("-----------------------------------")
print(tickets.head(50))