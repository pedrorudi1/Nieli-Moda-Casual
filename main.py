from Database import database 
from Gui import gui


database.criar_banco_dados()

def main():
    gui.App.mainloop()