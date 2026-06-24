# SAE201 - Présentation

Source : `SAE201_presentation.pdf`

## Contenu extrait

## Page 1

SAE 2.01
BUT Informatique
3 TutorielsMVCOpen DataDéveloppement
d’une application web
Flask Jinja2 CSS Chart.js
Partir de la base de données de la SAE2.04
et construire une application web complète.
## Page 2

Vue d'ensemble du projet
Ce projet prend la suite de SAE2.04 —la base MySQL et les scripts Python sont réutilisés tels quels
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
1 Tutoriel #1
Application
Flask MVC
Architecture MVC · Blueprints
Jinja2 · CSS
2 Tutoriel #2
Formulaires &
Visualisations
Cascade AJAX · Routes JSON
Chart.js · Comparaison · CSV
3 Tutoriel #3 (optionnel)
Déploiement
Alwaysdata
Compte mutualisé · sous-dossier
FileZilla · venv · WSGI
Point de départ: base MySQL SAE2.04 (9 tables de dimensions) —réutilisée telle quelle dans l'application
## Page 3

Stack technique du projet
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
Flask 3
Framework web Python
routes, Blueprints
Jinja2
Moteur de templates
héritage, filtres, boucles
CSS simple
Feuille de style
mise en forme du projet
Chart.js
Graphiques interactifs
courbe, camembert, multi
SQLAlchemy
ORM réutilisé
depuis SAE2.04
Alwaysdata
Compte mutualisé
sous-dossier équipe
## Page 4

1
Application web Flask
Architecture MVC
Blueprints  ·  Jinja2  ·  Templates  ·  Routes
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
## Page 5

Tutoriel #1  —Architecture MVC
SAE2.01 –IUT de Créteil -Vitry –Département InformatiqueM Modèle
Accès aux données
SQLAlchemy ORM
```text
models/
```

db.py
dimensions.pyV Vue
HTML + Jinja2
Feuille de style
```text
templates/
```

base.html
accueil.html
effectifs.htmlC Contrôleur
Logique Flask
Blueprints · routes
```text
controllers/
```

accueil.py
effectifs.py
api.py
`app.py  —Flask(__name__)  ·  register_blueprint()  ·  app.run(debug=True)`
## Page 6

Tutoriel #1  —Structure du projet et Blueprints
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
Arborescence du projet
```text
SAE201-code/
```

`├── app.py`
`├── config.py`
`├── wsgi.py`
`├── models/`
│   ├── db.py
│   └── dimensions.py
├── services/
│   └── ameli_api.py
`├── controllers/`
│   ├── accueil.py
│   └── effectifs.py
`└── templates/`
├── base.html
├── accueil.html
└── effectifs.html
Qu'est -ce qu'un Blueprint -
Un Blueprint est un groupe de routes thématiques.
Il permet de découper l'application en modules
indépendants, conformément à l'architecture MVC.
bp_accueil
/Page d'accueil · formulaire
bp_effectifs
/effectifsRésultats · tableau · graphique
bp_api
/api/*Routes JSON pour Chart.js
## Page 7

Tutoriel #1  —Templates Jinja2 et héritage
SAE2.01 –IUT de Créteil -Vitry –Département Informatiquebase.html  (parent)
<header><nav>…</nav></header>
{% block content %}{% endblock %}
{% block scripts %}{% endblock %}
accueil.html
{% extends 'base.html' %}
{% block content %}
<form method='GET'>
<select> regions </select>
<select> depts </select>
{% endblock %}
effectifs.html
{% extends 'base.html' %}
{% block content %}
<table>…</table>
<canvas id='chart'>
{% endblock %}
{% block scripts %}…{% endblock %}
comparaison.html
{% extends 'base.html' %}
{% block content %}
2 sélecteurs
<canvas id='chartComparaison'>
{% endblock %}
{% block scripts %}…{% endblock %}
## Page 8

2
Formulaires avancés
et visualisations
Cascade AJAX  ·  Routes JSON  ·  Chart.js  ·  Gestion d'erreurs
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
## Page 9

Tutoriel #2  —Cascade région →département (AJAX)
SAE2.01 –IUT de Créteil -Vitry –Département InformatiqueUtilisateur
choisit
une région→JavaScript
detecte le
changement→fetch()
/api/departements
/<id>→Flask retourne
JSON (liste
des depts)
JavaScript met à jour
<select id='departement'>
sans recharger la page ✓↑
Flask —views/api.py
@bp_api.route('/departements/<int:region_id>')
def departements(region_id):
region = session.query(Region).get(region_id)
return jsonify([{'id':d.id,'libelle':d.libelle}
for d in region.departements])
JavaScript —accueil.html
async function chargerDepts(regionId) {
const resp  = await
fetch(`/api/departements/${regionId}`);
const depts = await resp.json();
select.innerHTML = depts.map(d => `<option
value="${d.id}">${d.libelle}</option>`).join('');
}
## Page 10

Tutoriel #2  —Visualisations avec Chart.js
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
Courbe
Évolution des effectifs
sur toutes les années
Options clés:
type: 'line'
fill: true
tension: 0.3
spanGaps: true
Camembert
Répartition des honoraires
par catégorie
Options clés:
type: 'doughnut'
callback: montant M€
position: 'bottom'
Multi -séries
2 territoires superposés
(plein vs tiretés)
Options clés:
datasets: [A, B]
borderDash: [5,5]
Promise.all() parallèle
Les données sont chargées via fetch() depuis les routes JSON —plus propre que d'injecter du JSON dans le HTML via Jinja2
## Page 11

Tutoriel #2  —Comparaison et export CSV
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
Comparer deux territoires
Territoire A
Région ▾
Département ▾Territoire B
Région ▾
Département ▾
← Promise.all(): 2 appels API en parallèle
Export CSV
# views/exports.py
import csv, io
@bp.route('/export/csv')
def export_csv():
data = get_effectifs(...)
output = io.StringIO()
writer = csv.writer(output)
writer.writerow(['Année','Effectif',...])
for row in data:
writer.writerow([...])
return Response(
output.getvalue(),
mimetype='text/csv',
headers={'Content -Disposition':
'attachment; filename=...'}
)
Le navigateur déclenche
automatiquement le téléchargement.
## Page 12

3
Déploiement (optionnel)
sur Alwaysdata
Compte mutualisé  ·  Sous -dossier d'équipe  ·  FileZilla  ·  venv  ·  WSGI
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
## Page 13

Tutoriel #3  —Compte mutualisé
sae204.alwaysdata.net
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
1Accès fourni par l'enseignant
Identifiants du compte mutualisé
Panneau Alwaysdata · SFTP · SSH
3Créer le sous-dossier d'équipe
FileZilla → /www/sae201_XX
Dossier racine du futur site
2Installer FileZilla
filezilla-project.org · Client SFTP
Protocole SFTP · port 22
4Préparer l'application
`requirements.txt · wsgi.py`
`Exclure.env, venv/, __pycache__`
Base MySQL: même que SAE2.04 (mysql-sae204.alwaysdata.net · sae204_XX_bd · aucune migration)
## Page 14

Tutoriel #3  —venv, FileZilla et configuration WSGI
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
1venv
(SSH)
```text
python3 -m venv venv
```

source
venv/bin/activate
```text
pip install -r
```

`requirements.txt`
2FileZilla
(SFTP)
## 1. Connexion SFTP à

ssh-
sae204.alwaysdata.net
## 2. Naviguer vers

/www/sae201_XX
## 3. Glisser -déposer les

fichiers
3WSGI
`wsgi.py`
from app import app
# variable «
application »
# attendue par
Alwaysdata
application = app
4Config
site
Chemin app:
~/www/sae201_XX
`Fichier WSGI: wsgi.py`
Interpréteur:
~/www/.../venv/bin/pyt
hon3
Ordre: FileZilla →SSH + venv →Variables d'env →Créer le site WSGI →Redémarrer
## Page 15

Tutoriel #3 —Variables d'environnement et erreurs
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
Variables d'environnement (par site, dans Web →
Sites)
```text
FLASK_ENV   = production
DB_USER     = sae204_XX_user
DB_PASSWORD = ••••••••••••••••
DB_HOST     = mysql-sae204.alwaysdata.net
DB_NAME     = sae204_XX_bd
SECRET_KEY  = <secrets.token_hex(32)>
```

Erreurs courantes
500 Internal Error Traceback dans les logs SSH
`ModuleNotFoundError pip install -r requirements.txt`
OperationalError Vérifier DB_HOST/DB_PASSWORD
`Page blanche wsgi.py: variable = application`
Consulter les logs:
tail -f ~/admin/logs/apache/error.logMise à jour:
FileZilla: modifier fichier  →  Panneau → Sites → Redémarrer
## Page 16

Architecture complète —du serveur au navigateur
MySQL
Alwaysdata
9 tables
dimensions→
Flask
SQLAlchemy
ORM · Blueprints
Templates→
API
ameli.fr
Effectifs · Honoraires
Prescriptions, …→
Navigateur
Bootstrap
Chart.js
Fetch · AJAXORM requests() fetch()
3
tutoriels
9
tables réutilisées
5
types de routes
4
types de graphiques
SAE2.01 –IUT de Créteil -Vitry –Département Informatique
## Page 17

## Bilan —Ce que vous aurez appris

SAE2.01 –IUT de Créteil -Vitry –Département Informatique
Architecture MVC
• Blueprints Flask
• Séparation M / V / C
• Templates Jinja2 hérités
Front -end moderne
• CSS simple
• fetch() + async/await
• Cascade AJAX sans rechargement
Visualisations
• Chart.js courbe + camembert
• Routes JSON Flask
• Graphique multi -séries
API & données
• Pattern Route HTML vs JSON
• Promise.all() parallèle
• Export CSV (io.StringIO)
Déploiement
• Compte mutualisé Alwaysdata
• Sous -dossier d'équipe
• FileZilla + venv + WSGI
Bonnes pratiques
• Dev vs Production config
• SECRET_KEY robuste
• Lecture des logs SSH
## Audit du projet - 2026-06-21

- [x] Stack principale pr?sente : Flask, Jinja2, CSS, Chart.js, SQLAlchemy, requests.
- [x] Architecture MVC et Blueprints pr?sents : `bp_accueil`, `bp_api`, `bp_effectifs`, `bp_dashboard`, `bp_exports`.
- [x] Templates Jinja2 h?ritent de `base.html`.
- [x] Cascade AJAX r?gion vers d?partement impl?ment?e.
- [x] Routes JSON disponibles pour d?partements, pr?visualisation, ?volution et comparaison.
- [x] Graphiques Chart.js pr?sents : courbe effectifs, densit?, barres/comparaison et visualisations de dashboard.
- [x] Comparaison de deux territoires impl?ment?e via `/comparaisons` et `/api/comparaison/effectifs`.
- [x] Export CSV impl?ment? via `controllers/exports.py`.
- [x] D?ploiement pr?par? : `wsgi.py`, `.env.example`, `requirements.txt`, variables MySQL, compatibilit? `SCRIPT_NAME=/sae201_b6`.
- [x] Cache et bonne pratique `SECRET_KEY` robuste pr?sents.
- [ ] D?ploiement Alwaysdata r?el non confirm?.
- [ ] Lecture des logs SSH/Alwaysdata non v?rifi?e.
