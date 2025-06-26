import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import requests

from tauler import Tauler
from api import url

class Buscamines:
    """Classe que crea el tauler del joc Buscamines i gestiona la partida."""

    def __init__(self, master, configuracio): # Constructor de Buscamines
        self.master = master
        self.configuracio = configuracio
        self.tauler = self.crear_tauler(master, configuracio)
        self.caselles_obertes = 0
        self.inici_partida = None
        self.partida_finalitzada = False
        self.text_prefix = "Temps: "
        self.text_suffix = " s"
        self.temps_parat = 0.00
        self.etiqueta_temps = tk.Label(self.master,
                                       text=f"{self.text_prefix}{self.temps_parat:.2f}{self.text_suffix}",
                                       font=("Arial", 12))
        self.etiqueta_temps.grid(row=self.configuracio["tauler"]["files"], column=0, columnspan=self.configuracio["tauler"]["columnes"], pady=5)

    def crear_tauler(self, master, configuracio):
        return Tauler(master,
                      configuracio,
                      self.valida_marcat,
                      self.marcar) # 2 Callbacks: Li passem 2 funcions com a parametres

    # Retornant break evita l efecte visual de fer click al boto en cas que no estigui permes
    def valida_marcat(self, event, i, j):
        if self.tauler.tauler[i][j].marcada:
            return "break"
        self.revelar(i, j)

    def revelar(self, i, j, per_adjacencia=False): # 'per_adjacencia': False si s ha clicat, True si es revela per adjacencia
        if self.inici_partida is None and not self.partida_finalitzada:
            self.inici_partida = time.time() # Inicio el cronometre
            self.actualitzar_temps()
        casella = self.tauler.tauler[i][j]
        if not casella.revelada and (not casella.marcada or per_adjacencia):
            if casella.te_mina:
                casella.bomba()
                self.final_partida(False)
            else:
                self.caselles_obertes += 1
                casella.casella_premuda(i, j)
                if casella.adjacents == 0:
                    for x, y in self.tauler.adjacents(i, j):
                        self.revelar(x, y, True)
            if self.caselles_obertes == self.tauler.caselles_sense_bomba() and not self.partida_finalitzada:
                self.final_partida(True)

    def marcar(self, i, j): # Marcar com a possible bomba
        casella = self.tauler.tauler[i][j]
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

        # Funcio de validacio per limitar a 15 caracters
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
        if not self.partida_finalitzada:
            self.partida_finalitzada = True
            files = self.configuracio["tauler"]["files"]
            columnes = self.configuracio["tauler"]["columnes"]
            self.inici_partida = None
            # Mostrem les bombes restants
            for i in range(files):
                for j in range(columnes):
                    casella = self.tauler.tauler[i][j]
                    if casella.te_mina:
                        casella.bomba()
            if victoria:
                self.demanar_info(self.text_temps)
            else:
                messagebox.showinfo("Buscamines", "Has perdut!")
                self.reiniciar()

    def registrar_temps(self, nom, temps):
        # Si nom buit o nomes espais posem "Jugador misteriós"
        nom = nom.strip() or "Jugador misteriós"
        # Dades a afegir, camps "jugador", "temps" i "data_hora"
        dades = {
            "data": {
                "jugador": nom,
                "temps": str(temps).replace(",", "."),
                "data_hora": datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            }
        }
        # Fer la petició POST per guardar les dades
        requests.post(url, json=dades)
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
        for fila in self.tauler.tauler:
            for casella in fila:
                casella.boto.destroy()
        self.caselles_obertes = 0
        self.inici_partida = None
        self.partida_finalitzada = False
        self.actualitzar_etiqueta_temps(self.temps_parat)
        self.tauler = self.crear_tauler(self.master, self.configuracio)
