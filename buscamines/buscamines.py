import tkinter as tk
from tkinter import Button
import random
from typing import List

from casella import Casella

class Buscamines:
    """Classe que crea i gestiona el tauler del joc Buscamines.
    Té una graella d'objectes Casella vinculades a botons de tkinter."""

    def __init__(self, master, configuracio): # Constructor de Buscamines
        self.master = master
        self.config = configuracio
        self.tauler: List[List[Casella]] = [] # Indiquem el tipus de l atribut tauler
        # self.caselles_obertes = 0
        self.crear_tauler()
        self.posar_mines()

    def crear_tauler(self):
        for i in range(self.config["tauler"]["files"]):
            fila = []
            for j in range(self.config["tauler"]["columnes"]):
                boto = Button( # Creem el Button
                    self.master,
                    width=self.config["cella"]["amplada"],
                    height=self.config["cella"]["alcada"],
                    # font=self.config["font_cella"],
                    bg=self.config["cella"]["color"],
                    cursor=self.config["cella"]["hover"])
                boto.grid(row=i, column=j) # Afegeix el Button al tauler
                casella = Casella(boto) # Creem una Casella passant el Button com a parametre
                fila.append(casella) # Afegim la Casella a la fila
            self.tauler.append(fila) # Afegim la fila al tauler

    def posar_mines(self):
        # Generem tantes posicions com numero de bombes requerides, les posicions tenen un valor entre 0 i el nombre de botons que permet la mida del tauler
        posicions = random.sample(range(self.config["tauler"]["files"] * self.config["tauler"]["columnes"]), self.config["tauler"]["mines"])
        for pos in posicions:
            i, j = divmod(pos, self.config["tauler"]["columnes"]) # Convertim les posicions en coordenades i,j (fila,columna)
            self.tauler[i][j].te_mina = True
            self.tauler[i][j].casella_premuda(self.config)

        for f in self.tauler: # provisional: mostro tota la matriu
            for f2 in f:
                print(type(f2.boto))
                print(f2.boto.cget("bg"))
