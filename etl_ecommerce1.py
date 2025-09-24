import requests
import mysql.connector
import random
from datetime import datetime, timedelta

# =========================
# Configuração do MySQL
# =========================
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# =========================
# 1. Criar tabela de origens (UTM)
# =========================
origens = ['Google', 'Facebook', 'Instagram', 'Recomendação', 'Email Marketing', 'Orgânico (Site)']
cursor.execute("""
CREATE TABLE IF NOT EXISTS origens (
    origem_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100)
)
""")
cursor.execute("SELECT COUNT(*) FROM origens")
if cursor.fetchone()[0] == 0:
    for origem in origens:
        cursor.execute("INSERT INTO origens (nome) VALUES (%s)", (origem,))
conn.commit()

# Pegar ids das origens
cursor.execute("SELECT origem_id, nome FROM origens")
origem_dict = {nome: origem_id for origem_id, nome in cursor.fetchall()}

# =========================
# 2. Criar tabela de produtos e buscar Fake Store API
# =========================
print("Buscando produtos da Fake Store API...")
response = requests.get("https://fakestoreapi.com/products")
produtos = response.json()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    produto_id INT PRIMARY KEY,
    titulo VARCHAR(255),
    preco DECIMAL(10,2),
    descricao TEXT,
    categoria VARCHAR(100),
    imagem VARCHAR(255)
)
""")

for produto in produtos:
    cursor.execute("""
        INSERT INTO produtos (produto_id, titulo, preco, descricao, categoria, imagem)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE titulo=VALUES(titulo), preco=VALUES(preco)
    """, (produto['id'], produto['title'], produto['price'], produto['description'], produto['category'], produto['image']))
conn.commit()
print(f"{len(produtos)} produtos inseridos!")

# =========================
# 3. Criar tabela de clientes e inserir clientes fictícios
# =========================
print("Gerando clientes fictícios...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20),
    data_cadastro DATE,
    origem_id INT,
    etapa_funil VARCHAR(50),
    FOREIGN KEY (origem_id) REFERENCES origens(origem_id)
)
""")

nomes = ["Ana", "Beatriz", "Carla", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana"]
etapas_funil = ["Novo", "Contato Feito", "Proposta", "Fechamento"]

for _ in range(500):
    nome = random.choice(nomes)
    email = f"{nome.lower()}{random.randint(1,500)}@email.com"
    telefone = f"5516999{random.randint(100000,999999)}"
    data_cadastro = datetime.today() - timedelta(days=random.randint(0, 365))
    origem_id = random.choice(list(origem_dict.values()))
    etapa_funil = random.choice(etapas_funil)

    cursor.execute("""
        INSERT INTO clientes (nome, email, telefone, data_cadastro, origem_id, etapa_funil)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, email, telefone, data_cadastro.date(), origem_id, etapa_funil))
conn.commit()
print("500 clientes inseridos!")

# =========================
# 4. Criar tabela de pedidos e itens de pedido
# =========================
print("Gerando pedidos e itens de pedido...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    valor_total DECIMAL(10,2),
    data_pedido DATE,
    status VARCHAR(50),
    forma_pagamento VARCHAR(50),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS itens_pedido (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    produto_id INT,
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id),
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
)
""")

status_list = ["Novo", "Processando", "Enviado", "Entregue", "Cancelado"]
pagamentos = ["Cartão", "Pix", "Boleto", "Paypal"]

cursor.execute("SELECT cliente_id FROM clientes")
clientes_ids = [row[0] for row in cursor.fetchall()]
produto_ids = [produto['id'] for produto in produtos]

for cliente_id in clientes_ids:
    for _ in range(random.randint(1,3)):  # cada cliente faz 1-3 pedidos
        valor_total = 0
        data_pedido = datetime.today() - timedelta(days=random.randint(0, 365))
        status = random.choice(status_list)
        forma_pagamento = random.choice(pagamentos)

        cursor.execute("""
            INSERT INTO pedidos (cliente_id, valor_total, data_pedido, status, forma_pagamento)
            VALUES (%s, %s, %s, %s, %s)
        """, (cliente_id, 0, data_pedido.date(), status, forma_pagamento))
        pedido_id = cursor.lastrowid

        # inserir itens de pedido
        for _ in range(random.randint(1,5)):
            produto_id = random.choice(produto_ids)
            quantidade = random.randint(1,3)
            preco_unitario = next(p['price'] for p in produtos if p['id'] == produto_id)
            valor_total += quantidade * preco_unitario

            cursor.execute("""
                INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)
            """, (pedido_id, produto_id, quantidade, preco_unitario))

        # atualizar valor_total do pedido
        cursor.execute("UPDATE pedidos SET valor_total=%s WHERE pedido_id=%s", (valor_total, pedido_id))

conn.commit()
print("Pedidos e itens de pedido inseridos!")

# =========================
# 5. Criar tabela de avaliações
# =========================
print("Gerando avaliações de produtos...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS avaliacoes (
    avaliacao_id INT PRIMARY KEY AUTO_INCREMENT,
    produto_id INT,
    cliente_id INT,
    nota INT,
    comentario VARCHAR(255),
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
)
""")

for cliente_id in clientes_ids:
    for _ in range(random.randint(0,2)):  # 0-2 avaliações por cliente
        produto_id = random.choice(produto_ids)
        nota = random.randint(1,5)
        comentario = f"Avaliação nota {nota}"
        cursor.execute("""
            INSERT INTO avaliacoes (produto_id, cliente_id, nota, comentario)
            VALUES (%s, %s, %s, %s)
        """, (produto_id, cliente_id, nota, comentario))

conn.commit()
print("Avaliações inseridas!")

# =========================
# Fechar conexão
# =========================
cursor.close()
conn.close()
print("ETL finalizado com sucesso!")
