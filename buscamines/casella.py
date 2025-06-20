import tkinter as tk

class Casella:
    """Casella del tauler del Buscamines"""

    def __init__(self, boto):
        self.boto: tk.Button = boto # Encapsulem el Button de Tkinter, n indiquem el seu tipus
        self.te_mina = False
        self.revelada = False
        self.marcada = False
        self.adjacents = 0

    def casella_premuda(self, configuracio):
        self.revelada = True
        self.boto.config(
            text=self.adjacents,
            relief="sunken",
            state="disabled",
            bg=configuracio["cella"]["color_premuda"],
            cursor=configuracio["cella"]["hover_premuda"]
        )

    def casella_marcar(self, marcar, configuracio):
        if marcar:
            self.marcada = True
            self.boto.config(
                fg=configuracio["icona"]["perill"],
                activeforeground=configuracio["icona"]["perill"], # Mentres es prem es mante del mateix color
                text=configuracio["icona"]["bandera"]
            )
        else:
            self.marcada = False
            self.boto.config(
                fg=configuracio["icona"]["defecte"],
                activeforeground=configuracio["icona"]["defecte"],
                text=""
            )
