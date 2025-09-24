# ETL E-commerce

Este projeto simula um fluxo de **ETL (Extract, Transform, Load)** para dados de um e-commerce fictício, utilizando Python, MySQL e Power BI.

##  Objetivo
Criar um pipeline de dados que:
- Consome produtos de uma API pública (Fake Store API).
- Gera clientes fictícios.
- Cria pedidos e itens de pedidos.
- Armazena tudo em um banco de dados MySQL hospedado na **AWS RDS**.
- Permite análises em **Power BI**, como funil de vendas, origens de marketing, estudo de clientes, motivos de cancelamento etc.

##  Tecnologias utilizadas
- **Python** (para o ETL)
- **MySQL** (armazenamento dos dados)
- **AWS RDS** (banco de dados na nuvem)
- **Power BI** (visualização dos dados)
- **Git & GitHub** (versionamento e publicação do projeto)

##  Estrutura do projeto
etl_ecommerce/
│-- etl_ecommerce.py # Script principal do ETL
│-- requirements.txt # Dependências do projeto
│-- README.md # Documentação


##  Como executar
1. Clone o repositório:
   ```bash
   git clone https://github.com/leonardomigliacc/etl-ecommerce.git
   cd etl-ecommerce
Instale as dependências:
pip install -r requirements.txt
Configure o banco de dados MySQL no AWS RDS ou localmente.


Rode o ETL:
python etl_ecommerce.py
Resultados esperados
Produtos carregados da API.

Clientes fictícios inseridos.

Pedidos e itens de pedidos registrados no banco.



**Dashboard em Power BI com:**

Vendas totais

Funil

Pedidos e itens

Lucro

Origens de clientes (marketing)

Cancelamentos (com motivos)

Formas de pagamento

