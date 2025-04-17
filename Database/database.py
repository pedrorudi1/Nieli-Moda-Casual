import sqlite3

def create_connection():
    conn = sqlite3.connect('Database/database.db')
    return conn 

def criar_banco_dados():
    
    conn = create_connection()
    cursor = conn.cursor()
    
    # Tabela de clientes com código sequencial
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes
                      (codigo_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       telefone TEXT,
                       data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Tabela de produtos
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tipo TEXT NOT NULL,
                       cor TEXT,
                       tamanho TEXT,
                       preco_custo REAL,
                       preco_venda REAL,
                       quantidade INTEGER)''')
    
    # Tabela de vendas
    cursor.execute('''CREATE TABLE IF NOT EXISTS vendas
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       cliente_id TEXT,
                       valor_total REAL,
                       data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (cliente_id) REFERENCES clientes (codigo_cliente))''')
    
    # Tabela de itens de venda
    cursor.execute('''CREATE TABLE IF NOT EXISTS itens_venda
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       venda_id INTEGER,
                       produto_id INTEGER,
                       quantidade INTEGER,
                       valor_unitario REAL,
                       FOREIGN KEY (venda_id) REFERENCES vendas (id),
                       FOREIGN KEY (produto_id) REFERENCES produtos (id))''')
    
    # Tabela de pagamentos
    cursor.execute('''CREATE TABLE IF NOT EXISTS pagamentos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       cliente_id TEXT,
                       venda_id INTEGER,
                       valor_pago REAL,
                       data_pagamento DATETIME,
                       tipo_pagamento TEXT DEFAULT 'DINHEIRO',
                       FOREIGN KEY (cliente_id) REFERENCES clientes (codigo_cliente),
                       FOREIGN KEY (venda_id) REFERENCES vendas (id))''')
    
    #Tabela de créditos
    cursor.execute('''CREATE TABLE IF NOT EXISTS creditos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       cliente_id INTEGER,
                       valor REAL,
                       usado INTEGER DEFAULT 0,
                       data_credito TEXT,
                       observacao TEXT,
                       FOREIGN KEY(cliente_id) REFERENCES clientes(codigo_cliente));''')
    
   

        
    conn.commit()
    conn.close()