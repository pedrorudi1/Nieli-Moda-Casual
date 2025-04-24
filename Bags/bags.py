from Gui import gui
from Database import database
from Vendas import adicionar_item_venda, finalizar_venda
from tkinter import ttk, messagebox
from datetime import datetime

def abrir_bags():
    global tree_bags, combo_clientes, tree_produtos, tree_produtos_selecionados, tree_todas_bags, tree_itens_bag
    
    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")
    gui.canvas.create_text(730, 30, text="Gerenciamento de Bags", font=("Arial", 24))

    # Criar notebook para abas
    notebook = ttk.Notebook(gui.App)
    gui.canvas.create_window(730, 400, window=notebook, width=900, height=650)

    # Aba 1 - Criar Bag
    tab_criar = ttk.Frame(notebook)
    notebook.add(tab_criar, text="Criar Bag")

    # Frame para seleção de cliente
    frame_cliente = ttk.LabelFrame(tab_criar, text="Selecionar Cliente")
    frame_cliente.pack(fill="x", padx=10, pady=5)

    combo_clientes = ttk.Combobox(frame_cliente, width=40)
    combo_clientes.pack(padx=5, pady=5)
    atualizar_combo_clientes()

    # Frame para produtos disponíveis
    frame_produtos = ttk.LabelFrame(tab_criar, text="Produtos Disponíveis")
    frame_produtos.pack(fill="both", expand=True, padx=10, pady=5)

    tree_produtos = ttk.Treeview(frame_produtos, 
                                columns=("ID", "Descrição", "Detalhe", "Tamanho", "Preço"), 
                                show="headings", 
                                height=6)
    
    for col in ("ID", "Descrição", "Detalhe", "Tamanho", "Preço"):
        tree_produtos.heading(col, text=col)
        tree_produtos.column("ID", width=50)
        tree_produtos.column("Descrição", width=200)
        tree_produtos.column("Detalhe", width=100)
        tree_produtos.column("Tamanho", width=100)
        tree_produtos.column("Preço", width=100)
    
    tree_produtos.pack(fill="both", expand=True, padx=5, pady=5)
    atualizar_lista_produtos()

    # Botões de ação
    frame_botoes = ttk.Frame(tab_criar)
    frame_botoes.pack(fill="x", padx=10, pady=5)

    btn_adicionar = gui.Button(frame_botoes, 
                              text="↓ Adicionar à Bag", 
                              command=adicionar_produto_bag,
                              bg="#4CAF50",
                              fg="white")
    btn_adicionar.pack(side="left", padx=5)

    btn_remover = gui.Button(frame_botoes, 
                            text="↑ Remover da Bag", 
                            command=remover_produto_bag,
                            bg="#f44336",
                            fg="white")
    btn_remover.pack(side="left", padx=5)

    # Frame para produtos selecionados
    frame_selecionados = ttk.LabelFrame(tab_criar, text="Produtos na Bag")
    frame_selecionados.pack(fill="both", expand=True, padx=10, pady=5)

    tree_produtos_selecionados = ttk.Treeview(frame_selecionados, 
                                             columns=("ID", "Descrição", "Detalhe", "Tamanho", "Preço"), 
                                             show="headings", 
                                             height=6)
    
    for col in ("ID", "Descrição", "Detalhe", "Tamanho", "Preço"):
        tree_produtos_selecionados.heading(col, text=col)
        tree_produtos_selecionados.column(col, width=100)
    
    tree_produtos_selecionados.pack(fill="both", expand=True, padx=5, pady=5)

    # Botão finalizar
    btn_finalizar = gui.Button(tab_criar, 
                              text="Finalizar Bag", 
                              command=finalizar_bag,
                              bg="#2196F3",
                              fg="white",
                              width=20)
    btn_finalizar.pack(pady=10)

    # Aba 2 - Visualizar Bags
    tab_visualizar = ttk.Frame(notebook)
    notebook.add(tab_visualizar, text="Visualizar Bags")

    # Frame para lista de todas as bags
    frame_todas_bags = ttk.LabelFrame(tab_visualizar, text="Bags Cadastradas")
    frame_todas_bags.pack(fill="both", expand=True, padx=10, pady=5)

    # Treeview para todas as bags
    tree_todas_bags = ttk.Treeview(frame_todas_bags,
                                  columns=("ID", "Cliente", "Data Criação", "Tempo", "Qtd Itens", "Valor Total", "Status"),
                                  show="headings",
                                  height=8)
    
    tree_todas_bags.heading("ID", text="ID")
    tree_todas_bags.heading("Cliente", text="Cliente")
    tree_todas_bags.heading("Data Criação", text="Data Criação")
    tree_todas_bags.heading("Tempo", text="Tempo com Cliente")
    tree_todas_bags.heading("Qtd Itens", text="Qtd Itens")
    tree_todas_bags.heading("Valor Total", text="Valor Total")
    tree_todas_bags.heading("Status", text="Status")

    tree_todas_bags.column("ID", width=50)
    tree_todas_bags.column("Cliente", width=200)
    tree_todas_bags.column("Data Criação", width=150)
    tree_todas_bags.column("Tempo", width=150)
    tree_todas_bags.column("Qtd Itens", width=100)
    tree_todas_bags.column("Valor Total", width=100)
    tree_todas_bags.column("Status", width=100)

    tree_todas_bags.pack(fill="both", expand=True, padx=5, pady=5)

    # Frame para itens da bag selecionada
    frame_itens_bag = ttk.LabelFrame(tab_visualizar, text="Itens da Bag Selecionada")
    frame_itens_bag.pack(fill="both", expand=True, padx=10, pady=5)

    # Treeview para itens da bag
    tree_itens_bag = ttk.Treeview(frame_itens_bag,
                                 columns=("Selecionar", "ID", "Descrição", "Detalhe", "Tamanho", "Preço", "Status"),
                                 show="headings",
                                 height=6)
    
    tree_itens_bag.heading("Selecionar", text="")
    tree_itens_bag.heading("ID", text="ID")
    tree_itens_bag.heading("Descrição", text="Descrição")
    tree_itens_bag.heading("Detalhe", text="Detalhe")
    tree_itens_bag.heading("Tamanho", text="Tamanho")
    tree_itens_bag.heading("Preço", text="Preço")
    tree_itens_bag.heading("Status", text="Status")
    
    tree_itens_bag.column("Selecionar", width=30)
    tree_itens_bag.column("ID", width=50)
    tree_itens_bag.column("Descrição", width=150)
    tree_itens_bag.column("Detalhe", width=100)
    tree_itens_bag.column("Tamanho", width=100)
    tree_itens_bag.column("Preço", width=100)
    tree_itens_bag.column("Status", width=100)
    
    tree_itens_bag.pack(fill="both", expand=True, padx=5, pady=5)

    # Botões de controle
    frame_controles = ttk.Frame(tab_visualizar)
    frame_controles.pack(fill="x", padx=10, pady=5)

    btn_finalizar_selecao = gui.Button(frame_controles,
                                      text="Finalizar Seleção",
                                      command=finalizar_selecao_bag,
                                      bg="#4CAF50",
                                      fg="white")
    btn_finalizar_selecao.pack(side="left", padx=5)

    btn_cancelar_bag = gui.Button(frame_controles,
                                 text="Cancelar Bag",
                                 command=cancelar_bag,
                                 bg="#f44336",
                                 fg="white")
    btn_cancelar_bag.pack(side="left", padx=5)

    btn_vender_selecao = gui.Button(frame_controles,
                                   text="Vender Selecionados",
                                   command=vender_itens_selecionados,
                                   bg="#2196F3",
                                   fg="white")
    btn_vender_selecao.pack(side="left", padx=5)

    # Configurar eventos
    tree_todas_bags.bind("<<TreeviewSelect>>", on_selecionar_bag)
    tree_itens_bag.bind("<Button-1>", toggle_item_selection)
    atualizar_lista_bags()

def on_selecionar_bag(event=None):
    selected = tree_todas_bags.selection()
    if not selected:
        return
        
    bag_id = tree_todas_bags.item(selected[0])['values'][0]
    atualizar_itens_bag(bag_id)

def atualizar_itens_bag(bag_id):
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            p.id, 
            p.descricao, 
            p.detalhe, 
            p.tamanho, 
            CASE 
                WHEN p.preco_promocional > 0 THEN p.preco_promocional 
                ELSE p.preco_venda 
            END as preco_final,
            i.status
        FROM itens_bag i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.bag_id = ?
    """, (bag_id,))
    
    itens = cursor.fetchall()
    
    for item in tree_itens_bag.get_children():
        tree_itens_bag.delete(item)
        
    for item in itens:
        tree_itens_bag.insert("", "end", values=(
            '☐',  # Checkbox desmarcado
            *item  # Resto dos valores
        ))
    
    conn.close()

def atualizar_lista_bags():
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            b.id, 
            c.nome, 
            b.data_criacao, 
            b.status,
            COUNT(i.id) as qtd_itens,
            SUM(
                CASE 
                    WHEN p.preco_promocional > 0 THEN p.preco_promocional 
                    ELSE p.preco_venda 
                END
            ) as valor_total
        FROM bags b
        JOIN clientes c ON b.cliente_id = c.codigo_cliente
        JOIN itens_bag i ON i.bag_id = b.id
        JOIN produtos p ON i.produto_id = p.id
        GROUP BY b.id
        ORDER BY b.data_criacao DESC
    """)
    
    bags = cursor.fetchall()
    
    for item in tree_todas_bags.get_children():
        tree_todas_bags.delete(item)
        
    for bag in bags:
        data_criacao = datetime.strptime(bag[2], '%Y-%m-%d %H:%M:%S')
        tempo_decorrido = datetime.now() - data_criacao
        dias = tempo_decorrido.days
        horas = tempo_decorrido.seconds // 3600
        
        tree_todas_bags.insert("", "end", values=(
            bag[0],  # ID
            bag[1],  # Cliente
            data_criacao.strftime('%d/%m/%Y %H:%M'),  # Data Criação
            f"{dias}d {horas}h",  # Tempo com Cliente
            bag[4],  # Qtd Itens
            f"R$ {bag[5]:.2f}",  # Valor Total
            bag[3]   # Status
        ))
    
    conn.close()

def finalizar_selecao_bag():
    selected = tree_todas_bags.selection()
    if not selected:
        messagebox.showerror("Erro", "Selecione uma bag para finalizar")
        return
        
    bag_id = tree_todas_bags.item(selected[0])['values'][0]
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    try:
        # Retornar ao estoque os produtos não vendidos
        cursor.execute("""
            UPDATE produtos 
            SET quantidade = quantidade + 1
            WHERE id IN (
                SELECT produto_id 
                FROM itens_bag 
                WHERE bag_id = ? AND status != 'VENDIDO'
            )
        """, (bag_id,))
        
        cursor.execute("UPDATE bags SET status = 'FINALIZADA' WHERE id = ?", (bag_id,))
        cursor.execute("UPDATE itens_bag SET status = 'FINALIZADO' WHERE bag_id = ? AND status != 'VENDIDO'", (bag_id,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Bag finalizada com sucesso!")
        atualizar_lista_bags()
        
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Erro ao finalizar bag: {str(e)}")
    finally:
        conn.close()

def cancelar_bag():
    selected = tree_todas_bags.selection()
    if not selected:
        messagebox.showerror("Erro", "Selecione uma bag para cancelar")
        return
        
    bag_id = tree_todas_bags.item(selected[0])['values'][0]
    
    if not messagebox.askyesno("Confirmar", "Deseja realmente cancelar esta bag?"):
        return
        
    conn = database.create_connection()
    cursor = conn.cursor()
    
    try:
        # Retornar produtos ao estoque
        cursor.execute("""
            UPDATE produtos 
            SET quantidade = quantidade + 1
            WHERE id IN (
                SELECT produto_id 
                FROM itens_bag 
                WHERE bag_id = ? AND status != 'VENDIDO'
            )
        """, (bag_id,))

        # Atualizar status da bag e seus itens
        cursor.execute("UPDATE bags SET status = 'CANCELADA' WHERE id = ?", (bag_id,))
        cursor.execute("UPDATE itens_bag SET status = 'CANCELADO' WHERE bag_id = ? AND status != 'VENDIDO'", (bag_id,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Bag cancelada com sucesso!")
        atualizar_lista_bags()
        atualizar_lista_produtos()  # Atualizar lista de produtos para mostrar estoque atualizado
        
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Erro ao cancelar bag: {str(e)}")
    finally:
        conn.close()

def atualizar_combo_clientes():
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_cliente, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()
    conn.close()
    
    combo_clientes['values'] = [f"{c[0]} - {c[1]}" for c in clientes]

def atualizar_lista_produtos():
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            id, 
            descricao, 
            detalhe, 
            tamanho,
            CASE 
                WHEN preco_promocional > 0 THEN preco_promocional 
                ELSE preco_venda 
            END as preco_final,
            quantidade 
        FROM produtos 
        WHERE quantidade > 0 
        ORDER BY descricao, detalhe, tamanho
    """)
    produtos = cursor.fetchall()
    conn.close()

    # Limpar lista atual
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)

    # Inserir apenas produtos com estoque
    for produto in produtos:
        tree_produtos.insert("", "end", values=(
            produto[0],      # ID
            produto[1],      # Descrição
            produto[2],      # Detalhe
            produto[3],      # Tamanho
            f"R$ {produto[4]:.2f}"  # Preço (normal ou promocional)
        ))

def adicionar_produto_bag():
    if not combo_clientes.get():
        messagebox.showerror("Erro", "Selecione um cliente")
        return

    selected_item = tree_produtos.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um produto para adicionar à bag")
        return

    conn = database.create_connection()
    cursor = conn.cursor()

    # Verificar estoque antes de adicionar
    produto_valores = tree_produtos.item(selected_item[0])['values']
    cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_valores[0],))
    quantidade = cursor.fetchone()[0]
    
    if quantidade <= 0:
        messagebox.showerror("Erro", "Produto sem estoque disponível")
        conn.close()
        return

    # Verificar se o produto já está na bag
    for item in tree_produtos_selecionados.get_children():
        if tree_produtos_selecionados.item(item)['values'][0] == produto_valores[0]:
            messagebox.showerror("Erro", "Este produto já está na bag")
            conn.close()
            return

    # Se chegou aqui, pode adicionar o produto
    tree_produtos_selecionados.insert("", "end", values=produto_valores)
    conn.close()

def remover_produto_bag():
    selected_item = tree_produtos_selecionados.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um produto para remover da bag")
        return

    tree_produtos_selecionados.delete(selected_item)

def finalizar_bag():
    if not combo_clientes.get():
        messagebox.showerror("Erro", "Selecione um cliente")
        return

    produtos_selecionados = tree_produtos_selecionados.get_children()
    if not produtos_selecionados:
        messagebox.showerror("Erro", "Adicione produtos à bag")
        return

    cliente_id = combo_clientes.get().split(' - ')[0]
    
    try:
        conn = database.create_connection()
        cursor = conn.cursor()

        # Inserir nova bag
        cursor.execute("""
            INSERT INTO bags (cliente_id, data_criacao, status)
            VALUES (?, datetime('now', 'localtime'), 'PENDENTE')
        """, (cliente_id,))
        
        bag_id = cursor.lastrowid

        # Inserir itens da bag e atualizar estoque temporariamente
        for item in produtos_selecionados:
            produto_id = tree_produtos_selecionados.item(item)['values'][0]
            
            # Reduzir quantidade do produto temporariamente
            cursor.execute("""
                UPDATE produtos 
                SET quantidade = quantidade - 1 
                WHERE id = ?
            """, (produto_id,))
            
            cursor.execute("""
                INSERT INTO itens_bag (bag_id, produto_id, status)
                VALUES (?, ?, 'PENDENTE')
            """, (bag_id, produto_id))

        conn.commit()
        messagebox.showinfo("Sucesso", "Bag registrada com sucesso!")
        
        # Limpar seleções
        combo_clientes.set('')
        for item in tree_produtos_selecionados.get_children():
            tree_produtos_selecionados.delete(item)

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Erro ao registrar bag: {str(e)}")
    finally:
        conn.close()
        abrir_bags()

def vender_itens_selecionados():
    selected = tree_todas_bags.selection()
    if not selected:
        messagebox.showerror("Erro", "Selecione uma bag primeiro")
        return
    
    bag_id = tree_todas_bags.item(selected[0])['values'][0]
    cliente_id = None
    
    # Obter itens selecionados para venda
    itens_selecionados = []
    for item in tree_itens_bag.get_children():
        if tree_itens_bag.item(item)['values'][0] == '☒':  # Checkbox marcado
            itens_selecionados.append(tree_itens_bag.item(item)['values'][1:])  # Ignorar coluna de seleção
    
    if not itens_selecionados:
        messagebox.showerror("Erro", "Selecione produtos para vender")
        return
    
    try:
        conn = database.create_connection()
        cursor = conn.cursor()
        
        # Obter cliente_id da bag
        cursor.execute("SELECT cliente_id FROM bags WHERE id = ?", (bag_id,))
        cliente_id = cursor.fetchone()[0]
        
        # Criar nova venda
        valor_total = 0
        for item in itens_selecionados:
            produto_id = item[0]
            # Buscar preço atual (normal ou promocional)
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN preco_promocional > 0 THEN preco_promocional 
                        ELSE preco_venda 
                    END as preco_final
                FROM produtos 
                WHERE id = ?
            """, (produto_id,))
            preco = cursor.fetchone()[0]
            valor_total += preco

        cursor.execute("""
            INSERT INTO vendas (cliente_id, valor_total, data_venda)
            VALUES (?, ?, datetime('now', 'localtime'))
        """, (cliente_id, valor_total))
        
        venda_id = cursor.lastrowid
        
        # Inserir itens vendidos
        for item in itens_selecionados:
            produto_id = item[0]
            # Buscar preço atual novamente para cada item
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN preco_promocional > 0 THEN preco_promocional 
                        ELSE preco_venda 
                    END as preco_final
                FROM produtos 
                WHERE id = ?
            """, (produto_id,))
            valor_unitario = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, valor_unitario)
                VALUES (?, ?, 1, ?)
            """, (venda_id, produto_id, valor_unitario))
            
            # Atualizar status do item na bag
            cursor.execute("""
                UPDATE itens_bag 
                SET status = 'VENDIDO' 
                WHERE bag_id = ? AND produto_id = ?
            """, (bag_id, produto_id))
            
            # Não é necessário atualizar o estoque aqui pois já foi reduzido ao criar a bag
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
        atualizar_itens_bag(bag_id)
        
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Erro ao registrar venda: {str(e)}")
    finally:
        conn.close()

def toggle_item_selection(event):
    item = tree_itens_bag.identify_row(event.y)
    if item:
        valores = list(tree_itens_bag.item(item)['values'])
        if valores[6] != 'VENDIDO':  # Não permite selecionar itens já vendidos
            novo_valor = '☒' if valores[0] == '☐' else '☐'
            valores[0] = novo_valor
            tree_itens_bag.item(item, values=tuple(valores))