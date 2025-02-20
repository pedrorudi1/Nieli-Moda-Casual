from Database import database
from Gui import gui


    
def abrir_cadastro_clientes():
    from Clientes import cadastrar_cliente, excluir_cliente, preencher_campos_cliente
    global entry_nome, entry_telefone, tree_clientes
    
    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")

    gui.canvas.create_text(700, 50, text="Cadastro de Clientes", font=("Arial", 24))

    gui.canvas.create_text(550, 120, text="Nome:", anchor="e", font=("Arial", 12))
    entry_nome = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 120, window=entry_nome, anchor="w")

    gui.canvas.create_text(550, 160, text="Telefone:", anchor="e", font=("Arial", 12))
    entry_telefone = gui.Entry(gui.App, width=40, font=("Arial", 12))
    gui.canvas.create_window(560, 160, window=entry_telefone, anchor="w")

    btn_cadastrar = gui.Button(gui.App, text="Cadastrar", command=lambda: cadastrar_cliente(entry_nome, entry_telefone, tree_clientes), font=("Arial", 12), bg="#4CAF50", fg="white")
    gui.canvas.create_window(650, 290, window=btn_cadastrar)
    
    btn_atualizar = gui.Button(gui.App, text="Atualizar", command=lambda: atualizar_cliente(), font=("Arial", 12), bg="#2196F3", fg="white")
    gui.canvas.create_window(755, 290, window=btn_atualizar)

    btn_excluir = gui.Button(gui.App, text="Excluir", command=lambda: excluir_cliente(tree_clientes), font=("Arial", 12), bg="#f44336", fg="white")
    gui.canvas.create_window(850, 290, window=btn_excluir)

    tree_clientes = gui.ttk.Treeview(gui.App, columns=("Código", "Nome", "Telefone"), show="headings")
    tree_clientes.column("Código", width=100, minwidth=100, stretch="no")
    tree_clientes.heading("Código", text="Código")
    tree_clientes.column("Nome", width=300, minwidth=300, stretch="yes")
    tree_clientes.heading("Nome", text="Nome")
    tree_clientes.column("Telefone", width=150, minwidth=300, stretch="no")
    tree_clientes.heading("Telefone", text="Telefone")
    gui.canvas.create_window(700, 500, window=tree_clientes, width=800, height=300)
    
    
    tree_clientes.bind("<Double-1>", preencher_campos_cliente)
    tree_clientes.bind("<Delete>", del_para_excluir)

    atualizar_tabela_clientes(tree_clientes)
    
def cadastrar_cliente(entry_nome, entry_telefone, tree_clientes):
    nome = entry_nome.get().strip()
    telefone = entry_telefone.get().strip()
    
    if not nome:
        gui.messagebox.showerror("Erro", "Por favor, preencha o nome do cliente.")
        return
    
    if not telefone:
        telefone = "-"
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO clientes (nome, telefone)
        VALUES (?, ?)
    """, (nome, telefone))
    
    conn.commit()
    gui.messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")
    
    entry_nome.delete(0, gui.END)
    entry_telefone.delete(0, gui.END)
    
    conn.close()
    atualizar_tabela_clientes(tree_clientes)

def atualizar_cliente():
    
    selected_item = tree_clientes.selection()
    if not selected_item:
        gui.messagebox.showwarning("Aviso", "Por favor, selecione um cliente para atualizar.")
        return
    
    selected_item = selected_item[0]
    codigo_cliente = tree_clientes.item(selected_item)['values'][0]
    
    novo_nome = entry_nome.get().strip()
    novo_telefone = entry_telefone.get().strip()
    
               
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET nome=?, telefone=? WHERE codigo_cliente=?",
        (novo_nome, novo_telefone, codigo_cliente))
    
    conn.commit()
    gui.messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
    conn.close()
    
    atualizar_tabela_clientes(tree_clientes)
        
def atualizar_tabela_clientes(tree_clientes):
    
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    
    for item in tree_clientes.get_children():
        tree_clientes.delete(item)
        
    for row in rows:
        tree_clientes.insert("", "end", values=row)
    
    conn.close()
    
def excluir_cliente (tree_clientes):
    selected_item = tree_clientes.selection()
    if not selected_item:
        gui.messagebox.showwarning("Aviso", "Por favor, selecione um cliente para excluir.")
        return

    resposta = gui.messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir este cliente?")
    if resposta:
        codigo_cliente = tree_clientes.item(selected_item)['values'][0]

        conn = database.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vendas WHERE cliente_id = ?", (codigo_cliente,))
            if cursor.fetchone()[0] > 0:
                gui.messagebox.showerror("Erro", "Não é possível excluir um cliente que possui vendas registradas.")
                return

            cursor.execute("DELETE FROM clientes WHERE codigo_cliente = ?", (codigo_cliente,))
            conn.commit()
            tree_clientes.delete(selected_item)
            gui.messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")
            atualizar_tabela_clientes(tree_clientes)
        except database.sqlite3.Error as e:
            conn.rollback()
            gui.messagebox.showerror("Erro", f"Ocorreu um erro ao excluir o cliente: {str(e)}")
        finally:
            conn.close()
            
def preencher_campos_cliente(Event):
    
    item_selecionado = tree_clientes.selection()
    if item_selecionado:
        valores = tree_clientes.item(item_selecionado, 'values')
        
        entry_nome.delete(0, 'end')
        entry_telefone.delete(0, 'end')
        entry_nome.insert(0, valores[1])
        entry_telefone.insert(0, valores[2])

def del_para_excluir(Event):
    excluir_cliente(tree_clientes)