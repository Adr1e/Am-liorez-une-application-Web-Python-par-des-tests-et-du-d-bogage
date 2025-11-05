# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called 
    [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.


# Améliorez une application Web Python par des tests et du débogage

## 1. Description du projet

Ce projet vise à fiabiliser une application web Flask en appliquant les bonnes pratiques de tests et de débogage.  
L’application **Güdlft Registration** permet à des clubs de réserver des places pour des compétitions sportives.  

L’objectif est de garantir un code stable, maintenable et testé, conformément aux exigences du parcours OpenClassrooms « Développeur Python ».

---

## 2. Objectifs techniques

- Mise en place d’une stratégie de tests complète (unitaires et intégration).  
- Application des principes TDD (Test Driven Development).  
- Détection et correction des bugs existants.  
- Suivi de la couverture de code via `pytest-cov`.  
- Analyse de performance avec **Locust**.  

---

## 3. Installation

### Prérequis

- Python ≥ 3.10  
- Flask ≥ 3.x  
- Pytest ≥ 8.x  

### Étapes d’installation

```bash
git clone https://github.com/Adr1e/Am-liorez-une-application-Web-Python-par-des-tests-et-du-d-bogage.git
cd Am-liorez-une-application-Web-Python-par-des-tests-et-du-d-bogage
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

---

## 4. Lancer l’application

```bash
python server.py
```

Application disponible sur :  
http://localhost:5000

---

## 5. Lancer les tests

### Tous les tests
```bash
pytest -v
```

### Couverture
```bash
pytest --cov=server --cov-report=term-missing
```

### Rapport HTML
```bash
pytest --cov=server --cov-report=html
```

Ouvrir ensuite `htmlcov/index.html` dans un navigateur.

---

## 6. Résultats

- **Nombre total de tests :** 30  
- **Taux de réussite :** 100 %  
- **Couverture globale :** 97 %  
- **Ratio unitaires/intégration :** conforme (2:1)  
- **Application :** stable et conforme aux spécifications.

Les rapports complets sont disponibles ici :
- [Rapport de tests](./TEST_REPORT.md)
- [Rapport de performance](./PERF_REPORT.md)

---

## 7. Structure du projet

```
.
├── server.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── .coveragerc
├── pytest.ini
├── TEST_REPORT.md
├── PERF_REPORT.md
└── README.md
```

---

## 8. Auteur

Projet réalisé par **Adrien Fischer**  
Formation : *OpenClassrooms – Développeur Python*  
Projet : *Améliorez une application Web Python par des tests et du débogage*
