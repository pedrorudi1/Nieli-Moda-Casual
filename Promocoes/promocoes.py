from Gui import gui
from Database import database
from tkinter import messagebox, Frame, Label, Entry, Button, LEFT, BOTH
from tkinter import ttk


def abrir_promocoes():
    """Abre a tela de promoções"""
    global tree_promocoes
    
    # Limpar canvas e configurar background
    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")
    gui.canvas.create_text(700, 30, text="Promoções", font=("Arial", 24))

    # Frame principal
    frame_promocoes = gui.Frame(gui.App, bg="#F8EBFF")
    gui.canvas.create_window(700, 350, window=frame_promocoes, width=800)

    # Criar notebook para abas
    notebook = ttk.Notebook(frame_promocoes)
    notebook.pack(fill=BOTH, expand=True)

    # Aba de Produtos em Promoção
    tab_produtos = gui.Frame(notebook)
    notebook.add(tab_produtos, text="Produtos em Promoção")

    # Aba de Gerenciar Promoções
    tab_gerenciar = gui.Frame(notebook)
    notebook.add(tab_gerenciar, text="Gerenciar Promoções")

    # Tabela de produtos em promoção (primeira aba)
    tree_promocoes = ttk.Treeview(tab_produtos, 
                                 columns=("ID", "Tipo", "Cor", "Tamanho", "Preço Normal", "Preço Promocional"),
                                 show="headings", 
                                 height=15)

    tree_promocoes.heading("ID", text="ID")
    tree_promocoes.heading("Tipo", text="Tipo")
    tree_promocoes.heading("Cor", text="Cor")
    tree_promocoes.heading("Tamanho", text="Tamanho")
    tree_promocoes.heading("Preço Normal", text="Preço Normal")
    tree_promocoes.heading("Preço Promocional", text="Preço Promocional")

    tree_promocoes.column("ID", width=50, anchor="center")
    tree_promocoes.column("Tipo", width=150)
    tree_promocoes.column("Cor", width=100)
    tree_promocoes.column("Tamanho", width=100)
    tree_promocoes.column("Preço Normal", width=100, anchor="e")
    tree_promocoes.column("Preço Promocional", width=100, anchor="e")

    tree_promocoes.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Frame para gerenciamento de promoções (segunda aba)
    frame_gerenciar = gui.Frame(tab_gerenciar)
    frame_gerenciar.pack(pady=10, fill=BOTH, expand=True)

    # Combobox para selecionar produto
    gui.Label(frame_gerenciar, text="Selecionar Produto:", font=("Arial", 12)).pack(pady=5)
    combo_produtos = ttk.Combobox(frame_gerenciar, width=40)
    combo_produtos['values'] = consultar_produtos()
    combo_produtos.pack(pady=5)

    # Campo para preço promocional
    gui.Label(frame_gerenciar, text="Preço Promocional:", font=("Arial", 12)).pack(pady=5)
    entry_preco_promo = gui.Entry(frame_gerenciar, width=15)
    entry_preco_promo.pack(pady=5)

    # Botões
    frame_botoes = gui.Frame(frame_gerenciar)
    frame_botoes.pack(pady=10)

    btn_adicionar = gui.Button(frame_botoes, 
                          text="Adicionar à Promoção",
                          command=lambda: adicionar_promocao(combo_produtos.get(), entry_preco_promo.get()),
                          font=("Arial", 12), 
                          bg="#4CAF50", 
                          fg="white")
    btn_adicionar.pack(side=LEFT, padx=5)

    btn_remover = gui.Button(frame_botoes, 
                        text="Remover da Promoção",
                        command=lambda: remover_promocao(combo_produtos.get()),
                        font=("Arial", 12), 
                        bg="#f44336", 
                        fg="white")
    btn_remover.pack(side=LEFT, padx=5)

    # Carregar produtos em promoção
    carregar_produtos_promocao()

def adicionar_promocao(produto_info, preco_promo):
    """Adiciona um produto à lista de promoções"""
    if not produto_info or not preco_promo:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        produto_id = produto_info.split(' - ')[0]
        preco_promocional = float(preco_promo)

        if preco_promocional <= 0:
            raise ValueError("O preço promocional deve ser maior que zero")

        conn = database.create_connection()
        cursor = conn.cursor()

        # Verificar preço atual
        cursor.execute("SELECT preco_venda FROM produtos WHERE id = ?", (produto_id,))
        preco_atual = cursor.fetchone()[0]

        if preco_promocional >= preco_atual:
            messagebox.showerror("Erro", "O preço promocional deve ser menor que o preço normal.")
            return

        # Atualizar produto como em promoção
        cursor.execute("""
            UPDATE produtos 
            SET promocao = 1, preco_promocional = ? 
            WHERE id = ?
        """, (preco_promocional, produto_id))

        conn.commit()
        messagebox.showinfo("Sucesso", "Produto adicionado à promoção!")
        
        # Atualizar a tabela
        carregar_produtos_promocao()

    except ValueError as e:
        messagebox.showerror("Erro", f"Valor inválido: {str(e)}")
    except database.sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao adicionar promoção: {str(e)}")
    finally:
        conn.close()

def remover_promocao(produto_info):
    """Remove um produto da lista de promoções"""
    if not produto_info:
        messagebox.showerror("Erro", "Por favor, selecione um produto.")
        return

    try:
        produto_id = produto_info.split(' - ')[0]
        
        conn = database.create_connection()
        cursor = conn.cursor()

        # Remover produto da promoção
        cursor.execute("""
            UPDATE produtos 
            SET promocao = 0, preco_promocional = NULL 
            WHERE id = ?
        """, (produto_id,))

        conn.commit()
        messagebox.showinfo("Sucesso", "Produto removido da promoção!")
        
        # Atualizar a tabela
        carregar_produtos_promocao()

    except database.sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao remover promoção: {str(e)}")
    finally:
        conn.close()

def carregar_produtos_promocao():
    """Carrega os produtos em promoção na tabela"""
    for item in tree_promocoes.get_children():
        tree_promocoes.delete(item)

    conn = database.create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, tipo, cor, tamanho, preco_venda, preco_promocional
            FROM produtos
            WHERE promocao = 1
            ORDER BY tipo, cor, tamanho
        """)

        for row in cursor.fetchall():
            produto_id, tipo, cor, tamanho, preco_normal, preco_promo = row
            tree_promocoes.insert("", "end", values=(
                produto_id,
                tipo,
                cor,
                tamanho,
                f"R$ {preco_normal:.2f}",
                f"R$ {preco_promo:.2f}"
            ))

    except database.sqlite3.Error as e:
        print(f"Erro ao carregar produtos em promoção: {e}")
    finally:
        conn.close()

def consultar_produtos():
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tipo, cor, tamanho FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return [f"{id} - {tipo} {cor} {tamanho}" for id, tipo, cor, tamanho in produtos]