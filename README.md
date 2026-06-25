# DataSanté - SAE 2.01

DataSanté est une application web Flask réalisée dans le cadre de la SAE 2.01. Elle permet de consulter, visualiser et comparer des données de santé françaises à partir des référentiels construits en SAE 2.04 et de l'API publique Data Ameli.

## Contexte

Le projet répond aux trois tutoriels de la SAE 2.01 :

- tutoriel 1 : créer une application Flask structurée selon une architecture MVC et connectée à la base SAE 2.04 ;
- tutoriel 2 : ajouter des formulaires dynamiques, interroger l'API Data Ameli, afficher un tableau et un graphique ;
- tutoriel 3 : préparer le projet pour le déploiement avec `requirements.txt`, `wsgi.py`, des variables d'environnement et des URLs générées avec `url_for`.

## Objectifs

- Fournir une interface claire pour explorer les effectifs, densités, prescriptions, honoraires et pathologies.
- Filtrer les résultats par profession, région, département et année ou plage d'années.
- Afficher les résultats sous forme de KPI, tableaux triables, exports CSV, graphiques et carte interactive.
- Garder une structure de projet propre, maintenable et compatible avec un déploiement Alwaysdata.

## Membres du groupe

- ALLOUNE Abdelwadoud
- APELA AKUNDE Abdou
- BERRICHE Djibril
- WASEL Yassine

## Répartition du travail

| Membre | Travail principal |
| --- | --- |
| ALLOUNE Abdelwadoud | Accueil, carte interactive, intégration visuelle |
| APELA AKUNDE Abdou | Base de données, modèles SQLAlchemy, configuration |
| BERRICHE Djibril | API Data Ameli, pages prescriptions/honoraires/pathologies |
| WASEL Yassine | Comparaisons, graphiques, README et préparation de soutenance |

## Technologies utilisées

| Catégorie | Technologies |
| --- | --- |
| Back-end | Python, Flask, Jinja2, Blueprints |
| Base de données | SQLAlchemy, MySQL SAE 2.04, SQLite local de secours |
| API | Data Ameli, `requests` |
| Front-end | HTML5, CSS3, JavaScript |
| Visualisation | Chart.js, Leaflet, GeoJSON |
| Déploiement | Alwaysdata, WSGI, FileZilla/SFTP |
| Tests et vérification | `pytest`, `compileall`, `node --check` |

## Structure du projet

```text
S201 - APP/
|-- app.py                         # Création de Flask et blueprints
|-- config.py                      # Configuration et variables d'environnement
|-- wsgi.py                        # Entrée WSGI pour Alwaysdata
|-- requirements.txt               # Dépendances Python
|-- .env                           # Configuration locale non versionnée
|
|-- controllers/                   # Routes HTML et endpoints JSON
|   |-- accueil.py                 # Accueil, filtres, carte
|   |-- api.py                     # API interne utilisée par le front-end
|   `-- dashboard.py               # Pages d'analyse
|
|-- models/                        # Modèles SQLAlchemy
|   |-- db.py                      # Connexion et initialisation SQLite
|   `-- dimensions.py              # Tables de dimensions SAE 2.04
|
|-- services/                      # Logique métier
|   |-- ameli_api.py               # Client Data Ameli
|   |-- analytics.py               # Calculs d'évolution
|   `-- cache.py                   # Cache mémoire
|
|-- templates/                     # Vues Jinja2
|-- static/                        # CSS, JavaScript, GeoJSON, images
|-- data/                          # SQL source SAE 2.04
|-- docs/                          # Tutoriels, annexes, soutenance
`-- scripts/                       # Scripts techniques
```

## Installation locale

Prérequis :

- Python 3.10 ou supérieur ;
- `pip` ;
- une connexion Internet pour les appels Data Ameli.

Commandes :

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Ouvrir ensuite [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Configuration

Le projet doit être lancé avec un fichier `.env` placé à la racine. Ce fichier contient les vrais identifiants de la base SAE 2.04 et ne doit jamais être versionné sur GitHub.

Pour ce projet, le `.env` local doit contenir :

```env
DB_USER=sae204_b6_user
DB_PASSWORD=<mot_de_passe_fourni_par_l_enseignant>
DB_HOST=mysql-sae204.alwaysdata.net
DB_NAME=sae204_b6_bd
FLASK_ENV=development
SECRET_KEY=<chaine_longue_et_unique>
```

Le mot de passe réel est volontairement conservé uniquement dans le fichier `.env` local. Il n'est pas affiché dans le README pour respecter les consignes de sécurité du tutoriel : `.env` contient des informations sensibles et doit rester exclu du dépôt.

Au lancement, `config.py` charge automatiquement ce fichier avec `python-dotenv`. Si les quatre variables MySQL ne sont pas renseignées, l'application utilise une base SQLite locale alimentée par `data/sae204_ideal.sql`, ce qui permet de travailler même sans accès immédiat à MySQL.

## Pages du site

| Page | Fonction |
| --- | --- |
| `/` | Accueil avec critères de recherche, carte Leaflet, KPI, graphique et tableaux actualisés |
| `/indicateurs` | Synthèse des dimensions disponibles : régions, départements, professions, prescriptions |
| `/comparaisons` | Comparaison de deux séries par territoire, profession et période, avec vues sexe/âge |
| `/prescriptions` | Analyse des montants prescrits par profession, poste, territoire et période |
| `/honoraires` | Analyse des honoraires et dépassements par profession, territoire et période |
| `/pathologies` | Analyse du nombre de personnes concernées par une pathologie |
| `/a-propos` | Présentation du projet, des sources et de l'architecture |

Il n'y a pas de portail admin, d'inscription ou de connexion dans les consignes livrées : le projet est une application de consultation de données publiques.

## Base de données

La base SAE 2.04 fournit les tables de dimensions utilisées pour alimenter les formulaires :

- `region`
- `departement`
- `profession_sante`
- `sexe`
- `tranche_age`
- `type_exercice`
- `type_honoraire`
- `type_prescription`
- `type_secteur`

Les tables de faits ne sont pas stockées localement : les données chiffrées sont récupérées à la demande depuis Data Ameli. Cette approche évite de dupliquer les jeux de données publics et garde les résultats à jour.

## API et pipeline de données

Le pipeline applicatif est le suivant :

1. les référentiels sont lus dans MySQL ou SQLite avec SQLAlchemy ;
2. l'utilisateur choisit ses filtres dans les formulaires ;
3. JavaScript appelle les endpoints internes Flask ;
4. Flask interroge Data Ameli via `services/ameli_api.py` ;
5. les données sont filtrées, nettoyées, agrégées puis renvoyées en JSON ;
6. l'interface met à jour les KPI, graphiques et tableaux.

Endpoints internes principaux :

| Endpoint | Rôle |
| --- | --- |
| `/api/departements/<region_id>` | Liste les départements d'une région |
| `/api/preview/effectifs` | Alimente les vues de l'accueil |
| `/api/analyses/prescriptions` | Alimente la page prescriptions |
| `/api/analyses/honoraires` | Alimente la page honoraires |
| `/api/analyses/pathologies` | Alimente la page pathologies |
| `/api/comparaison/series` | Alimente la page comparaisons |

## Fonctionnalités principales

- filtres par profession, région, département, année et plage d'années ;
- sélection possible d'une région entière grâce à l'agrégat régional Data Ameli ;
- carte interactive synchronisée avec les formulaires ;
- graphiques Chart.js avec titres, légendes et axes lisibles ;
- tableaux triables par colonne ;
- téléchargement CSV des tableaux ;
- cache mémoire pour limiter les appels répétitifs à Data Ameli ;
- pages d'erreur 404 et 500 claires ;
- structure compatible avec un sous-dossier Alwaysdata grâce à `url_for`.

## Démonstration

Pour présenter l'application :

1. lancer `python app.py` ;
2. ouvrir `http://127.0.0.1:5000` ;
3. sur l'accueil, sélectionner une profession, une région entière ou un département, puis une année ;
4. montrer la carte, les KPI, le graphique d'évolution et les tableaux exportables ;
5. ouvrir `Indicateurs`, puis `Comparaisons` pour comparer deux séries ;
6. ouvrir `Prescriptions`, `Honoraires` et `Pathologies` pour montrer les analyses par période ;
7. télécharger un CSV depuis un tableau.

## Vérifications

Commandes utiles :

```powershell
python -m compileall app.py config.py controllers models services wsgi.py
python -m pytest
node --check static/js/map.js
node --check static/js/preview.js
node --check static/js/analysis.js
node --check static/js/comparaisons.js
```

## Déploiement

Le fichier `wsgi.py` expose `application`, attendu par Alwaysdata.

Variables de production à définir côté site Alwaysdata :

```env
DB_USER=sae204_b6_user
DB_PASSWORD=<mot_de_passe_fourni_par_l_enseignant>
DB_HOST=mysql-sae204.alwaysdata.net
DB_NAME=sae204_b6_bd
FLASK_ENV=production
SECRET_KEY=<chaine_longue_et_unique>
```

Le site attendu pour l'équipe b6 est :

```text
https://sae204.alwaysdata.net/sae201_b6/
```

## Limites éventuelles

- L'application dépend de la disponibilité de l'API Data Ameli.
- Certaines combinaisons profession/territoire/période peuvent ne pas renvoyer de données.
- Le déploiement Alwaysdata et le transfert SFTP doivent être vérifiés depuis le compte serveur.
- Les données de faits ne sont pas historisées localement, elles sont consultées à la demande.

## Conformité avec les tutoriels

| Consigne | Statut | Détail |
| --- | --- | --- |
| Tutoriel 1 : projet Flask MVC | Conforme | `models/`, `controllers/`, `templates/`, `static/`, blueprints et page d'accueil présents |
| Tutoriel 1 : connexion base SAE 2.04 | Conforme | MySQL via `.env`, SQLite de secours depuis `sae204_ideal.sql` |
| Tutoriel 1 : listes régions/professions | Conforme | Les listes sont chargées depuis la base et triées |
| Tutoriel 2 : formulaires dynamiques | Conforme | Régions, départements, professions, années et plages d'années |
| Tutoriel 2 : API Data Ameli | Conforme | Service centralisé dans `services/ameli_api.py` |
| Tutoriel 2 : tableau et graphique | Conforme | Présents sur accueil, comparaisons, prescriptions, honoraires et pathologies |
| Tutoriel 3 : `requirements.txt` | Conforme | Dépendances listées |
| Tutoriel 3 : `wsgi.py` | Conforme | Variable `application` exposée |
| Tutoriel 3 : pas d'URL statique en dur | Conforme | Templates et scripts utilisent `url_for` ou des URLs passées en `data-*` |
| Tutoriel 3 : secrets non versionnés | Conforme | `.env` ignoré par Git et valeurs sensibles gardées hors du dépôt |
