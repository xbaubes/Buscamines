from tkinter import Tk
import os
import sys

from config import CONFIGURACIO
from buscamines import Buscamines

def resource_path(rel_path): # Aconsegueix el path absolut tant en .py com en .exe
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

if __name__ == "__main__": # Executa el codi nomes si el fitxer s executa directament, no quan s importa
    root = Tk() # Crea finestra principal de l aplicacio amb Tkinter
    root.title("Buscamines")
    root.resizable(False, False) # No permet que l'usuari redimensioni la finestra

    ruta_icona = resource_path("icon/bomba.ico")
    if os.path.exists(ruta_icona):
        root.iconbitmap(ruta_icona)

    Buscamines(root, CONFIGURACIO)
    root.mainloop()
