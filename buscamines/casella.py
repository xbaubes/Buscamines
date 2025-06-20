from tkinter import Button

class Casella:
    """Casella del tauler del Buscamines"""

    def __init__(self, boto, configuracio_cella):
        self.boto: Button = boto # Encapsulem el Button de Tkinter, n indiquem el seu tipus
        self.configuracio = configuracio_cella
        self.te_mina = False
        self.revelada = False
        self.marcada = False
        self.adjacents = 0

    def casella_premuda(self, i, j):
        self.revelada = True
        self.boto.config(
            text=self.adjacents,
            relief=self.configuracio["premuda"],
            state="disabled",
            bg=self.configuracio["color_premuda"],
            cursor=self.configuracio["hover_premuda"]
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

    def bomba(self):
        self.boto.config(
            fg=self.configuracio["icona"]["defecte"],
            text=self.configuracio["icona"]["bomba"],
            bg=self.configuracio["icona"]["perill"],
            relief=self.configuracio["premuda"]
        )
