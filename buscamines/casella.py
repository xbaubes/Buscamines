class Casella:
    """Representa una casella del taulell del Buscamines"""
    def __init__(self, boto):
        self.boto = boto
        self.te_mina = False
        self.revelada = False
        self.adjacents = 0
        self.marcada = False
