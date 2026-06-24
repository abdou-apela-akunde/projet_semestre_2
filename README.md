# DataSante - SAE 2.01

Application web Flask de consultation et de visualisation de donnees de sante en France. Le projet exploite les tables de reference de la SAE 2.04 et les jeux de donnees ouverts de Data Ameli.

## Objectif

L'application permet de choisir une profession, une periode et un territoire pour explorer des effectifs, des densites, des honoraires, des prescriptions et des donnees de pathologies. Les resultats sont presentes sous forme de KPI, tableaux exportables, graphiques et carte interactive.

## Fonctionnalites

- Filtres par profession, region, departement et annee.
- Carte Leaflet de la France : regions et departements sont selectionnables.
- Synchronisation dans les deux sens entre la carte et les filtres.
- Apercu dynamique sur l'accueil sans redirection.
- Analyses d'honoraires, prescriptions et pathologies.
- Comparaison de deux professions ou territoires avec evolution, sexe et tranche d'age.
- Tableaux triables et exportables en CSV.
- Mise en cache en memoire des appels Data Ameli.
- Pages Indicateurs et A propos.

## Technologies

| Categorie | Technologies |
| --- | --- |
| Back-end | Python, Flask, SQLAlchemy |
| Base de donnees | MySQL SAE 2.04 ou SQLite locale |
| Front-end | HTML5, CSS3, JavaScript |
| Visualisation | Chart.js et Leaflet |
| Donnees | API Data Ameli et fichiers GeoJSON |
| Tests | pytest |

## Architecture

Le projet suit une organisation MVC adaptee a Flask :

- `controllers/` gere les routes HTML et JSON.
- `models/` definit les tables de dimensions et la connexion a la base.
- `services/` regroupe les appels a Data Ameli, le cache et les calculs.
- `templates/` contient les vues Jinja2.
- `static/` contient les ressources executees ou affichees dans le navigateur.

## Pages disponibles

| URL | Role |
| --- | --- |
| `/` | Accueil, filtres, carte et previsualisation |
| `/honoraires` | Analyse des honoraires |
| `/prescriptions` | Analyse des prescriptions |
| `/pathologies` | Analyse des pathologies |
| `/indicateurs` | Indicateurs de reference |
| `/comparaisons` | Comparaison de deux series |
| `/a-propos` | Presentation du projet et de ses sources |

## API interne

Les pages utilisent les endpoints JSON suivants :

| Endpoint | Role |
| --- | --- |
| `/api/departements/<region_id>` | Charge les departements d'une region |
| `/api/preview/effectifs` | Retourne les KPI et l'evolution de l'accueil |
| `/api/analyses/honoraires` | Retourne les donnees d'honoraires |
| `/api/analyses/prescriptions` | Retourne les donnees de prescriptions |
| `/api/analyses/pathologies` | Retourne les donnees de pathologies |
| `/api/comparaison/series` | Retourne deux series et leurs repartitions |

## Installation locale

### Prerequis

- Python 3.10 ou plus recent
- `pip`
- Une connexion Internet pour interroger Data Ameli

### Demarrage

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Ouvrir ensuite [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Configuration

Les variables peuvent etre placees dans un fichier `.env` a la racine du projet.

```env
FLASK_ENV=development
SECRET_KEY=une-cle-secrete-a-modifier

# Configuration MySQL facultative
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_NAME=sae204
```

Si les quatre variables MySQL ne sont pas renseignees, l'application initialise automatiquement une base SQLite a partir de `data/sae204_ideal.sql`.

## Donnees et sources

- **SAE 2.04** : referentiels de regions, departements, professions, ages, sexes et categories d'analyse.
- **Data Ameli** : effectifs et densites des professionnels de sante, honoraires, prescriptions et pathologies.
- **GeoJSON France** : contours des regions et departements, utilises par Leaflet.

Les appels externes sont centralises dans `services/ameli_api.py`. En cas d'indisponibilite de l'API, l'interface affiche un etat sans resultat plutot qu'une erreur bloquante.

## Tests et verification

Lancer les tests automatises :

```powershell
python -m pytest
```

Verifier egalement la syntaxe des scripts front-end :

```powershell
node --check static/js/map.js
node --check static/js/preview.js
```

## Deploiement

`wsgi.py` expose la variable `application` attendue par un serveur WSGI, notamment Alwaysdata. En production, definissez les variables MySQL et une `SECRET_KEY` forte dans les variables d'environnement de l'hebergeur.

## Structure de l'application

```text
S201 - APP/
|-- app.py                         # Creation de Flask et enregistrement des blueprints
|-- config.py                      # Configuration de l'application
|-- wsgi.py                        # Entree WSGI pour le deploiement
|-- requirements.txt               # Dependances Python
|-- .env                           # Variables locales non versionnees
|
|-- controllers/                   # Routes HTML et API JSON
|   |-- accueil.py                 # Accueil et donnees de la carte
|   |-- api.py                     # Endpoints AJAX
|   `-- dashboard.py               # Pages d'analyse
|
|-- models/                        # Modeles SQLAlchemy
|   |-- db.py                      # Connexion et initialisation SQLite
|   `-- dimensions.py              # Tables de dimensions
|
|-- services/                      # Logique metier
|   |-- ameli_api.py               # Client Data Ameli
|   |-- analytics.py               # Calculs d'evolution
|   `-- cache.py                   # Cache en memoire
|
|-- templates/                     # Pages Jinja2
|   |-- base.html                  # Structure commune
|   |-- accueil.html               # Filtres, carte et apercu
|   |-- honoraires.html            # Analyse des honoraires
|   |-- prescriptions.html         # Analyse des prescriptions
|   |-- pathologies.html           # Analyse des pathologies
|   |-- indicateurs.html           # KPI
|   |-- comparaisons.html          # Comparaison
|   |-- a_propos.html              # Presentation du projet
|   `-- erreur.html                # Erreurs 404 et 500
|
|-- static/
|   |-- css/style.css              # Styles et responsive design
|   |-- js/                        # Interactions et graphiques
|   |-- data/                      # GeoJSON des regions et departements
|   `-- img/                       # Logo UPEC
|
|-- data/                          # SQL source et base SQLite locale
|-- docs/                          # Tutoriels et consignes de la SAE
`-- scripts/                       # Outils techniques
```

## Documentation

Les tutoriels et consignes fournis pour la SAE sont conserves dans `docs/`. Le code Python contient des docstrings courtes et le JavaScript utilise des commentaires de contexte afin de faciliter la reprise du projet.

## Bonnes pratiques Git

Ne pas versionner les fichiers generes ou sensibles : `.env`, `venv/`, `__pycache__/`, `.pytest_cache/` et `data/sae201_local.db`.
