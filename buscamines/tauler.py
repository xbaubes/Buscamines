import tkinter as tk
from tkinter import Button

# from casella import Casella

class Tauler:
    """Tauler del Buscamines"""

    def __init__(self, master, config): # Constructor de Tauler
        self.master = master
        self.config = config
        # self.tauler = []
        # self.caselles_obertes = 0
        self.crear_tauler()

    def crear_tauler(self):
        for i in range(self.config["files"]):
            # fila = []
            for j in range(self.config["columnes"]):
                boto = Button( # Creem el Button
                    self.master,
                    width=self.config["amplada_cella"],
                    height=self.config["alcada_cella"],
                    # font=self.config["font_cella"],
                    bg=self.config["color_cella"],
                    cursor=self.config["hover_cella"])
                boto.grid(row=i, column=j) # Afegeix el Button al tauler
                # fila.append(Casella(boto))
            # self.tauler.append(fila)
