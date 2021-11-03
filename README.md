# Application web Django - Dépôt de demande/reponse de critique de livres

Ce programme à pour objet de permettre à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.
- Demande de critiques de livres ou d'articles en créant un ticket.
- Publier des critiques soit en réponse à un ticket, soit sans ticket préalable.


Structuration du site :
- Une page "flux" contenant les derniers tickets et critiques des utilisateurs qu'il suit, classés par ordre chronologique, les plus récents en premier,
- Une page "posts" où l'utilisateur retrouve l'intégralité de ses tickets et critiques,
- Une page "abonnements" où l'utilisateur peut saisir le nom d'un autre utilisateur qu'il souhaite suivre, voir ses abonnements et les gérer, et voir ses abonnés.



## Informations d'installation et d'exécution avec venv et pip


**Configurations et exécution du programme**
Installation :
- Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/C22660/LITReview.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/C22660/LITReview/archive/refs/heads/master.zip))
- Rendez-vous depuis un terminal à la racine du répertoire ocmovies-api-fr avec la commande `$ cd LITReview`
- Créer un environnement virtuel pour le projet avec `$ python -m venv env` sous windows ou `$ python3 -m venv env` sous macos ou linux.
- Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
- Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`

Une fois cette installation effectuée :
- Appliquer les migrations dans la base de données :
depuis le terminal > `$ python manage.py migrate`

- Création du superuser (utilisateur avec droits d'administration) :
depuis le terminal > `$ python manage.py createsuperuser`
entrer le nom d'utilisateur (Username), Email, et mot de passe (invisible lors de la frappe dans le terminal)

- Lancement du serveur :
depuis le terminal > `$ python manage.py runserver`

- Accès à la page d'administration :
Dans la barre d'adresse, ajouter /administration-application
(127.0.0.1:8000/administration-application)
L'interface d'administration apparaît

- L'accès à la page d'accueil (page de connexion/inscription) directement depuis 127.0.0.1:8000

## Techologies
Python 3.9
Package ajouté : Django 3.1.6, Pillow 8.3.2

## Auteur
Cédric M
