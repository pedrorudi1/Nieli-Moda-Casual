from Database import database
from Gui import gui
from tkinter import ttk
import datetime

def abrir_cadastro_vendas():
    global entry_cliente_search, entry_produto_search, entry_quantidade, tree_vendas
    global list_clientes, list_produtos, tree_itens, lbl_estoque, lbl_valor_calculado, entry_valor_final
    global frame_pesquisa_cliente_window, frame_pesquisa_produto_window

    
    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")
    
    gui.canvas.create_text(700, 50, text="Registro de Vendas", font=("Arial", 24))

    # Frame para seleção de cliente e produto
    frame_selecao = ttk.Frame(gui.App)
    gui.canvas.create_window(700, 150, window=frame_selecao)

    # Pesquisa de Cliente
    ttk.Label(frame_selecao, text="Buscar Cliente:").grid(row=0, column=0, padx=5, pady=5)
    entry_cliente_search = ttk.Entry(frame_selecao, width=40)
    entry_cliente_search.grid(row=0, column=1, padx=5, pady=5)
    entry_cliente_search.bind('<Return>', pesquisar_clientes)
    
    # Frame de pesquisa para clientes
    frame_pesquisa_cliente = ttk.Frame(gui.App)
    frame_pesquisa_cliente_window = gui.canvas.create_window(700, 170, window=frame_pesquisa_cliente, state='hidden')
    
    # Lista de Clientes
    list_clientes = ttk.Treeview(frame_pesquisa_cliente, columns=("ID", "Nome"), show="headings", height=4)
    list_clientes.heading("ID", text="ID")
    list_clientes.heading("Nome", text="Nome")
    list_clientes.bind('<<TreeviewSelect>>', cliente_selecionado)

    # Pesquisa de Produto
    ttk.Label(frame_selecao, text="Buscar Produto:").grid(row=1, column=0, padx=5, pady=5)
    entry_produto_search = ttk.Entry(frame_selecao, width=40)
    entry_produto_search.grid(row=1, column=1, padx=5, pady=5)
    entry_produto_search.bind('<Return>', pesquisar_produtos)

    # Frame de pesquisa para produtos
    frame_pesquisa_produto = ttk.Frame(gui.App)
    frame_pesquisa_produto_window = gui.canvas.create_window(700, 200, window=frame_pesquisa_produto, state='hidden')
    
    # Lista de Produtos
    list_produtos = ttk.Treeview(frame_pesquisa_produto, 
                                columns=("ID", "Descrição", "Preço"), 
                                show="headings", 
                                height=4)
    list_produtos.heading("ID", text="ID")
    list_produtos.heading("Descrição", text="Descrição")
    list_produtos.heading("Preço", text="Preço")
    list_produtos.bind('<<TreeviewSelect>>', produto_selecionado)


    # Estoque disponível
    lbl_estoque = ttk.Label(frame_selecao, text="Em estoque: -")
    lbl_estoque.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    # Quantidade
    ttk.Label(frame_selecao, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5)
    entry_quantidade = ttk.Entry(frame_selecao, width=10)
    entry_quantidade.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    # Botões
    btn_adicionar = gui.Button(frame_selecao, text="Adicionar Item", 
                              command=lambda: adicionar_item_venda(), font=("Arial", 12), bg="#4CAF50", fg="white")
    btn_adicionar.grid(row=4, column=0, columnspan=2, pady=10)

    # Tabela de itens da venda atual
    tree_itens = ttk.Treeview(gui.App, columns=("Produto", "Quantidade", "Valor Unit.", "Total", "ID"), 
                             show="headings", height=5)
    tree_itens.heading("Produto", text="Produto")
    tree_itens.heading("Quantidade", text="Quantidade")
    tree_itens.heading("Valor Unit.", text="Valor Unit.")
    tree_itens.heading("Total", text="Total")
    gui.canvas.create_window(700, 350, window=tree_itens, width=600)

    # Frame para valor total e desconto
    frame_valor = ttk.Frame(gui.App)
    gui.canvas.create_window(700, 430, window=frame_valor)

    # Valor calculado
    ttk.Label(frame_valor, text="Valor calculado:").grid(row=0, column=0, padx=5, pady=5)
    lbl_valor_calculado = ttk.Label(frame_valor, text="R$ 0,00")
    lbl_valor_calculado.grid(row=0, column=1, padx=5, pady=5)

    # Valor final
    ttk.Label(frame_valor, text="Valor final:").grid(row=0, column=2, padx=5, pady=5)
    entry_valor_final = ttk.Entry(frame_valor, width=15)
    entry_valor_final.grid(row=0, column=3, padx=5, pady=5)

    # Botões de controle dos itens
    btn_remover = gui.Button(gui.App, text="Remover Item",
                            command=lambda: remover_item_venda(),
                            font=("Arial", 12),
                            bg="#f44336",
                            fg="white")
    gui.canvas.create_window(650, 470, window=btn_remover)
    
    btn_finalizar = gui.Button(gui.App, text="Finalizar Venda",
                              command=lambda: finalizar_venda(tree_itens),
                              font=("Arial", 12),
                              bg="#2196F3",
                              fg="white")
    gui.canvas.create_window(775, 470, window=btn_finalizar)

    # Histórico de Vendas
    tree_vendas = ttk.Treeview(gui.App, 
                              columns=("ID", "Cliente", "Valor Total", "Data"), 
                              show="headings", height=10)
    tree_vendas.heading("ID", text="ID")
    tree_vendas.heading("Cliente", text="Cliente")
    tree_vendas.heading("Valor Total", text="Valor Total")
    tree_vendas.heading("Data", text="Data")
    gui.canvas.create_window(700, 580, window=tree_vendas, width=800, height=125)

    # Botão Excluir Venda
    btn_excluir = gui.Button(gui.App, text="Excluir Venda",
                            command=lambda: excluir_venda(),
                            font=("Arial", 12),
                            bg="#f44336",
                            fg="white")
    gui.canvas.create_window(700, 680, window=btn_excluir)
    
    atualizar_historico_vendas()
    tree_itens.bind("<Delete>", del_para_remover_item_venda)
    tree_vendas.bind("<Delete>", del_para_excluir_venda)

def pesquisar_clientes(event=None):
    termo_busca = entry_cliente_search.get().strip().lower()
    
    # Limpar lista atual
    for item in list_clientes.get_children():
        list_clientes.delete(item)
    
    # Se o campo estiver vazio, esconde a lista e retorna
    if not termo_busca:
        list_clientes.pack_forget()
        gui.canvas.itemconfig(frame_pesquisa_cliente_window, state='hidden')
        return
    
    # Esconder frame de produtos se estiver visível
    gui.canvas.itemconfig(frame_pesquisa_produto_window, state='hidden')
    
    # Mostrar frame de pesquisa de clientes
    gui.canvas.itemconfig(frame_pesquisa_cliente_window, state='normal')
    
    # Exibir a lista de clientes
    list_clientes.pack(padx=5, pady=5)
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    # Busca com LIKE para encontrar correspondências parciais
    cursor.execute("""
        SELECT codigo_cliente, nome 
        FROM clientes 
        WHERE LOWER(nome) LIKE ? 
        ORDER BY nome
    """, (f"%{termo_busca}%",))
    
    clientes = cursor.fetchall()
    conn.close()
    
    for cliente in clientes:
        list_clientes.insert("", "end", values=(cliente[0], cliente[1]))

def pesquisar_produtos(event=None):
    termo_busca = entry_produto_search.get().strip().lower()
    
    # Limpar lista atual
    for item in list_produtos.get_children():
        list_produtos.delete(item)
    
    # Se o campo estiver vazio, esconde a lista e retorna
    if not termo_busca:
        list_produtos.pack_forget()
        gui.canvas.itemconfig(frame_pesquisa_produto_window, state='hidden')
        return
    
    # Esconder frame de clientes se estiver visível
    gui.canvas.itemconfig(frame_pesquisa_cliente_window, state='hidden')
    
    # Mostrar frame de pesquisa de produtos
    gui.canvas.itemconfig(frame_pesquisa_produto_window, state='normal')
    
    # Exibir a lista de produtos
    list_produtos.pack(padx=5, pady=5)
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    # Busca produtos com quantidade maior que 0 no estoque
    cursor.execute("""
        SELECT id, descricao, detalhe, tamanho, preco_venda, promocao, preco_promocional, quantidade
        FROM produtos 
        WHERE (LOWER(descricao) LIKE ? OR LOWER(detalhe) LIKE ?)
        AND quantidade > 0
        ORDER BY descricao
    """, (f"%{termo_busca}%", f"%{termo_busca}%"))
    
    produtos = cursor.fetchall()
    conn.close()
    
    for produto in produtos:
        id_, desc, detalhe, tamanho, preco_normal, em_promocao, preco_promo, quantidade = produto
        
        # Verificar quantidade disponível considerando itens no carrinho
        quantidade_no_carrinho = sum(
            int(tree_itens.item(item)["values"][1])
            for item in tree_itens.get_children()
            if tree_itens.item(item)["values"][4] == id_
        )
        
        quantidade_disponivel = quantidade - quantidade_no_carrinho
        
        # Só exibir produtos com estoque disponível
        if quantidade_disponivel > 0:
            descricao = f"{desc} {detalhe} {tamanho}"
            preco = preco_promo if em_promocao and preco_promo else preco_normal
            preco_str = f"R${preco:.2f}" + (" (PROMOÇÃO)" if em_promocao and preco_promo else "")
            list_produtos.insert("", "end", values=(id_, descricao, preco_str))

def cliente_selecionado(event=None):
    selected = list_clientes.selection()
    if selected:
        cliente = list_clientes.item(selected[0])["values"]
        list_clientes.pack_forget()
        entry_cliente_search.delete(0, 'end')
        entry_cliente_search.insert(0, cliente[1])
        gui.canvas.itemconfig(frame_pesquisa_cliente_window, state='hidden')

def produto_selecionado(event=None):
    selected = list_produtos.selection()
    if selected:
        produto = list_produtos.item(selected[0])["values"]
        list_produtos.pack_forget()
        entry_produto_search.delete(0, 'end')
        entry_produto_search.insert(0, produto[1])
        gui.canvas.itemconfig(frame_pesquisa_produto_window, state='hidden')
        atualizar_estoque_disponivel()

def adicionar_item_venda():
    selected_produtos = list_produtos.selection()
    atualizar_estoque_disponivel()
    if not selected_produtos or not entry_quantidade.get():
        gui.messagebox.showerror("Erro", "Selecione um produto e informe a quantidade")
        return

    try:
        quantidade = int(entry_quantidade.get())
        if quantidade <= 0:
            raise ValueError()
    except ValueError:
        gui.messagebox.showerror("Erro", "Quantidade inválida")
        return

    produto_values = list_produtos.item(selected_produtos[0])["values"]
    produto_id = produto_values[0]
    produto_info = produto_values[1]
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT quantidade, preco_venda, promocao, preco_promocional 
        FROM produtos 
        WHERE id = ?
    """, (produto_id,))
    
    produto = cursor.fetchone()
    if not produto:
        conn.close()
        return
        
    estoque, preco_normal, em_promocao, preco_promocional = produto
    
    # Verificar quantidade disponível considerando itens já no carrinho
    estoque_atual = estoque - sum(
        int(tree_itens.item(item)["values"][1]) 
        for item in tree_itens.get_children()
        if tree_itens.item(item)["values"][4] == produto_id
    )
    
    if quantidade > estoque_atual:
        gui.messagebox.showerror("Erro", "Quantidade maior que o estoque disponível")
        conn.close()
        return

    preco = preco_promocional if em_promocao and preco_promocional else preco_normal
    valor_total = quantidade * preco
    
    # Adicionar indicador de promoção ao nome do produto se aplicável
    if em_promocao and preco_promocional:
        produto_info += " (PROMOÇÃO)"
    
    tree_itens.insert("", "end", values=(produto_info, quantidade, f"R${preco:.2f}", f"R${valor_total:.2f}", produto_id))
    
    # Limpar campos após adicionar
    entry_quantidade.delete(0, 'end')
    entry_produto_search.delete(0, 'end')
    
    # Atualizar valor calculado
    valor_calculado = sum(float(tree_itens.item(item)["values"][3].replace("R$", "")) 
                         for item in tree_itens.get_children())
    lbl_valor_calculado.config(text=f"R$ {valor_calculado:.2f}")
    entry_valor_final.delete(0, 'end')
    entry_valor_final.insert(0, f"{valor_calculado:.2f}")
    
    # Ocultar lista de produtos
    list_produtos.pack_forget()
    gui.canvas.itemconfig(frame_pesquisa_produto_window, state='hidden')

    conn.close()

def finalizar_venda(tree_itens):
    selected_clients = list_clientes.selection()
    if not selected_clients or len(tree_itens.get_children()) == 0:
        gui.messagebox.showerror("Erro", "Selecione um cliente e adicione itens à venda")
        return

    try:
        valor_final = float(entry_valor_final.get().replace(",", "."))
    except ValueError:
        gui.messagebox.showerror("Erro", "Valor final inválido")
        return

    cliente_id = list_clientes.item(selected_clients[0])["values"][0]
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    try:
        # Inserir venda principal - removido produto_id do INSERT
        cursor.execute("""
            INSERT INTO vendas (cliente_id, valor_total, data_venda)
            VALUES (?, ?, datetime('now', 'localtime'))
        """, (cliente_id, valor_final))
        
        venda_id = cursor.lastrowid

        # Inserir itens da venda
        for item in tree_itens.get_children():
            valores = tree_itens.item(item)["values"]
            quantidade = int(valores[1])
            valor_unitario = float(valores[2].replace("R$", "").strip())
            produto_id = valores[4]  # ID do produto
            
            # Inserir item da venda
            cursor.execute("""
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, valor_unitario)
                VALUES (?, ?, ?, ?)
            """, (venda_id, produto_id, quantidade, valor_unitario))
            
            # Atualizar estoque
            cursor.execute("""
                UPDATE produtos 
                SET quantidade = quantidade - ? 
                WHERE id = ?
            """, (quantidade, produto_id))

        conn.commit()
        gui.messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
        
        # Limpar interface após venda bem sucedida
        for item in tree_itens.get_children():
            tree_itens.delete(item)
        
        entry_cliente_search.delete(0, 'end')
        entry_produto_search.delete(0, 'end')
        entry_quantidade.delete(0, 'end')
        entry_valor_final.delete(0, 'end')
        
        atualizar_historico_vendas()

    except Exception as e:
        conn.rollback()
        gui.messagebox.showerror("Erro", f"Erro ao finalizar venda: {str(e)}")
    finally:
        conn.close()

def atualizar_historico_vendas():
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.id, c.nome, v.valor_total, v.data_venda 
        FROM vendas v 
        JOIN clientes c ON v.cliente_id = c.codigo_cliente 
        ORDER BY v.data_venda DESC
    """)
    
    vendas = cursor.fetchall()
    
    for item in tree_vendas.get_children():
        tree_vendas.delete(item)
        
    for venda in vendas:
        tree_vendas.insert("", "end", values=(
            venda[0],
            venda[1],
            f"R${venda[2]:.2f}",
            venda[3]
        ))
    
    conn.close()

def excluir_venda():
    selected_item = tree_vendas.selection()
    if not selected_item:
        gui.messagebox.showerror("Erro", "Selecione uma venda para excluir")
        return
    
    if not gui.messagebox.askyesno("Confirmar", "Deseja realmente excluir esta venda?"):
        return
        
    venda_id = tree_vendas.item(selected_item[0])["values"][0]
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    try:
        # Primeiro, recuperar os itens da venda para restaurar o estoque
        cursor.execute("""
            SELECT produto_id, quantidade 
            FROM itens_venda 
            WHERE venda_id = ?
        """, (venda_id,))
        itens = cursor.fetchall()
        
        # Restaurar o estoque
        for item in itens:
            produto_id, quantidade = item
            cursor.execute("""
                UPDATE produtos 
                SET quantidade = quantidade + ? 
                WHERE id = ?
            """, (quantidade, produto_id))
        
        # Excluir os itens da venda
        cursor.execute("DELETE FROM itens_venda WHERE venda_id = ?", (venda_id,))
        
        # Excluir a venda
        cursor.execute("DELETE FROM vendas WHERE id = ?", (venda_id,))
        
        conn.commit()
        gui.messagebox.showinfo("Sucesso", "Venda excluída com sucesso!")
        
        # Atualizar a interface
        atualizar_historico_vendas()
        
    except Exception as e:
        conn.rollback()
        gui.messagebox.showerror("Erro", f"Erro ao excluir venda: {str(e)}")
    finally:
        conn.close()

def remover_item_venda():
    selected_item = tree_itens.selection()
    if not selected_item:
        gui.messagebox.showerror("Erro", "Selecione um item para remover")
        return
        
    if gui.messagebox.askyesno("Confirmar", "Deseja remover este item da venda?"):
        tree_itens.delete(selected_item)
        # Atualizar valor calculado após remoção
        valor_calculado = sum(float(tree_itens.item(item)["values"][3].replace("R$", "")) 
                            for item in tree_itens.get_children())
        lbl_valor_calculado.config(text=f"R$ {valor_calculado:.2f}")
        entry_valor_final.delete(0, 'end')
        entry_valor_final.insert(0, f"{valor_calculado:.2f}")

def atualizar_estoque_disponivel(event=None):
    selected_items = list_produtos.selection()
    if not selected_items:
        lbl_estoque.config(text="Estoque disponível: -")
        return
        
    try:
        produto_id = list_produtos.item(selected_items[0])["values"][0]
        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        quantidade = cursor.fetchone()[0]
        conn.close()
        
        # Subtrair quantidade dos itens já no carrinho
        quantidade_no_carrinho = sum(
            int(tree_itens.item(item)["values"][1])
            for item in tree_itens.get_children()
            if tree_itens.item(item)["values"][4] == produto_id
        )
        
        quantidade_disponivel = quantidade - quantidade_no_carrinho
        lbl_estoque.config(text=f"Estoque disponível: {quantidade_disponivel}")
    except:
        lbl_estoque.config(text="Estoque disponível: -")

def del_para_remover_item_venda(event):
    remover_item_venda()

def del_para_excluir_venda(event):
    excluir_venda()