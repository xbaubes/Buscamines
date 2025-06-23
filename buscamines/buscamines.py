import tkinter as tk
from tkinter import Button, messagebox, simpledialog
from datetime import datetime
import random
import time
import requests
from typing import List

from casella import Casella
from api import url

class Buscamines:
    """Classe que crea i gestiona el tauler del joc Buscamines.
    Té una graella d'objectes Casella vinculades a botons de tkinter."""

    def __init__(self, master, configuracio): # Constructor de Buscamines
        self.master = master
        self.configuracio = configuracio
        self.tauler: List[List[Casella]] = [] # Indiquem el tipus de l atribut tauler
        self.caselles_obertes = 0
        self.inici_partida = None
        self.text_prefix = "Temps: "
        self.text_suffix = " s"
        self.temps_parat = 0.00
        self.etiqueta_temps = tk.Label(self.master,
                                       text=f"{self.text_prefix}{self.temps_parat:.2f}{self.text_suffix}",
                                       font=("Arial", 12))
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
            self.etiqueta_temps.grid(row=self.configuracio["tauler"]["files"], column=0, columnspan=self.configuracio["tauler"]["columnes"], pady=5)
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
        if self.inici_partida is None:
            self.inici_partida = time.time() # Inicio el cronometre
            self.actualitzar_temps()
        casella = self.tauler[i][j]
        if not casella.revelada and (not casella.marcada or per_adjacencia):
            if casella.te_mina:
                casella.bomba()
                self.final_partida(False)
            else:
                self.caselles_obertes += 1
                casella.casella_premuda(i, j)
                if casella.adjacents == 0:
                    for x, y in self.adjacents(i, j):
                        self.revelar(x, y, True)
            if self.caselles_obertes == self.caselles_sense_bomba():
                self.final_partida(True)

    def marcar(self, i, j): # Marcar com a possible bomba
        casella = self.tauler[i][j]
        if not casella.revelada:
            if casella.marcada:
                casella.casella_marcar(False)
            else:
                casella.casella_marcar(True)

    def actualitzar_etiqueta_temps(self, temps):
        self.text_temps = f"{temps:.2f}"
        self.etiqueta_temps.config(text=self.text_prefix + self.text_temps + self.text_suffix)

    def obtenir_temps(self) -> float:
        if self.inici_partida is None:
            return self.temps_parat
        else:
            return round((time.time() - self.inici_partida), 2)

    def actualitzar_temps(self):
        if self.inici_partida is not None:
            temps = self.obtenir_temps()
            self.actualitzar_etiqueta_temps(temps)
            self.master.after(100, self.actualitzar_temps) # Torna a cridar se cada 100 ms

    def demanar_info(self, durada):
        finestra = tk.Toplevel()
        finestra.title("Felicitats!")
        finestra.geometry("300x130")
        finestra.resizable(False, False)

        def en_tancar():
            self.reiniciar()
            finestra.destroy()

        finestra.protocol("WM_DELETE_WINDOW", en_tancar)

        tk.Label(finestra, text=f"Has guanyat en {durada} segons!", font=("Arial", 11)).pack(pady=5)
        tk.Label(finestra, text="Introdueix el teu nom (màx. 15 caràcters):", font=("Arial", 10)).pack()

        # Funció de validació per limitar a 15 caracters
        def validar_input(nou_text):
            return len(nou_text) <= 15

        vcmd = (finestra.register(validar_input), "%P")

        entrada = tk.Entry(finestra, font=("Arial", 10), validate="key", validatecommand=vcmd)
        entrada.pack(pady=5)
        entrada.focus()

        def enviar():
            nom = entrada.get().strip()
            self.registrar_temps(nom, durada)
            finestra.destroy()
            self.reiniciar()

        tk.Button(finestra, text="Desar", command=enviar).pack(pady=5)
        finestra.grab_set()

    def final_partida(self, victoria):
        files = self.configuracio["tauler"]["files"]
        columnes = self.configuracio["tauler"]["columnes"]
        self.inici_partida = None
        # Mostrem les bombes restants
        for i in range(files):
            for j in range(columnes):
                casella = self.tauler[i][j]
                if casella.te_mina:
                    casella.bomba()
        if victoria:
            self.demanar_info(self.text_temps)
        else:
            missatge="Has perdut!"
            messagebox.showinfo("Buscamines", missatge)
            self.reiniciar()

    def registrar_temps(self, nom, temps):
        # Si nom buit o nomes espais posem "Jugador misteriós"
        nom = nom.strip() or "Jugador misteriós"
        # Dades a afegir, camps "jugador", "temps" i "data_hora"
        dades = {
            "data": {
                "jugador": nom,
                "temps": str(temps).replace(",", "."),
                "data_hora": datetime.now().strftime("%d-%m-%Y - %H:%M:%S")
            }
        }
        # Fer la petició POST
        resposta = requests.post(url, json=dades)
        # Mostrar resultat
        self.resultats()

    def resultats(self):
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dades = resposta.json()

            # Filtra per registres amb temps i ordena per temps ascendent
            dades_valides = [f for f in dades if f.get("temps") and f["temps"].replace(".", "", 1).isdigit()]
            dades_ordenades = sorted(dades_valides, key=lambda fila: float(fila["temps"]))

            # Crear finestra
            finestra = tk.Toplevel()
            finestra.title("Millors temps")
            finestra.geometry("300x300")
            finestra.resizable(False, False)
            tk.Label(finestra, text="🏆    TOP 10    🏆", font=("Arial", 12, "bold")).pack(pady=10)

            # Top 10
            for idx, fila in enumerate(dades_ordenades[:10], start=1):
                jugador = fila.get("jugador", "Anònim")
                temps = fila.get("temps")
                text = f"{idx}. {jugador} - {temps} s"
                tk.Label(finestra, text=text, font=("Arial", 10)).pack(anchor="w", padx=20)

    def reiniciar(self): # Elimina la partida actual i preparar ne una de nova
        self.tauler.clear()
        self.caselles_obertes = 0
        self.inici_partida = None
        self.actualitzar_etiqueta_temps(self.temps_parat)
        self.crear_tauler()
