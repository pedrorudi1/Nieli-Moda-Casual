from Database import database
from Gui import gui
from tkinter import ttk
import datetime

def abrir_cadastro_vendas():
    global entry_cliente, entry_produto, entry_quantidade, tree_vendas, combo_clientes
    global combo_produtos, tree_itens, lbl_estoque, lbl_valor_calculado, entry_valor_final

    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")
    
    gui.canvas.create_text(700, 50, text="Registro de Vendas", font=("Arial", 24))

    # Frame para seleção de cliente e produto
    frame_selecao = ttk.Frame(gui.App)
    gui.canvas.create_window(700, 150, window=frame_selecao)

    # Seleção de Cliente
    ttk.Label(frame_selecao, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
    combo_clientes = ttk.Combobox(frame_selecao, width=40)
    combo_clientes.grid(row=0, column=1, padx=5, pady=5)
    atualizar_combo_clientes()

    # Seleção de Produto
    ttk.Label(frame_selecao, text="Produto:").grid(row=1, column=0, padx=5, pady=5)
    combo_produtos = ttk.Combobox(frame_selecao, width=40)
    combo_produtos.grid(row=1, column=1, padx=5, pady=5)
    combo_produtos.bind('<<ComboboxSelected>>', atualizar_estoque_disponivel)
    atualizar_combo_produtos()

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


def atualizar_combo_clientes():
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_cliente, nome FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    
    combo_clientes['values'] = [f"{c[0]} - {c[1]}" for c in clientes]

def atualizar_combo_produtos():
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tipo, cor, tamanho, preco_venda FROM produtos WHERE quantidade > 0")
    produtos = cursor.fetchall()
    conn.close()
    
    combo_produtos['values'] = [f"{p[0]} - {p[1]} {p[2]} {p[3]} (R${p[4]:.2f})" for p in produtos]

def atualizar_estoque_disponivel(event):
    if not combo_produtos.get():
        lbl_estoque.config(text="Estoque disponível: -")
        return
        
    try:
        produto_id = int(combo_produtos.get().split('-')[0].strip())
        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        quantidade = cursor.fetchone()[0]
        conn.close()
        
        lbl_estoque.config(text=f"Estoque disponível: {quantidade}")
    except:
        lbl_estoque.config(text="Estoque disponível: -")

def adicionar_item_venda():
    if not combo_produtos.get() or not entry_quantidade.get():
        gui.messagebox.showerror("Erro", "Selecione um produto e informe a quantidade")
        return

    try:
        quantidade = int(entry_quantidade.get())
        if quantidade <= 0:
            raise ValueError()
    except ValueError:
        gui.messagebox.showerror("Erro", "Quantidade inválida")
        return

    produto_id = int(combo_produtos.get().split('-')[0].strip())
    
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT quantidade, preco_venda FROM produtos WHERE id = ?", (produto_id,))
    estoque, preco = cursor.fetchone()
    conn.close()

    if quantidade > estoque:
        gui.messagebox.showerror("Erro", "Quantidade maior que o estoque disponível")
        return

    valor_total = quantidade * preco
    produto_info = combo_produtos.get().split('-')[1].strip()
    tree_itens.insert("", "end", values=(produto_info, quantidade, f"R${preco:.2f}", f"R${valor_total:.2f}", produto_id))
    entry_quantidade.delete(0, 'end')
    
    # Update calculated value
    valor_calculado = sum(float(tree_itens.item(item)["values"][3].replace("R$", "")) 
                         for item in tree_itens.get_children())
    lbl_valor_calculado.config(text=f"R$ {valor_calculado:.2f}")
    entry_valor_final.delete(0, 'end')
    entry_valor_final.insert(0, f"{valor_calculado:.2f}")

def finalizar_venda(tree_itens):
    if not combo_clientes.get() or len(tree_itens.get_children()) == 0:
        gui.messagebox.showerror("Erro", "Selecione um cliente e adicione itens à venda")
        return

    try:
        valor_final = float(entry_valor_final.get().replace(",", "."))
    except ValueError:
        gui.messagebox.showerror("Erro", "Valor final inválido")
        return

    cliente_id = int(combo_clientes.get().split('-')[0].strip())
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    # Inserir venda usando o valor final manual
    cursor.execute("""
        INSERT INTO vendas (cliente_id, valor_total, data_venda)
        VALUES (?, ?, datetime('now', 'localtime'))
    """, (cliente_id, valor_final))
    
    venda_id = cursor.lastrowid

    # Inserir itens da venda
    for item in tree_itens.get_children():
        valores = tree_itens.item(item)["values"]
        produto_info = valores[0]
        quantidade = int(valores[1])
        valor_unitario = float(valores[2].replace("R$", ""))
        produto_id = valores[4]  # Pegar o ID do produto diretamente
        
        try:
            # Inserir item usando o ID armazenado
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
        except Exception as e:
            conn.rollback()
            gui.messagebox.showerror("Erro", f"Erro ao processar item: {produto_info}")
            return

    conn.commit()
    conn.close()
    
    gui.messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
    for item in tree_itens.get_children():
        tree_itens.delete(item)
    
    atualizar_historico_vendas()
    atualizar_combo_produtos()

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
        atualizar_combo_produtos()
        
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

def del_para_remover_item_venda(event):
    remover_item_venda()

def del_para_excluir_venda(event):
    excluir_venda()