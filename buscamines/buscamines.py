import tkinter as tk
from tkinter import Button

from casella import Casella

class Buscamines:
    """Taulell del Buscamines"""
    
    def __init__(self, master, config): #Constructor
        self.master = master
        self.config = config
        self.taulell = []
        self.caselles_obertes = 0
        self.crear_taulell()
 
    def crear_taulell(self):
        for i in range(self.config["files"]):
            fila = []
            for j in range(self.config["columnes"]):
                boto = Button(
                    self.master,
                    width=self.config["amplada_cella"],
                    height=self.config["alcada_cella"],
                    font=self.config["font_cella"],
                    bg=self.config["color_cella"])
                boto.grid(row=i, column=j)
                fila.append(Casella(boto))
            self.taulell.append(fila)
