from Gui import gui
from Database import database
from tkinter import messagebox, Frame, Label, Entry, Button, LEFT, BOTH, TOP, END
from tkinter import ttk

# Global variables
tree_promocoes = None
tree_produtos = None
entry_filtro = None
lbl_preco_atual = None
entry_preco_promo = None

def abrir_promocoes():
    global tree_promocoes, tree_produtos, entry_filtro, lbl_preco_atual, entry_preco_promo
    
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
                                 columns=("ID", "Descrição", "Detalhe", "Tamanho", "Preço Normal", "Preço Promocional"),
                                 show="headings", 
                                 height=15)

    tree_promocoes.heading("ID", text="ID")
    tree_promocoes.heading("Descrição", text="Descrição")
    tree_promocoes.heading("Detalhe", text="Detalhe")
    tree_promocoes.heading("Tamanho", text="Tamanho")
    tree_promocoes.heading("Preço Normal", text="Preço Normal")
    tree_promocoes.heading("Preço Promocional", text="Preço Promocional")

    tree_promocoes.column("ID", width=50, anchor="center")
    tree_promocoes.column("Descrição", width=150)
    tree_promocoes.column("Detalhe", width=100)
    tree_promocoes.column("Tamanho", width=100)
    tree_promocoes.column("Preço Normal", width=100, anchor="e")
    tree_promocoes.column("Preço Promocional", width=100, anchor="e")

    tree_promocoes.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Frame para botão de remover promoção
    frame_botoes = gui.Frame(tab_produtos)
    frame_botoes.pack(pady=10)

    btn_remover = gui.Button(frame_botoes, 
                          text="Remover da Promoção",
                          command=lambda: remover_promocao(),
                          font=("Arial", 12),
                          bg="#FF5252",
                          fg="white")
    btn_remover.pack(pady=10)

    # Frame para gerenciamento de promoções (segunda aba)
    frame_gerenciar = gui.Frame(tab_gerenciar)
    frame_gerenciar.pack(pady=10, fill=BOTH, expand=True)

    # Frame para pesquisa
    frame_pesquisa = gui.Frame(frame_gerenciar)
    frame_pesquisa.pack(pady=5, fill=BOTH)

    gui.Label(frame_pesquisa, text="Filtrar produtos:", font=("Arial", 12)).pack(side=LEFT, padx=5)
    entry_filtro = gui.Entry(frame_pesquisa, width=40)
    entry_filtro.pack(side=LEFT, padx=5)

    # Tabela de produtos disponíveis
    tree_produtos = ttk.Treeview(frame_gerenciar,
                                columns=("ID", "Descrição", "Detalhe", "Tamanho", "Preço"),
                                show="headings",
                                height=10)
    
    tree_produtos.heading("ID", text="ID")
    tree_produtos.heading("Descrição", text="Descrição")
    tree_produtos.heading("Detalhe", text="Detalhe")
    tree_produtos.heading("Tamanho", text="Tamanho")
    tree_produtos.heading("Preço", text="Preço")

    tree_produtos.column("ID", width=50, anchor="center")
    tree_produtos.column("Descrição", width=200)
    tree_produtos.column("Detalhe", width=150)
    tree_produtos.column("Tamanho", width=100)
    tree_produtos.column("Preço", width=100, anchor="e")

    tree_produtos.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Frame para informações do produto selecionado
    frame_info = gui.Frame(frame_gerenciar)
    frame_info.pack(pady=10, fill=BOTH)

    # Labels e entrada para preço promocional
    frame_preco = gui.Frame(frame_info)
    frame_preco.pack(pady=5)

    lbl_preco_atual = gui.Label(frame_preco, text="Preço Atual: R$ 0.00", font=("Arial", 12))
    lbl_preco_atual.pack(side=LEFT, padx=20)

    gui.Label(frame_preco, text="Preço Promocional: R$", font=("Arial", 12)).pack(side=LEFT)
    entry_preco_promo = gui.Entry(frame_preco, width=10)
    entry_preco_promo.pack(side=LEFT, padx=5)

    # Botão de adicionar promoção
    btn_adicionar = gui.Button(frame_info, 
                              text="Adicionar à Promoção",
                              command=lambda: adicionar_promocao_selecionada(),
                              font=("Arial", 12),
                              bg="#4CAF50",
                              fg="white")
    btn_adicionar.pack(pady=10)

    # Bindings
    entry_filtro.bind('<KeyRelease>', filtrar_produtos_disponiveis)
    tree_produtos.bind('<<TreeviewSelect>>', atualizar_preco_selecionado)
    tree_promocoes.bind('<Delete>', lambda event: remover_promocao())

    # Carregar produtos
    carregar_produtos_disponiveis()

def carregar_produtos_disponiveis():
    """Carrega todos os produtos disponíveis na tabela"""
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)

    conn = database.create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, descricao, detalhe, tamanho, preco_venda
            FROM produtos
            WHERE promocao = 0
            ORDER BY descricao, detalhe, tamanho
        """)

        for row in cursor.fetchall():
            produto_id, descricao, detalhe, tamanho, preco = row
            tree_produtos.insert("", "end", values=(
                produto_id,
                descricao,
                detalhe,
                tamanho,
                f"R$ {preco:.2f}"
            ))

    except database.sqlite3.Error as e:
        print(f"Erro ao carregar produtos: {e}")
    finally:
        conn.close()

def filtrar_produtos_disponiveis(event=None):
    """Filtra os produtos na tabela baseado no texto digitado"""
    termo = entry_filtro.get().lower()
    
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)

    conn = database.create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, descricao, detalhe, tamanho, preco_venda
            FROM produtos
            WHERE promocao = 0
            AND (LOWER(descricao) LIKE ? OR LOWER(detalhe) LIKE ?)
            ORDER BY descricao, detalhe, tamanho
        """, (f'%{termo}%', f'%{termo}%'))

        for row in cursor.fetchall():
            produto_id, descricao, detalhe, tamanho, preco = row
            tree_produtos.insert("", "end", values=(
                produto_id,
                descricao,
                detalhe,
                tamanho,
                f"R$ {preco:.2f}"
            ))

    except database.sqlite3.Error as e:
        print(f"Erro ao filtrar produtos: {e}")
    finally:
        conn.close()

def atualizar_preco_selecionado(event=None):
    """Atualiza o preço atual do produto selecionado na tabela"""
    selecao = tree_produtos.selection()
    if not selecao:
        return

    item = tree_produtos.item(selecao[0])
    preco = item['values'][4].replace('R$ ', '').replace(',', '.')
    lbl_preco_atual.config(text=f"Preço Atual: {item['values'][4]}")

def adicionar_promocao_selecionada():
    """Adiciona o produto selecionado à promoção"""
    selecao = tree_produtos.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um produto primeiro.")
        return

    try:
        preco_promo = float(entry_preco_promo.get().replace(',', '.'))
        item = tree_produtos.item(selecao[0])
        produto_id = item['values'][0]
        preco_atual = float(item['values'][4].replace('R$ ', '').replace(',', '.'))

        if preco_promo >= preco_atual:
            messagebox.showerror("Erro", "O preço promocional deve ser menor que o preço normal.")
            return

        if preco_promo <= 0:
            messagebox.showerror("Erro", "O preço promocional deve ser maior que zero.")
            return

        conn = database.create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE produtos 
            SET promocao = 1, preco_promocional = ? 
            WHERE id = ?
        """, (preco_promo, produto_id))

        conn.commit()
        messagebox.showinfo("Sucesso", "Produto adicionado à promoção!")
        
        # Atualizar as tabelas
        carregar_produtos_disponiveis()
        carregar_produtos_promocao()
        entry_preco_promo.delete(0, END)

    except ValueError:
        messagebox.showerror("Erro", "Digite um valor válido para o preço promocional.")
    except database.sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao adicionar promoção: {str(e)}")
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
            SELECT id, descricao, detalhe, tamanho, preco_venda, preco_promocional
            FROM produtos
            WHERE promocao = 1
            ORDER BY descricao, detalhe, tamanho
        """)

        for row in cursor.fetchall():
            produto_id, descricao, detalhe, tamanho, preco_normal, preco_promo = row
            tree_promocoes.insert("", "end", values=(
                produto_id,
                descricao,
                detalhe,
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
    cursor.execute("SELECT id, descricao, detalhe, tamanho FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return [f"{id} - {descricao} {detalhe} {tamanho}" for id, descricao, detalhe, tamanho in produtos]


def atualizar_preco_atual(event=None):
    try:
        produto_id = tree_produtos.selection()[0]
        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT preco_venda FROM produtos WHERE id = ?", (produto_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            preco_atual = resultado[0]
            lbl_preco_atual.config(text=f"Preço Atual: R$ {preco_atual:.2f}")
        else:
            lbl_preco_atual.config(text="Preço Atual: R$ 0.00")
            
    except Exception as e:
        print(f"Erro ao atualizar preço: {e}")
        lbl_preco_atual.config(text="Preço Atual: R$ 0.00")
    finally:
        conn.close()

def remover_promocao():
    """Remove o produto selecionado da promoção"""
    selecao = tree_promocoes.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um produto primeiro.")
        return

    if messagebox.askyesno("Confirmar", "Deseja realmente remover este produto da promoção?"):
        try:
            item = tree_promocoes.item(selecao[0])
            produto_id = item['values'][0]

            conn = database.create_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE produtos 
                SET promocao = 0, preco_promocional = NULL 
                WHERE id = ?
            """, (produto_id,))

            conn.commit()
            messagebox.showinfo("Sucesso", "Produto removido da promoção!")
            
            # Atualizar as tabelas
            carregar_produtos_promocao()
            carregar_produtos_disponiveis()

        except database.sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao remover promoção: {str(e)}")
        finally:
            conn.close()