from Database import database
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, ttk, messagebox, Toplevel, Label, Frame, StringVar, END, LEFT, RIGHT, BOTH, Text
from Clientes import abrir_cadastro_clientes
from Produtos import abrir_cadastro_produtos
from Vendas import abrir_cadastro_vendas
from ContasAReceber import abrir_contas_a_receber
from Promocoes import abrir_promocoes
from Dashboard import abrir_dashboard
from Bags import abrir_bags


    
database.criar_banco_dados()

App = Tk()
App.title("Niéli Moda Casual")
#App.iconbitmap(r"Assets/iconbitmap.ico")
App.geometry("1200x740")
App.configure(bg="#E4E1DC")

FotoBG = PhotoImage(file=r"Assets/Background.png")
FotoClientes = PhotoImage(file=r"Assets/Clientes.png")
FotoProdutos = PhotoImage(file=r"Assets/Produtos.png")
FotoVendas = PhotoImage(file=r"Assets/Vendas.png")
FotoRelatorios = PhotoImage(file=r"Assets/Relatorios.png")
FotoContasAReceber = PhotoImage(file=r"Assets/ContasAReceber.png")
FotoPromocoes = PhotoImage(file=r"Assets/Promocoes.png")
FotoBags = PhotoImage(file=r"Assets/Bags.png")

canvas = Canvas(App, width=1200, height=740, bg="#E4E1DC")
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=FotoBG, anchor="nw")


BtnClientes = Button(App, text='Clientes', image=FotoClientes, command=abrir_cadastro_clientes, font=("Arial", 12))
BtnClientes.place(x=52.0, y=40.0)
BtnProdutos = Button(App, text='Produtos', image=FotoProdutos, command=abrir_cadastro_produtos, font=("Arial", 12))
BtnProdutos.place(x=52.0, y=140.0)
BtnVendas = Button(App, text='Vendas', image=FotoVendas, command=abrir_cadastro_vendas, font=("Arial", 12))
BtnVendas.place(x=52.0, y=240.0)
BtnContasAReceber = Button(App, text='Contas a Receber', image=FotoContasAReceber, command=abrir_contas_a_receber, font=("Arial", 12))
BtnContasAReceber.place(x=52.0, y=340.0)
BtnPromocoes = Button(App, text='Promoções', image=FotoPromocoes, command=abrir_promocoes, font=("Arial", 12))
BtnPromocoes.place(x=52.0, y=440.0)
BtnBags = Button(App, text='Bags', image=FotoBags, command=abrir_bags, font=("Arial", 12))
BtnBags.place(x=52.0, y=540.0)
BtnDashboard = Button(App, text='Dashboard', image=FotoRelatorios, command=abrir_dashboard, font=("Arial", 12))
BtnDashboard.place(x=52.0, y=640.0)


App.resizable(True, True)

try:
    import pyi_splash
    pyi_splash.close()
except ImportError:
    pass

App.mainloop()