import tkinter as tk

class Casella:
    """Casella del tauler del Buscamines"""

    def __init__(self, boto):
        self.boto: tk.Button = boto # Encapsulem el Button de Tkinter, n indiquem el seu tipus
        self.te_mina = False
        #self.revelada = False
        #self.adjacents = 0
        #self.marcada = False

    def casella_premuda(self,configuracio):
        self.boto.config(
            bg=configuracio["cella"]["color_premuda"], # provisional: canvio color cella amb bomba
            cursor=configuracio["cella"]["hover_premuda"] # provisional: canvio hover cella amb bomba
        )
