# backend-course

Cours de développement backend via Python et [FastAPI](https://fastapi.tiangolo.com/).

## Sommaire

1. [Préparer son environnement de développement](#préparer-son-environnement-de-développement)
2. [Consignes du projet](#consignes-du-projet)


## Préparer son environnement de développement

> Testé avec Python 3.10 et FastAPI 0.115

- [Installer Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- [Créer un fork du projet](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#forking-a-repository)
- Ouvrir le projet dans votre éditeur préféré.
- [Créer un environnement virtuel Python](https://docs.python.org/3/tutorial/venv.html)
    ```bash
    # Exemple via bash
    cd <chemin/vers/dossier/du/projet/>

    # Le dossier contenant l'environnement virtuel sera nommé "env"
    python3 -m venv env

    # On active l'environnement virtuel
    
    ## Windows
    env\Scripts\activate
    
    ## GNU/Linux
    . env/bin/activate
    ```
- [(OPTIONNEL) VSCode - Définir l'environnement d'exécution](https://code.visualstudio.com/docs/python/environments#_working-with-python-interpreters)
- Installer les [dépendances du projet](requirements.txt)
    > Ces dépendances doivent être renseignées au fur et à mesure dans le fichier requirements.txt.
    ```bash
    python3 -m pip install -r requirements.txt
    ```
- Valider le fonctionnement via le fichier test [checkenv.py](src/tests/checkenv.py).
    ```bash
    python3 -m fastapi dev src/tests/checkenv.py
    #  FastAPI   Starting development server 🚀
    #  ...
    #  server   Server started at http://127.0.0.1:8000
    #  ...
    ```
