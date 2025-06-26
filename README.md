# 💣💣💣💣 Buscamines 💣💣💣💣

Projecte desenvolupat amb Python i Tkinter que reimplementa el clàssic joc del **Buscamines**:
Aplicació gràfica interactiva on has de descobrir cel·les sense explotar les mines.
Inclou registre de puntuacions mitjançant l'API de [SheetDB](https://sheetdb.io).

## 📦 Estructura del projecte

```
buscamines/
├── main.py              # Iniciador de l'aplicació
├── buscamines.py        # Lògica del joc
├── casella.py           # Classe Casella
├── config.py            # Configuració de l'aparença i el joc
└── api.py               # URL de l'API SheetDB
icon/
└── bomba.ico        # Icona per a l'executable
.gitignore
requirements.txt
exe-requirements.txt
```

## ▶️ Requisits

- Python 3.10+
- Dependències per **executar** el joc definides a `requirements.txt`
- Dependències per **crear executable** definides a `exe-requirements.txt`
- Connexió a internet per desar i recuperar puntuacions

## 🎮 Executar el joc

```bash
pip install -r requirements.txt
python main.py
```

## 🗃️ Crear executable

Pots crear una versió executable per a Windows utilitzant `pyinstaller`.

### 1. Instal·la les dependències de d'execució

```bash
pip install -r exe-requirements.txt
```

### 2. Genera l'executable

Assegura’t que el fitxer `bomba.ico` és a la carpeta `../icon/`.

Des de l'arrel del projecte introdueix:

```bash
pyinstaller --onefile --windowed --name=Buscamines --icon=icon/bomba.ico --add-data "icon/bomba.ico;icon" buscamines/main.py
```

L'executable es generarà a la carpeta `dist/`.

Sinó pots descarregar la versió 1.0 des d'aquí:

[⬇️ Descarrega Buscamines v1.0](https://github.com/xbaubes/Buscamines/releases/download/v1.0/Buscamines.exe)

## 🕹️ Funcionalitats

- Tauler configurable (files, columnes, mines)
- Control de temps i classificació TOP 10
- Disseny gràfic personalitzat amb emojis
- Marcatge amb clic dret
- Revelació automàtica de caselles
- Guardat i visualització de puntuacions amb nom, temps i data/hora

## ⏱️ API de puntuacions

Aquest projecte utilitza una API proporcionada per [SheetDB](https://sheetdb.io) per desar i obtenir els millors temps:

```python
url = "https://sheetdb.io/api/v1/77zmp0nhr00bh"
```

## 📸 Captura

![Captura del joc](GUI.png)

## 🚧 TODO

🛠️ Estructura i codi

- **Separació MVC**: Actualment la lògica i la GUI estan entrellaçades. Reorganització modular separant clarament models, views, controllers. Això permetria reutilitzar la lògica per fer una versió web amb Flask

## 📝 Llicència

Aquest projecte està disponible sota la llicència MIT: lliure d'ús, còpia i modificació amb crèdit a l'autor.
