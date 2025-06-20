import tkinter as tk

class Casella:
    """Casella del tauler del Buscamines"""

    def __init__(self, boto, configuracio):
        self.boto: tk.Button = boto # Encapsulem el Button de Tkinter, n indiquem el seu tipus
        self.configuracio = configuracio
        self.te_mina = False
        self.revelada = False
        self.marcada = False
        self.adjacents = 0

    def casella_premuda(self, i, j):
        self.revelada = True
        self.boto.config(
            text=self.adjacents,
            relief="sunken",
            state="disabled",
            bg=self.configuracio["cella"]["color_premuda"],
            cursor=self.configuracio["cella"]["hover_premuda"]
        )

    def casella_marcar(self, marcar):
        if marcar:
            self.marcada = True
            self.boto.config(
                fg=self.configuracio["icona"]["perill"],
                activeforeground=self.configuracio["icona"]["perill"], # Mentres es prem es mante del mateix color
                text=self.configuracio["icona"]["bandera"]
            )
        else:
            self.marcada = False
            self.boto.config(
                fg=self.configuracio["icona"]["defecte"],
                activeforeground=self.configuracio["icona"]["defecte"],
                text=""
            )
