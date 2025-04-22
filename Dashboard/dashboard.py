from Database import database
from Gui import gui
from datetime import datetime, timedelta
from tkinter import ttk


def abrir_dashboard():
    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")
    gui.canvas.create_text(700, 30, text="Dashboard", font=("Arial", 24))

    frame_dashboard = gui.Frame(gui.App, bg="#F8EBFF")
    gui.canvas.create_window(700, 350, window=frame_dashboard, width=800)

    # Estilo para os frames de indicadores
    style_frame = {"relief": "ridge", "borderwidth": 2, "padx": 15, "pady": 15}
    style_titulo = {"font": ("Arial", 14, "bold"), "pady": 10}
    style_valor = {"font": ("Arial", 12), "pady": 5}

    # Frame Clientes
    frame_clientes = gui.Frame(frame_dashboard, **style_frame)
    frame_clientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    gui.Label(frame_clientes, text="Clientes", **style_titulo).pack()
    
    total_clientes = obter_dados_clientes()
    gui.Label(frame_clientes, text=f"Total de Clientes: {total_clientes}", **style_valor).pack()

    # Frame Vendas
    frame_vendas = gui.Frame(frame_dashboard, **style_frame)
    frame_vendas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    gui.Label(frame_vendas, text="Vendas", **style_titulo).pack()
    
    vendas_mes, vendas_trimestre = obter_dados_vendas()
    gui.Label(frame_vendas, text=f"Vendas (Mês Atual): R$ {vendas_mes:.2f}", **style_valor).pack()
    gui.Label(frame_vendas, text=f"Vendas (3 Meses): R$ {vendas_trimestre:.2f}", **style_valor).pack()

    # Frame Recebimentos
    frame_recebimentos = gui.Frame(frame_dashboard, **style_frame)
    frame_recebimentos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    gui.Label(frame_recebimentos, text="Recebimentos", **style_titulo).pack()
    
    recebido_mes, recebido_trimestre = obter_dados_recebimentos()
    gui.Label(frame_recebimentos, text=f"Recebido (Mês Atual): R$ {recebido_mes:.2f}", **style_valor).pack()
    gui.Label(frame_recebimentos, text=f"Recebido (3 Meses): R$ {recebido_trimestre:.2f}", **style_valor).pack()

    # Frame Lucro
    frame_lucro = gui.Frame(frame_dashboard, **style_frame)
    frame_lucro.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    
    gui.Label(frame_lucro, text="Lucro Líquido", **style_titulo).pack()
    
    lucro_mes, lucro_trimestre = obter_dados_lucro()
    gui.Label(frame_lucro, text=f"Lucro (Mês Atual): R$ {lucro_mes:.2f}", **style_valor).pack()
    gui.Label(frame_lucro, text=f"Lucro (3 Meses): R$ {lucro_trimestre:.2f}", **style_valor).pack()

    # Configurar grid
    frame_dashboard.grid_columnconfigure(0, weight=1)
    frame_dashboard.grid_columnconfigure(1, weight=1)

def obter_dados_clientes():

    conn = database.create_connection()
    cursor = conn.cursor()
    
    # Total de clientes
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    
   
    conn.close()
    return total_clientes

def obter_dados_vendas():
    """Retorna o total de vendas do mês atual e dos últimos 3 meses"""
    conn = database.create_connection()
    cursor = conn.cursor()
    
    hoje = datetime.now()
    primeiro_dia_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    primeiro_dia_tres_meses = (hoje - timedelta(days=90)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Vendas do mês atual
    cursor.execute("""
        SELECT COALESCE(SUM(valor_total), 0) FROM vendas 
        WHERE data_venda >= ?
    """, (primeiro_dia_mes,))
    vendas_mes = cursor.fetchone()[0]
    
    # Vendas dos últimos 3 meses
    cursor.execute("""
        SELECT COALESCE(SUM(valor_total), 0) FROM vendas 
        WHERE data_venda >= ?
    """, (primeiro_dia_tres_meses,))
    vendas_trimestre = cursor.fetchone()[0]
    
    conn.close()
    return vendas_mes, vendas_trimestre

def obter_dados_recebimentos():
    """Retorna o total recebido no mês atual e nos últimos 3 meses"""
    conn = database.create_connection()
    cursor = conn.cursor()
    
    hoje = datetime.now()
    primeiro_dia_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    primeiro_dia_tres_meses = (hoje - timedelta(days=90)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Recebimentos do mês atual
    cursor.execute("""
        SELECT COALESCE(SUM(valor_pago), 0) FROM pagamentos 
        WHERE data_pagamento >= ?
    """, (primeiro_dia_mes,))
    recebido_mes = cursor.fetchone()[0]
    
    # Recebimentos dos últimos 3 meses
    cursor.execute("""
        SELECT COALESCE(SUM(valor_pago), 0) FROM pagamentos 
        WHERE data_pagamento >= ?
    """, (primeiro_dia_tres_meses,))
    recebido_trimestre = cursor.fetchone()[0]
    
    conn.close()
    return recebido_mes, recebido_trimestre

def obter_dados_lucro():
    conn = database.create_connection()
    cursor = conn.cursor()
        
    hoje = datetime.now()
    primeiro_dia_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    primeiro_dia_tres_meses = (hoje - timedelta(days=90)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Query corrigida para calcular o lucro líquido
    query_lucro = """
        WITH vendas_pagas AS (
            SELECT v.id, v.data_venda, 
                COALESCE(SUM(p.valor_pago), 0) as total_pago
            FROM vendas v
            LEFT JOIN pagamentos p ON v.id = p.venda_id
            GROUP BY v.id, v.data_venda
            HAVING total_pago >= v.valor_total
        )
        SELECT COALESCE(SUM(
            (iv.valor_unitario - p.preco_custo) * iv.quantidade
        ), 0) as lucro_liquido
        FROM vendas_pagas vp
        JOIN itens_venda iv ON vp.id = iv.venda_id
        JOIN produtos p ON iv.produto_id = p.id
        WHERE vp.data_venda >= ?
    """
        
        # Lucro do mês atual
    cursor.execute(query_lucro, (primeiro_dia_mes,))
    lucro_mes = cursor.fetchone()[0] or 0
        
        # Lucro dos últimos 3 meses
    cursor.execute(query_lucro, (primeiro_dia_tres_meses,))
    lucro_trimestre = cursor.fetchone()[0] or 0
        
    conn.close()
    return lucro_mes, lucro_trimestre