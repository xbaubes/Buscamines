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
        files = self.configuracio["tauler"]["files"]
        columnes = self.configuracio["tauler"]["columnes"]
        for i in range(files):
            fila = []
            for j in range(columnes):
                boto = self.crear_boto(i, j)
                casella = Casella(boto, self.configuracio["cella"]) # Creem una Casella passant el Button com a parametre
                fila.append(casella) # Afegim la Casella a la fila
            self.tauler.append(fila) # Afegim la fila al tauler
        self.posar_mines()
        self.calcular_adjacents()

    def crear_boto(self, i, j):
        boto = Button(
            self.master,
            width=self.configuracio["cella"]["amplada"],
            height=self.configuracio["cella"]["alcada"],
            font=self.configuracio["cella"]["font"],
            bg=self.configuracio["cella"]["color"],
            cursor=self.configuracio["cella"]["hover"],
            fg=self.configuracio["cella"]["icona"]["defecte"],
            activeforeground=self.configuracio["cella"]["icona"]["defecte"])
        boto.bind("<Button-1>", lambda event, i=i, j=j: self.valida_marcat(event, i, j)) # Click esquerre
        boto.bind("<Button-3>", lambda event, i=i, j=j: self.marcar(i, j)) # Click dret
        boto.grid(row=i, column=j) # Afegeix el Button al tauler
        return boto

    def posar_mines(self):
        # Generem tantes posicions com numero de bombes requerides, les posicions tenen un valor entre 0 i el nombre de botons que permet la mida del tauler
        posicions = random.sample(range(self.caselles_totals()), self.configuracio["tauler"]["mines"])
        for pos in posicions:
            i, j = divmod(pos, self.configuracio["tauler"]["columnes"]) # Convertim les posicions en coordenades i,j (fila,columna)
            self.tauler[i][j].te_mina = True

    def calcular_adjacents(self):
        files = self.configuracio["tauler"]["files"]
        columnes = self.configuracio["tauler"]["columnes"]
        for i in range(files):
            for j in range(columnes):
                self.tauler[i][j].adjacents = self.comptar_mines_adjacents(i, j)

    def comptar_mines_adjacents(self, i, j):
        return sum(1 for x, y in self.adjacents(i, j) if self.tauler[x][y].te_mina)

    def adjacents(self, i, j): # Retorna les coordenades (x,y) adjacents a la casella
        for x in range(max(0, i - 1), min(self.configuracio["tauler"]["files"], i + 2)):
            for y in range(max(0, j - 1), min(self.configuracio["tauler"]["columnes"], j + 2)):
                if not (x == i and y == j):
                    yield x, y # Fa return per cada iteracio

    def caselles_totals(self):
        return self.configuracio["tauler"]["files"] * self.configuracio["tauler"]["columnes"]

    def caselles_sense_bomba(self):
        return self.caselles_totals() - self.configuracio["tauler"]["mines"]

    # Retornant break evita l efecte visual de fer click al boto en cas que no estigui permes
    def valida_marcat(self, event, i, j):
        if self.tauler[i][j].marcada:
            return "break"
        self.revelar(i, j)

    def revelar(self, i, j, per_adjacencia=False): # 'per_adjacencia': False si s ha clicat, True si es revela per adjacencia
        casella = self.tauler[i][j]
        files = self.configuracio["tauler"]["files"]
        columnes = self.configuracio["tauler"]["columnes"]
        if not casella.revelada and (not casella.marcada or per_adjacencia):
            if casella.te_mina:
                casella.bomba()
                self.final_partida("Has perdut!")
            else:
                self.caselles_obertes += 1
                casella.casella_premuda(i, j)
                if casella.adjacents == 0:
                    for x, y in self.adjacents(i, j):
                        self.revelar(x, y, True)
            if self.caselles_obertes == self.caselles_sense_bomba():
                self.final_partida("Has guanyat!")

    def marcar(self, i, j): # Marcar com a possible bomba
        casella = self.tauler[i][j]
        if not casella.revelada:
            if casella.marcada:
                casella.casella_marcar(False)
            else:
                casella.casella_marcar(True)

    def final_partida(self, missatge):
        files = self.configuracio["tauler"]["files"]
        columnes = self.configuracio["tauler"]["columnes"]
        # Mostrem les bombes restants
        for i in range(files):
            for j in range(columnes):
                casella = self.tauler[i][j]
                if casella.te_mina:
                    casella.bomba()
        messagebox.showinfo("Buscamines", missatge)
        self.reiniciar()

    def reiniciar(self): # Elimina la partida actual i preparar ne una de nova
        self.tauler.clear()
        self.caselles_obertes = 0
        self.crear_tauler()
