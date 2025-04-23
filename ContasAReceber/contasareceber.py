from Gui import gui
from Database import database
from tkinter import messagebox
import pywhatkit
import time

def abrir_contas_a_receber():
    global tree_vendas, entry_valor_pago, selected_venda, tree_pagamentos, tree_creditos
    global entry_valor_credito, entry_obs_credito
    global combo_clientes, btn_usar_credito, lbl_credito_disponivel, tree_cobranca
    selected_venda = None

    gui.canvas.delete("all")
    gui.canvas.create_image(0, 0, image=gui.FotoBG, anchor="nw")
    
    gui.canvas.create_text(700, 50, text="Contas a Receber", font=("Arial", 24))

    # Criar notebook para as abas
    notebook = gui.ttk.Notebook(gui.App)
    gui.canvas.create_window(700, 400, window=notebook, width=800, height=600)

    # Aba 1 - Registrar Pagamentos
    tab_registrar = gui.ttk.Frame(notebook)
    notebook.add(tab_registrar, text="Registrar Pagamentos")

    # Tabela de vendas pendentes
    tree_vendas = gui.ttk.Treeview(tab_registrar, 
                                  columns=("ID", "Cliente", "Valor Total", "Valor Pago", "Valor Pendente", "Data"), 
                                  show="headings", 
                                  height=10)
    
    tree_vendas.heading("ID", text="ID")
    tree_vendas.heading("Cliente", text="Cliente")
    tree_vendas.heading("Valor Total", text="Valor Total")
    tree_vendas.heading("Valor Pago", text="Valor Pago")
    tree_vendas.heading("Valor Pendente", text="Valor Pendente")
    tree_vendas.heading("Data", text="Data")
    
    tree_vendas.column("ID", width=50)
    tree_vendas.column("Cliente", width=200)
    tree_vendas.column("Valor Total", width=100)
    tree_vendas.column("Valor Pago", width=100)
    tree_vendas.column("Valor Pendente", width=100)
    tree_vendas.column("Data", width=150)
    
    tree_vendas.pack(pady=10)

    # Frame para pagamento
    frame_pagamento = gui.ttk.Frame(tab_registrar)
    frame_pagamento.pack(pady=10)

    # Label com informações da venda selecionada
    lbl_venda_info = gui.ttk.Label(frame_pagamento, text="Selecione uma venda para registrar pagamento")
    lbl_venda_info.grid(row=0, column=0, columnspan=3, pady=10)

    gui.ttk.Label(frame_pagamento, text="Valor do Pagamento: R$").grid(row=1, column=0, padx=5, pady=5)
    entry_valor_pago = gui.ttk.Entry(frame_pagamento)
    entry_valor_pago.grid(row=1, column=1, padx=5, pady=5)

    # Label para exibir crédito disponível
    lbl_credito_disponivel = gui.ttk.Label(frame_pagamento, text="Crédito disponível: R$ 0,00")
    lbl_credito_disponivel.grid(row=1, column=2, padx=5, pady=5)

    # Botão Registrar Pagamento em Dinheiro
    btn_registrar = gui.Button(frame_pagamento, 
                              text="Registrar Pagamento",
                              command=lambda: registrar_pagamento(),
                              font=("Arial", 12),
                              bg="#4CAF50",
                              fg="white")
    btn_registrar.grid(row=2, column=0, pady=10, padx=5)

    # Botão Usar Crédito (inicialmente desabilitado)
    btn_usar_credito = gui.Button(frame_pagamento, 
                                 text="Usar Crédito",
                                 command=lambda: usar_credito_disponivel(),
                                 font=("Arial", 12),
                                 bg="#2196F3",
                                 fg="white",
                                 state="disabled")
    btn_usar_credito.grid(row=2, column=1, pady=10, padx=5)

    # Aba 2 - Histórico de Pagamentos
    tab_historico = gui.ttk.Frame(notebook)
    notebook.add(tab_historico, text="Histórico de Pagamentos")

    # Frame para filtros
    frame_filtros = gui.ttk.Frame(tab_historico)
    frame_filtros.pack(pady=10)

    gui.ttk.Label(frame_filtros, text="Cliente:").grid(row=0, column=0, padx=5)
    combo_clientes = gui.ttk.Combobox(frame_filtros, width=30)
    combo_clientes.grid(row=0, column=1, padx=5)

    gui.ttk.Label(frame_filtros, text="Data Inicial:").grid(row=0, column=2, padx=5)
    entry_data_inicial = gui.ttk.Entry(frame_filtros, width=12)
    entry_data_inicial.grid(row=0, column=3, padx=5)

    gui.ttk.Label(frame_filtros, text="Data Final:").grid(row=0, column=4, padx=5)
    entry_data_final = gui.ttk.Entry(frame_filtros, width=12)
    entry_data_final.grid(row=0, column=5, padx=5)

    btn_filtrar = gui.Button(frame_filtros,
                            text="Filtrar",
                            command=lambda: filtrar_pagamentos(combo_clientes.get(), 
                                                            entry_data_inicial.get(),
                                                            entry_data_final.get()),
                            font=("Arial", 12),
                            bg="#2196F3",
                            fg="white")
    btn_filtrar.grid(row=0, column=6, padx=10)

    # Tabela de pagamentos
    tree_pagamentos = gui.ttk.Treeview(tab_historico,
                                      columns=("ID", "Cliente", "Valor Pago", "Data Pagamento"),
                                      show="headings",
                                      height=10)
    
    tree_pagamentos.heading("ID", text="ID")
    tree_pagamentos.heading("Cliente", text="Cliente")
    tree_pagamentos.heading("Valor Pago", text="Valor Pago")
    tree_pagamentos.heading("Data Pagamento", text="Data Pagamento")
    
    tree_pagamentos.column("ID", width=50)
    tree_pagamentos.column("Cliente", width=200)
    tree_pagamentos.column("Valor Pago", width=100)
    tree_pagamentos.column("Data Pagamento", width=150)
    
    tree_pagamentos.pack(pady=10, fill='both', expand=True)

    # Aba 3 - Créditos
    tab_creditos = gui.ttk.Frame(notebook)
    notebook.add(tab_creditos, text="Créditos")

    # Frame para registro de crédito
    frame_credito = gui.ttk.Frame(tab_creditos)
    frame_credito.pack(pady=10)

    gui.ttk.Label(frame_credito, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
    combo_clientes_credito = gui.ttk.Combobox(frame_credito, width=30)
    combo_clientes_credito.grid(row=0, column=1, padx=5, pady=5)

    gui.ttk.Label(frame_credito, text="Valor: R$").grid(row=1, column=0, padx=5, pady=5)
    entry_valor_credito = gui.ttk.Entry(frame_credito)
    entry_valor_credito.grid(row=1, column=1, padx=5, pady=5)

    gui.ttk.Label(frame_credito, text="Observação:").grid(row=2, column=0, padx=5, pady=5)
    entry_obs_credito = gui.ttk.Entry(frame_credito, width=50)
    entry_obs_credito.grid(row=2, column=1, padx=5, pady=5)

    btn_registrar_credito = gui.Button(frame_credito,
                                     text="Registrar Crédito",
                                     command=lambda: registrar_credito(combo_clientes_credito.get(),
                                                                     entry_valor_credito.get(),
                                                                     entry_obs_credito.get()),
                                     font=("Arial", 12),
                                     bg="#4CAF50",
                                     fg="white")
    btn_registrar_credito.grid(row=3, column=0, columnspan=2, pady=10)

    # Tabela de créditos
    tree_creditos = gui.ttk.Treeview(tab_creditos,
                                    columns=("ID", "Cliente", "Valor", "Data", "Observação"),
                                    show="headings",
                                    height=10)
    
    tree_creditos.heading("ID", text="ID")
    tree_creditos.heading("Cliente", text="Cliente")
    tree_creditos.heading("Valor", text="Valor")
    tree_creditos.heading("Data", text="Data")
    tree_creditos.heading("Observação", text="Observação")
    
    tree_creditos.column("ID", width=50)
    tree_creditos.column("Cliente", width=200)
    tree_creditos.column("Valor", width=100)
    tree_creditos.column("Data", width=150)
    tree_creditos.column("Observação", width=200)
    
    tree_creditos.pack(pady=10, fill='both', expand=True)

    # Aba 4 - Cobrança
    tab_cobranca = gui.ttk.Frame(notebook)
    notebook.add(tab_cobranca, text="Cobrança")

    # Frame para lista de clientes com valores pendentes
    frame_lista = gui.ttk.Frame(tab_cobranca)
    frame_lista.pack(pady=10, fill='both', expand=True)

    # Tabela de clientes com valores pendentes
    tree_cobranca = gui.ttk.Treeview(frame_lista,
                                    columns=("Selecionar", "Cliente", "Telefone", "Valor Pendente"),
                                    show="headings",
                                    height=10)
    
    tree_cobranca.heading("Selecionar", text="Selecionar")
    tree_cobranca.heading("Cliente", text="Cliente")
    tree_cobranca.heading("Telefone", text="Telefone")
    tree_cobranca.heading("Valor Pendente", text="Valor Pendente")
    
    tree_cobranca.column("Selecionar", width=70)
    tree_cobranca.column("Cliente", width=200)
    tree_cobranca.column("Telefone", width=120)
    tree_cobranca.column("Valor Pendente", width=120)
    
    tree_cobranca.pack(pady=10, padx=10, fill='both')

    # Frame para mensagem e botões
    frame_mensagem = gui.ttk.Frame(tab_cobranca)
    frame_mensagem.pack(pady=10, padx=10, fill='x')

    # Campo para mensagem personalizada
    gui.ttk.Label(frame_mensagem, text="Mensagem personalizada:").pack(anchor='w')
    text_mensagem = gui.Text(frame_mensagem, height=4, width=50)
    text_mensagem.pack(pady=5, fill='x')
    
    # Mensagem padrão
    mensagem_padrao = """Olá {cliente}, 
Notamos que você possui um valor pendente de R$ {valor} em nossa loja.
Poderia nos informar quando será possível realizar o pagamento?
Agradecemos sua atenção!"""
    
    text_mensagem.insert('1.0', mensagem_padrao)

    # Frame para botões
    frame_botoes = gui.ttk.Frame(tab_cobranca)
    frame_botoes.pack(pady=10)

    # Botões
    btn_enviar = gui.Button(frame_botoes,
                           text="Enviar Cobrança",
                           command=lambda: enviar_cobranca(tree_cobranca, text_mensagem.get('1.0', 'end-1c')),
                           font=("Arial", 12),
                           bg="#4CAF50",
                           fg="white")
    btn_enviar.pack(side='left', padx=5)

    # Atualizar lista de cobranças
    atualizar_lista_cobrancas(tree_cobranca)

    # Adicionar binding para checkbox
    tree_cobranca.bind('<Button-1>', toggle_checkbox)

    # Inicializar dados
    tree_vendas.bind("<<TreeviewSelect>>", lambda e: on_select_venda())
    tree_cobranca.bind("<Button-1>", toggle_checkbox)
    atualizar_lista_vendas()
    atualizar_combo_clientes(combo_clientes)
    atualizar_combo_clientes(combo_clientes_credito)
    atualizar_historico_pagamentos()
    atualizar_lista_creditos()

def atualizar_lista_vendas():
    conn = database.create_connection()
    cursor = conn.cursor()
    
    # Busca vendas com seus pagamentos
    cursor.execute("""
        SELECT v.id, c.nome, v.valor_total, v.data_venda,
               COALESCE(SUM(p.valor_pago), 0) as valor_pago
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.codigo_cliente
        LEFT JOIN pagamentos p ON v.id = p.venda_id
        GROUP BY v.id
        HAVING v.valor_total > COALESCE(SUM(p.valor_pago), 0)
        ORDER BY v.data_venda DESC
    """)
    
    vendas = cursor.fetchall()
    
    for item in tree_vendas.get_children():
        tree_vendas.delete(item)
        
    for venda in vendas:
        venda_id, cliente, valor_total, data, valor_pago = venda
        valor_pendente = valor_total - valor_pago
        
        tree_vendas.insert("", "end", values=(
            venda_id,
            cliente,
            f"R${valor_total:.2f}",
            f"R${valor_pago:.2f}",
            f"R${valor_pendente:.2f}",
            data
        ))
    
    conn.close()

def on_select_venda():
    selected = tree_vendas.selection()
    if not selected:
        return
        
    global selected_venda
    selected_venda = tree_vendas.item(selected[0])['values']
    
    # Verificar crédito disponível e atualizar interface
    cliente_id = None
    conn = database.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT cliente_id FROM vendas WHERE id = ?", (selected_venda[0],))
        cliente_id = cursor.fetchone()[0]
        atualizar_exibicao_credito(cliente_id)
    except:
        atualizar_exibicao_credito(None)
    finally:
        conn.close()

def verificar_credito_cliente(cliente_id):
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0) 
        FROM creditos 
        WHERE cliente_id = ? AND usado = 0
    """, (cliente_id,))
    
    credito_total = cursor.fetchone()[0]
    conn.close()
    
    return credito_total

def atualizar_credito(cliente_id, valor_usado):
    conn = database.create_connection()
    cursor = conn.cursor()
    
    try:
        # Encontrar o crédito mais antigo não usado
        cursor.execute("""
            SELECT id, valor 
            FROM creditos 
            WHERE cliente_id = ? AND usado = 0 
            ORDER BY data_credito 
            LIMIT 1
        """, (cliente_id,))
        
        credito = cursor.fetchone()
        if not credito:
            raise Exception("Nenhum crédito disponível")
            
        credito_id, valor_credito = credito
        
        if valor_credito > valor_usado:
            # Se o crédito é maior que o valor usado, atualiza o valor restante
            novo_valor = valor_credito - valor_usado
            cursor.execute("""
                UPDATE creditos 
                SET valor = ?
                WHERE id = ?
            """, (novo_valor, credito_id))
        else:
            # Se o crédito é igual ou menor, marca como usado
            cursor.execute("""
                UPDATE creditos 
                SET usado = 1
                WHERE id = ?
            """, (credito_id,))
            
            # Se ainda há valor a ser usado, processa o próximo crédito recursivamente
            valor_restante = valor_usado - valor_credito
            if valor_restante > 0:
                conn.commit()
                conn.close()
                atualizar_credito(cliente_id, valor_restante)
                return
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def atualizar_exibicao_credito(cliente_id):
    if cliente_id:
        credito_disponivel = verificar_credito_cliente(cliente_id)
        lbl_credito_disponivel.config(text=f"Crédito disponível: R$ {credito_disponivel:.2f}")
        if credito_disponivel > 0:
            btn_usar_credito['state'] = 'normal'
        else:
            btn_usar_credito['state'] = 'disabled'
    else:
        lbl_credito_disponivel.config(text="Crédito disponível: R$ 0,00")
        btn_usar_credito['state'] = 'disabled'

def usar_credito_disponivel():
    if not selected_venda:
        gui.messagebox.showerror("Erro", "Selecione uma venda para usar crédito")
        return

    venda_id = selected_venda[0]
    valor_pendente = float(selected_venda[4].replace('R$', '').replace(',', '.'))
    
    cliente_id = None
    conn = database.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT cliente_id FROM vendas WHERE id = ?", (venda_id,))
        cliente_id = cursor.fetchone()[0]
    except Exception as e:
        gui.messagebox.showerror("Erro", "Erro ao obter informações do cliente")
        return
    finally:
        conn.close()

    if not cliente_id:
        gui.messagebox.showerror("Erro", "Cliente não encontrado")
        return

    credito_disponivel = verificar_credito_cliente(cliente_id)
    
    if credito_disponivel <= 0:
        gui.messagebox.showerror("Erro", "Cliente não possui crédito disponível")
        return
        
    valor_credito = min(credito_disponivel, valor_pendente)
    
    try:
        # Registrar uso do crédito
        atualizar_credito(cliente_id, valor_credito)
        
        # Registrar pagamento com crédito
        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pagamentos (cliente_id, venda_id, valor_pago, data_pagamento, tipo_pagamento)
            VALUES (?, ?, ?, datetime('now', 'localtime'), 'CREDITO')
        """, (cliente_id, venda_id, valor_credito))
        conn.commit()
        conn.close()
        
        # Atualizar exibição do crédito após o uso
        atualizar_exibicao_credito(cliente_id)
        
        gui.messagebox.showinfo("Sucesso", f"Crédito de R${valor_credito:.2f} utilizado com sucesso!")
        atualizar_lista_vendas()
        atualizar_historico_pagamentos()
        
    except Exception as e:
        gui.messagebox.showerror("Erro", f"Erro ao processar crédito: {str(e)}")
        return

def registrar_pagamento():
    if not selected_venda:
        gui.messagebox.showerror("Erro", "Selecione uma venda para registrar o pagamento")
        return

    try:
        valor_pago = float(entry_valor_pago.get().replace(',', '.'))
        if valor_pago <= 0:
            raise ValueError()
    except ValueError:
        gui.messagebox.showerror("Erro", "Digite um valor válido para o pagamento")
        return

    venda_id = selected_venda[0]
    cliente_id = None
    
    conn = database.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT cliente_id FROM vendas WHERE id = ?", (venda_id,))
        cliente_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO pagamentos (cliente_id, venda_id, valor_pago, data_pagamento, tipo_pagamento)
            VALUES (?, ?, ?, datetime('now', 'localtime'), 'DINHEIRO')
        """, (cliente_id, venda_id, valor_pago))
        
        conn.commit()
        gui.messagebox.showinfo("Sucesso", "Pagamento registrado com sucesso!")
        entry_valor_pago.delete(0, gui.END)
        atualizar_lista_vendas()
        atualizar_historico_pagamentos()
        
    except Exception as e:
        conn.rollback()
        gui.messagebox.showerror("Erro", f"Erro ao registrar pagamento: {str(e)}")
    finally:
        conn.close()

def filtrar_pagamentos(cliente, data_inicial, data_final):
    conn = database.create_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT p.id, c.nome, p.valor_pago, p.data_pagamento
        FROM pagamentos p
        JOIN clientes c ON p.cliente_id = c.codigo_cliente
        WHERE 1=1
    """
    params = []
    
    if cliente:
        query += " AND c.nome LIKE ?"
        params.append(f"%{cliente}%")
        
    if data_inicial:
        query += " AND date(p.data_pagamento) >= date(?)"
        params.append(data_inicial)
        
    if data_final:
        query += " AND date(p.data_pagamento) <= date(?)"
        params.append(data_final)
        
    query += " ORDER BY p.data_pagamento DESC"
    
    cursor.execute(query, params)
    pagamentos = cursor.fetchall()
    
    for item in tree_pagamentos.get_children():
        tree_pagamentos.delete(item)
        
    for pagamento in pagamentos:
        tree_pagamentos.insert("", "end", values=pagamento)
    
    conn.close()

def atualizar_historico_pagamentos():
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, c.nome, p.valor_pago, p.data_pagamento
        FROM pagamentos p
        JOIN clientes c ON p.cliente_id = c.codigo_cliente
        ORDER BY p.data_pagamento DESC
    """)
    
    pagamentos = cursor.fetchall()
    
    for item in tree_pagamentos.get_children():
        tree_pagamentos.delete(item)
        
    for pagamento in pagamentos:
        tree_pagamentos.insert("", "end", values=pagamento)
    
    conn.close()

def atualizar_combo_clientes(combo):
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome FROM clientes ORDER BY nome")
    clientes = [row[0] for row in cursor.fetchall()]
    
    combo['values'] = clientes
    
    conn.close()

def registrar_credito(cliente, valor, observacao):
    global entry_valor_credito, entry_obs_credito  # Declarar uso das variáveis globais
    
    if not cliente or not valor:
        gui.messagebox.showerror("Erro", "Cliente e valor são obrigatórios")
        return
        
    try:
        valor = float(valor.replace(',', '.'))
        if valor <= 0:
            raise ValueError()
    except ValueError:
        gui.messagebox.showerror("Erro", "Digite um valor válido")
        return
        
    conn = database.create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT codigo_cliente FROM clientes WHERE nome = ?", (cliente,))
        cliente_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO creditos (cliente_id, valor, data_credito, observacao)
            VALUES (?, ?, datetime('now', 'localtime'), ?)
        """, (cliente_id, valor, observacao))
        
        conn.commit()
        gui.messagebox.showinfo("Sucesso", "Crédito registrado com sucesso!")
        
        # Limpar campos usando as variáveis globais
        entry_valor_credito.delete(0, gui.END)
        entry_obs_credito.delete(0, gui.END)
        
        atualizar_lista_creditos()
        
    except Exception as e:
        conn.rollback()
        gui.messagebox.showerror("Erro", f"Erro ao registrar crédito: {str(e)}")
    finally:
        conn.close()

def atualizar_lista_creditos():
    conn = database.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.id, cl.nome, c.valor, c.data_credito, c.observacao
        FROM creditos c
        JOIN clientes cl ON c.cliente_id = cl.codigo_cliente
        ORDER BY c.data_credito DESC
    """)
    
    creditos = cursor.fetchall()
    
    for item in tree_creditos.get_children():
        tree_creditos.delete(item)
        
    for credito in creditos:
        tree_creditos.insert("", "end", values=credito)
    
    conn.close()

def atualizar_lista_cobrancas(tree):
    conn = database.create_connection()
    cursor = conn.cursor()
    
    # Limpar tabela
    for item in tree.get_children():
        tree.delete(item)
    
    # Buscar clientes com valores pendentes
    cursor.execute("""
        SELECT DISTINCT 
            c.nome, 
            CAST(c.telefone AS TEXT) as telefone,
            (v.valor_total - COALESCE(SUM(p.valor_pago), 0)) as valor_pendente
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.codigo_cliente
        LEFT JOIN pagamentos p ON v.id = p.venda_id
        GROUP BY v.id
        HAVING valor_pendente > 0
        ORDER BY c.nome
    """)
    
    for row in cursor.fetchall():
        tree.insert('', 'end', values=('☐', row[0], row[1], f"R$ {row[2]:.2f}"))
    
    conn.close()

def enviar_cobranca(tree, mensagem):
    selecionados = []
    for item in tree.get_children():
        if tree.item(item)['values'][0] == '☒':  # Checkbox marcado
            selecionados.append(tree.item(item)['values'])
    
    if not selecionados:
        messagebox.showerror("Erro", "Selecione pelo menos um cliente para enviar cobrança")
        return

    for cliente in selecionados:
        nome = cliente[1]
        telefone = str(cliente[2]).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        valor = cliente[3]
        
        msg = mensagem.format(cliente=nome, valor=valor)
        
        try:
            # Enviar mensagem via WhatsApp
            pywhatkit.sendwhatmsg_instantly(
                phone_no=f"+55{telefone}",
                message=msg,
                wait_time=15
            )
            time.sleep(2)  # Aguardar envio
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar mensagem para {nome}: {str(e)}")
            continue

    messagebox.showinfo("Sucesso", "Cobranças enviadas com sucesso!")

def toggle_checkbox(event):
    item = tree_cobranca.identify_row(event.y)
    if item:
        valores = list(tree_cobranca.item(item)['values'])
        novo_valor = '☒' if valores[0] == '☐' else '☐'
        valores[0] = novo_valor
        tree_cobranca.item(item, values=tuple(valores))