import tkinter as tk

class Casella:
    """Casella del tauler del Buscamines"""

    def __init__(self, boto):
        self.boto: tk.Button = boto # Encapsulem el Button de Tkinter, n indiquem el seu tipus
        self.te_mina = False
        self.revelada = False
        #self.marcada = False <- per poder desmarcar

    def casella_premuda(self,configuracio):
        self.revelada = True
        self.boto.config(
            text="",
            relief="sunken",
            state="disabled",
            bg=configuracio["cella"]["color_premuda"],
            cursor=configuracio["cella"]["hover_premuda"]
        )
