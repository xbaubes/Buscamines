from tkinter import Button, messagebox
import random
from typing import List

from casella import Casella

class Buscamines:
    """Classe que crea i gestiona el tauler del joc Buscamines.
    Té una graella d'objectes Casella vinculades a botons de tkinter."""

    def __init__(self, master, configuracio): # Constructor de Buscamines
        self.master = master
        self.configuracio = configuracio
        self.tauler: List[List[Casella]] = [] # Indiquem el tipus de l atribut tauler
        self.caselles_obertes = 0
        self.crear_tauler()

    def crear_tauler(self):
        for i in range(self.configuracio["tauler"]["files"]):
            fila = []
            for j in range(self.configuracio["tauler"]["columnes"]):
                boto = Button( # Creem el Button
                    self.master,
                    width=self.configuracio["cella"]["amplada"],
                    height=self.configuracio["cella"]["alcada"],
                    font=self.configuracio["cella"]["font"],
                    bg=self.configuracio["cella"]["color"],
                    cursor=self.configuracio["cella"]["hover"])
                boto.config(command=lambda i=i, j=j: self.revelar(i, j)) # clic esquerre
                boto.bind("<Button-3>", lambda event, i=i, j=j: self.marcar(i, j)) # click dret
                boto.grid(row=i, column=j) # Afegeix el Button al tauler
                casella = Casella(boto) # Creem una Casella passant el Button com a parametre
                fila.append(casella) # Afegim la Casella a la fila
            self.tauler.append(fila) # Afegim la fila al tauler
        self.posar_mines()

    def posar_mines(self):
        # Generem tantes posicions com numero de bombes requerides, les posicions tenen un valor entre 0 i el nombre de botons que permet la mida del tauler
        posicions = random.sample(range(self.configuracio["tauler"]["files"] * self.configuracio["tauler"]["columnes"]), self.configuracio["tauler"]["mines"])
        for pos in posicions:
            i, j = divmod(pos, self.configuracio["tauler"]["columnes"]) # Convertim les posicions en coordenades i,j (fila,columna)
            self.tauler[i][j].te_mina = True
            self.tauler[i][j].boto.config(bg="blue") # provisional: canvio color cella amb bomba

    def revelar(self, i, j):
        casella = self.tauler[i][j]
        if not casella.revelada:
            if casella.te_mina:
                casella.boto.config(
                    fg=self.configuracio["icona"]["color_bomba"],
                    text=self.configuracio["icona"]["bomba"],
                    bg=self.configuracio["icona"]["perill"],
                    relief="sunken"
                )
                self.final_partida("Has perdut!")
            else:
                self.caselles_obertes += 1
                casella.casella_premuda(self.configuracio)
        if self.caselles_obertes == self.configuracio["tauler"]["files"] * self.configuracio["tauler"]["columnes"] - self.configuracio["tauler"]["mines"]:
            self.final_partida("Has guanyat!")

    def marcar(self, i, j): # Marcar com a possible bomba
        casella = self.tauler[i][j]
        if not casella.revelada:
            casella.boto.config(
                text=self.configuracio["icona"]["bandera"],
                fg=self.configuracio["icona"]["perill"],
                activeforeground=self.configuracio["icona"]["perill"] # Mentres es prem es mante del mateix color
            )

    def final_partida(self, missatge):
        messagebox.showinfo("Buscamines", missatge)
        self.reiniciar()

    def reiniciar(self): # Elimina la partida actual
        self.tauler.clear()
        self.caselles_obertes = 0
        self.crear_tauler()
