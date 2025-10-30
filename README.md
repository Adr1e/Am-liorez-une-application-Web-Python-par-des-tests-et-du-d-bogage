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



# 1. Activer l'environnement virtuel
source .venv/bin/activate

# 2. Vérifier l'installation des dépendances
pip install -r requirements.txt

# 3. Lancer l'application Flask
export FLASK_APP=server.py FLASK_DEBUG=0
flask run
# (Laisser ce terminal ouvert, l'application tourne sur http://127.0.0.1:5000)

# 4. Ouvrir un nouveau terminal pour tester les routes principales
curl -i http://127.0.0.1:5000/
curl -s http://127.0.0.1:5000/points | python -m json.tool

# 5. Lancer tous les tests unitaires et d'intégration
pytest -v

# 6. Vérifier la couverture du code
coverage run -m pytest
coverage report -m

# 7. (Optionnel) Générer le rapport HTML de la couverture
coverage html
open htmlcov/index.html

# 8. Lancer les tests de performance avec Locust (interface web)
locust -H http://127.0.0.1:5000
# Ouvrir http://localhost:8089
# Configurer : 6 utilisateurs, spawn rate = 1, durée ~2 minutes

# 9. Vérifier les résultats de performance
à faire
# 10. Nettoyer les fichiers temporaires et caches (fin de démo)
à faire
