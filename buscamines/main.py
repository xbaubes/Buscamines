import tkinter as tk
from tkinter import PhotoImage
import os

from config import CONFIGURACIO
from buscamines import Buscamines

if __name__ == "__main__": # Executa el codi nomes si el fitxer s executa directament, no quan s importa
    
    root = tk.Tk() # Crea finestra principal de l aplicacio amb Tkinter
    root.title("Buscamines")
    root.resizable(False, False) # No permet que l'usuari redimensioni la finestra

    ruta_arrel = os.path.dirname(__file__) # Ruta absoluta de la carpeta on es guarda aquest fitxer (main.py)
    ruta_icona = os.path.join(ruta_arrel, "..", "icon", "bomba.png")
    if os.path.exists(ruta_icona):
        icona = PhotoImage(file=ruta_icona)
        root.iconphoto(False, icona)

    Buscamines(root, CONFIGURACIO)
    root.mainloop()
