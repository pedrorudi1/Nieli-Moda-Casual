from Database import database
from Gui import gui

def abrir_cadastro_produtos():
    from Produtos import preencher_campos_produto, cadastrar_produto, atualizar_produto, excluir_produto
    global tree_produtos, entry_tipo, entry_cor, entry_tamanho, entry_preco_custo, entry_preco_venda, entry_quantidade
    
    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")

    gui.canvas.create_text(700, 50, text="Cadastro de Produtos", font=("Arial", 24))

    gui.canvas.create_text(550, 120, text="Tipo:", anchor="e", font=("Arial", 12))
    entry_tipo = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 120, window=entry_tipo, anchor="w")

    gui.canvas.create_text(550, 160, text="Cor:", anchor="e", font=("Arial", 12))
    entry_cor = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 160, window=entry_cor, anchor="w")

    gui.canvas.create_text(550, 200, text="Tamanho:", anchor="e", font=("Arial", 12))
    entry_tamanho = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 200, window=entry_tamanho, anchor="w")

    gui.canvas.create_text(550, 240, text="Preço de Custo:", anchor="e", font=("Arial", 12))
    entry_preco_custo = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 240, window=entry_preco_custo, anchor="w")

    gui.canvas.create_text(550, 280, text="Preço de Venda: ", anchor="e", font=("Arial, 12"))
    entry_preco_venda = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560,280, window=entry_preco_venda, anchor="w")

    gui.canvas.create_text(550, 320, text="Quantidade:", anchor="e", font=("Arial", 12))
    entry_quantidade = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 320, window=entry_quantidade, anchor="w")

    btn_cadastrar = gui.Button(gui.App, text="Cadastrar", command=lambda: cadastrar_produto (entry_tipo,
                                                                                            entry_cor,
                                                                                            entry_tamanho,
                                                                                            entry_preco_custo,
                                                                                            entry_preco_venda,
                                                                                            entry_quantidade,
                                                                                            tree_produtos),
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

    tree_produtos = gui.ttk.Treeview(gui.App, columns=("ID", "Tipo", "Cor", "Tamanho", "Preço Custo", "Preço Venda", "Quantidade"), show="headings")
    tree_produtos.column("ID", width=50, minwidth=50, stretch="no")
    tree_produtos.heading("ID", text="ID")
    tree_produtos.column("Tipo", width=200, minwidth=100, stretch="yes")
    tree_produtos.heading("Tipo", text="Tipo")
    tree_produtos.column("Cor", width=100, minwidth=100, stretch="yes")
    tree_produtos.heading("Cor", text="Cor")
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

    atualizar_tabela_produtos(tree_produtos)

def cadastrar_produto(entry_tipo,
                      entry_cor,
                      entry_tamanho,
                      entry_preco_custo,
                      entry_preco_venda,
                      entry_quantidade,
                      tree_produtos):
    
    tipo = entry_tipo.get().strip()
    cor = entry_cor.get().strip()
    tamanho = entry_tamanho.get().strip()
    preco_custo = float(entry_preco_custo.get())
    preco_venda = float(entry_preco_venda.get())
    quantidade = int(entry_quantidade.get())

    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (tipo, cor, tamanho, preco_custo, preco_venda, quantidade) VALUES (?, ?, ?, ?, ?, ?)",
                   (tipo, cor, tamanho, preco_custo, preco_venda, quantidade))
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()

    entry_tipo.delete(0, gui.END)
    entry_cor.delete(0, gui.END)
    entry_tamanho.delete(0,gui.END)
    entry_preco_custo.delete(0,gui.END)
    entry_preco_venda.delete(0, gui.END)
    entry_quantidade.delete(0, gui.END)

    if 'tree_produtos' in globals() and tree_produtos:
        tree_produtos.insert("", "end", values=(novo_id, tipo, cor, tamanho, preco_custo, preco_venda, quantidade))
    else:
        print("Erro: A tabela de produtos não foi encontrada.")

    gui.messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

def atualizar_produto():
    
    selected_item = tree_produtos.selection()
    if not selected_item:
        gui.messagebox.showwarning("Aviso", "Por favor, selecione um produto para atualizar.")
        return
    
    selected_item = selected_item[0]
    id = tree_produtos.item(selected_item)['values'][0]
    
    novo_tipo = entry_tipo.get().strip()
    novo_cor = entry_cor.get().strip()
    novo_tamanho = entry_tamanho.get().strip()
    novo_preco_custo = entry_preco_custo.get().strip()
    novo_preco_venda = entry_preco_venda.get().strip()
    novo_quantidade = entry_quantidade.get().strip()
        
               
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET tipo=?, cor=?, tamanho=?, preco_custo=?, preco_venda=?, quantidade=? WHERE id=?",
        (novo_tipo, novo_cor, novo_tamanho, novo_preco_custo, novo_preco_venda, novo_quantidade, id))
    
    conn.commit()
    gui.messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
    conn.close()
    
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
        
        entry_tipo.delete(0, 'end')
        entry_cor.delete(0, 'end')
        entry_tamanho.delete(0, 'end')
        entry_preco_custo.delete(0, 'end')
        entry_preco_venda.delete(0, 'end')
        entry_quantidade.delete(0, 'end')
        entry_tipo.insert(0, valores[1])
        entry_cor.insert(0, valores[2])
        entry_tamanho.insert(0, valores[3])
        entry_preco_custo.insert(0, valores[4])
        entry_preco_venda.insert(0, valores[5])
        entry_quantidade.insert(0, valores[6])
    
def atualizar_tabela_produtos(tree_produtos):
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)
        
    for row in rows:
        tree_produtos.insert("", "end", values=row)
    
    conn.close()

def del_para_excluir(Event):
    excluir_produto(tree_produtos)