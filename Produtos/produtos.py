from Database import database
from Gui import gui
from tkinter import ttk

def abrir_cadastro_produtos():
    from Produtos import preencher_campos_produto, cadastrar_produto, atualizar_produto, excluir_produto
    global tree_produtos, entry_descricao, entry_detalhe, entry_tamanho, entry_preco_custo
    global entry_preco_venda, entry_quantidade, data_cadastro
    from datetime import datetime
    
    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")

    gui.canvas.create_text(700, 50, text="Cadastro de Produtos", font=("Arial", 24))

    gui.canvas.create_text(550, 120, text="Descrição:", anchor="e", font=("Arial", 12))
    entry_descricao = ttk.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 120, window=entry_descricao, anchor="w")

    gui.canvas.create_text(550, 160, text="Detalhe:", anchor="e", font=("Arial", 12))
    entry_detalhe = ttk.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 160, window=entry_detalhe, anchor="w")

    gui.canvas.create_text(550, 200, text="Tamanho:", anchor="e", font=("Arial", 12))
    entry_tamanho = ttk.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 200, window=entry_tamanho, anchor="w")

    gui.canvas.create_text(550, 240, text="Preço de Custo:", anchor="e", font=("Arial", 12))
    entry_preco_custo = ttk.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 240, window=entry_preco_custo, anchor="w")

    gui.canvas.create_text(550, 280, text="Preço de Venda: ", anchor="e", font=("Arial, 12"))
    entry_preco_venda = ttk.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560,280, window=entry_preco_venda, anchor="w")

    gui.canvas.create_text(550, 320, text="Quantidade:", anchor="e", font=("Arial", 12))
    entry_quantidade = ttk.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 320, window=entry_quantidade, anchor="w")

    btn_cadastrar = gui.Button(gui.App, text="Cadastrar", command=lambda: cadastrar_produto (entry_descricao,
                                                                                            entry_detalhe,
                                                                                            entry_tamanho,
                                                                                            entry_preco_custo,
                                                                                            entry_preco_venda,
                                                                                            entry_quantidade,
                                                                                            tree_produtos,
                                                                                            ),
                               font=("Arial", 12), bg="#4CAF50", fg="white")
    gui.canvas.create_window(650, 360, window=btn_cadastrar)

    btn_atualizar = gui.Button(gui.App, text="Atualizar",
                               command=lambda: atualizar_produto(),
                               font=("Arial", 12),
                               bg="#2196F3",
                               fg="white")
    gui.canvas.create_window(755, 360, window=btn_atualizar)

    btn_excluir = gui.Button(gui.App,
                             text="Excluir",
                             command=lambda: excluir_produto(tree_produtos), 
                             font=("Arial", 12),
                             bg="#f44336",
                             fg="white")
    gui.canvas.create_window(850, 360, window=btn_excluir)

    tree_produtos = gui.ttk.Treeview(gui.App, columns=("ID", "Descrição", "Detalhe", "Tamanho", "Preço Custo", "Preço Venda", "Quantidade"), show="headings")
    tree_produtos.column("ID", width=50, minwidth=50, stretch="no")
    tree_produtos.heading("ID", text="ID")
    tree_produtos.column("Descrição", width=200, minwidth=100, stretch="yes")
    tree_produtos.heading("Descrição", text="Descrição")
    tree_produtos.column("Detalhe", width=100, minwidth=100, stretch="yes")
    tree_produtos.heading("Detalhe", text="Detalhe")
    tree_produtos.column("Tamanho", width=100, minwidth=100, stretch="yes")
    tree_produtos.heading("Tamanho", text="Tamanho")
    tree_produtos.column("Preço Custo", width=100, minwidth=100, stretch="yes")
    tree_produtos.heading("Preço Custo", text="Preço Custo")
    tree_produtos.column("Preço Venda", width=100, minwidth=100, stretch="yes")
    tree_produtos.heading("Preço Venda", text="Preço Venda")
    tree_produtos.column("Quantidade", width=100, minwidth=100, stretch="yes")
    tree_produtos.heading("Quantidade", text="Quantidade")
    gui.canvas.create_window(700, 540, window=tree_produtos, width=800, height=300)

    tree_produtos.bind("<Double-1>", preencher_campos_produto)
    tree_produtos.bind("<Delete>", del_para_excluir)
    entry_descricao.bind("<KeyRelease>", filtrar_produtos)

    atualizar_tabela_produtos(tree_produtos)

def cadastrar_produto(entry_descricao,
                      entry_detalhe,
                      entry_tamanho,
                      entry_preco_custo,
                      entry_preco_venda,
                      entry_quantidade,
                      tree_produtos):
    
    from datetime import datetime
    
    descricao = entry_descricao.get().strip()
    detalhe = entry_detalhe.get().strip()
    tamanho = entry_tamanho.get().strip()
    preco_custo = float(entry_preco_custo.get().strip().replace(",","."))
    preco_venda = float(entry_preco_venda.get().strip().replace(",","."))
    quantidade = int(entry_quantidade.get())
    data_cadastro = datetime.now()

    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (descricao, detalhe, tamanho, preco_custo, preco_venda, quantidade, data_cadastro) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (descricao, detalhe, tamanho, preco_custo, preco_venda, quantidade, data_cadastro))
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()

    entry_descricao.delete(0, gui.END)
    entry_detalhe.delete(0, gui.END)
    entry_tamanho.delete(0,gui.END)
    entry_preco_custo.delete(0,gui.END)
    entry_preco_venda.delete(0, gui.END)
    entry_quantidade.delete(0, gui.END)

    if 'tree_produtos' in globals() and tree_produtos:
        tree_produtos.insert("", "end", values=(novo_id, descricao, detalhe, tamanho, preco_custo, preco_venda, quantidade, data_cadastro))
    else:
        print("Erro: A tabela de produtos não foi encontrada.")

    gui.messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
    atualizar_tabela_produtos(tree_produtos)

def atualizar_produto():
    from datetime import datetime

    selected_item = tree_produtos.selection()
    if not selected_item:
        gui.messagebox.showwarning("Aviso", "Por favor, selecione um produto para atualizar.")
        return
    
    selected_item = selected_item[0]
    id = tree_produtos.item(selected_item)['values'][0]
    
    novo_descricao = entry_descricao.get().strip()
    novo_detalhe = entry_detalhe.get().strip()
    novo_tamanho = entry_tamanho.get().strip()
    novo_preco_custo = entry_preco_custo.get().strip().replace(",", ".").replace("R$", "")
    novo_preco_venda = entry_preco_venda.get().strip().replace(",", ".").replace("R$", "")
    novo_quantidade = entry_quantidade.get().strip()
    data_atualizacao = datetime.now()
        
               
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET descricao=?, detalhe=?, tamanho=?, preco_custo=?, preco_venda=?, quantidade=?, data_cadastro=? WHERE id=?",
        (novo_descricao, novo_detalhe, novo_tamanho, novo_preco_custo, novo_preco_venda, novo_quantidade, data_atualizacao, id))
    
    conn.commit()
    gui.messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
    conn.close()
    
    entry_descricao.delete(0, gui.END)
    entry_detalhe.delete(0, gui.END)
    entry_tamanho.delete(0,gui.END)
    entry_preco_custo.delete(0,gui.END)
    entry_preco_venda.delete(0, gui.END)
    entry_quantidade.delete(0, gui.END)
    atualizar_tabela_produtos(tree_produtos)

def excluir_produto (tree_produtos):
    selected_item = tree_produtos.selection()
    if not selected_item:
        gui.messagebox.showwarning("Aviso", "Por favor, selecione um produto para excluir.")
        return

    resposta = gui.messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir este produto?")
    if resposta:
        id = tree_produtos.item(selected_item)['values'][0]

        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PRODUTOS WHERE id = ?", (id,))
        conn.commit()
        tree_produtos.delete(selected_item)
        gui.messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
        atualizar_tabela_produtos(tree_produtos)
        conn.close()
        
def preencher_campos_produto(Event):
    
    item_selecionado = tree_produtos.selection()
    if item_selecionado:
        valores = tree_produtos.item(item_selecionado, 'values')
        
        entry_descricao.delete(0, 'end')
        entry_detalhe.delete(0, 'end')
        entry_tamanho.delete(0, 'end')
        entry_preco_custo.delete(0, 'end')
        entry_preco_venda.delete(0, 'end')
        entry_quantidade.delete(0, 'end')
        entry_descricao.insert(0, valores[1])
        entry_detalhe.insert(0, valores[2])
        entry_tamanho.insert(0, valores[3])
        preco_custo = valores[4].replace("R$", "").replace(",", ".").strip()
        preco_venda = valores[5].replace("R$", "").replace(",", ".").strip()
        entry_preco_custo.insert(0, float(preco_custo))
        entry_preco_venda.insert(0, float(preco_venda))
        entry_quantidade.insert(0, valores[6])
    
def atualizar_tabela_produtos(tree_produtos):
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)
        
    for row in rows:
        valores = list(row)
        valores[4] = f"R$ {valores[4]:.2f}".replace(".", ",")
        valores[5] = f"R$ {valores[5]:.2f}".replace(".", ",")
        tree_produtos.insert("", "end", values=valores)
    
    conn.close()

def del_para_excluir(Event):
    excluir_produto(tree_produtos)

def filtrar_produtos(event=None):
    
    search_term = entry_descricao.get().lower()
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)

    if not search_term:
        atualizar_tabela_produtos(tree_produtos)
        return

    conn = database.create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos WHERE descricao LIKE ?", ('%' + search_term + '%',))
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        valores = list(row)
        valores[4] = f"R$ {valores[4]:.2f}".replace(".", ",")
        valores[5] = f"R$ {valores[5]:.2f}".replace(".", ",")
        tree_produtos.insert("", "end", values=valores)