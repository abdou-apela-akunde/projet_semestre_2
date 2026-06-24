# Tutoriel #2 - Formulaire, API ameli.fr et visualisations

Source : `SAE201-Tutoriel2-FormulairesAPI.pdf`

## Suivi

- [x] Tutoriel lu
- [x] Prérequis vérifiés
- [x] Toutes les étapes réalisées
- [x] Résultat final testé

## Consignes détaillées

Formulaire, API ameli.fr et visualisations

Sélection dynamique, appel à l'API, tableau de résultats, premier graphique.

Ce tutoriel transforme l'application en un outil interactif : l'utilisateur choisit une profession, un
territoire et une année, puis obtient en retour les données chiffrées issues de l'API data.ameli.fr,
présentées sous forme de tableau et de graphique.
Prérequis
Avoir terminé le tutoriel #1 : application Flask qui se connecte à la base et affiche les régions
et professions sur la page d'accueil.

SAE2.01 – Tutoriel #2

SAE2.01 – Tutoriel #2
### 1.1 Ce qu'on va construire

- [x] Réaliser : Ce qu'on va construire

Un formulaire à quatre champs :
• profession (liste déroulante remplie depuis la base),
• région (liste déroulante remplie depuis la base),
• département (liste déroulante mise à jour dynamiquement selon la région choisie),
• année (liste des années disponibles, par exemple 2015 à 2023).
La soumission du formulaire redirige vers une page /effectifs qui affiche les résultats.
### 1.2 Mise à jour du template accueil.html

- [x] Réaliser : Mise à jour du template accueil.html

### `templates/accueil.html`

```html
{% extends "base.html" %}

{% block titre %}Accueil{% endblock %}

{% block contenu %}
  <h2>Consulter les effectifs</h2>
  <form action="{{ url_for('effectifs.afficher') }}" method="get">

    <label for="profession">Profession</label>
    <select name="profession_id" id="profession" required>
      <option value=""> -- Choisir --</option>
      {% for p in professions %}
        <option value="{{ p.id }}">{{ p.libelle }}</option>
      {% endfor %}
    </select>

    <label for="region">Région</label>
    <select name="region_id" id="region" required>
      <option value=""> -- Choisir --</option>
      {% for r in regions %}
        <option value="{{ r.id }}">{{ r.libelle }}</option>
      {% endfor %}
    </select>

    <label for="departement">Département</label>
    <select name="departement_id" id="departement" required>
      <option value=""> -- Choisir une région --</option>
    </select>

    <label for="annee">Année</label>
    <select name="annee" id="annee" required>
      {% for a in range(2023, 2014, -1) %}
        <option value="{{ a }}">{{ a }}</option>
      {% endfor %}
    </select>

    <button type="submit">Afficher les effectifs</button>
  </form>

  <script src="{{ url_for('static', filename='js/cascade.js') }}"></script>
{% endblock %}
SAE2.01 – Tutoriel #2
2.1 Le problème
Si on chargeait tous les départements dès la page d'accueil, la liste serait immense et peu
pertinente. La bonne approche consiste à ne charger que les départements de la région choisie,
au moment où l'utilisateur la sélectionne. C'est le rôle d'un appel AJAX.
2.2 Route JSON côté serveur
Créer un contrôleur dédié aux routes JSON (celles qui ne rendent pas une page HTML, mais des
données pour JavaScript) :
controllers/api.py
from flask import Blueprint, jsonify
from models.db import Session
from models.dimensions import Departement

bp_api = Blueprint("api", __name__, url_prefix="/api")

@bp_api.route("/departements/<int:region_id>")
def departements(region_id):
    """Retourne les départements d'une région au format JSON."""
    session = Session()
    try:
        depts = (session.query(Departement)
                        .filter_by(region_id=region_id)
                        .order_by(Departement.code).all())
        return jsonify([
            {"id": d.id, "code": d.code, "libelle": d.libelle}
            for d in depts
        ])
    finally:
        session.close()
```

Ne pas oublier d'enregistrer le blueprint dans app.py :
from controllers.api import bp_api
app.register_blueprint(bp_api)
SAE2.01 – Tutoriel #2
Créer le fichier static/js/cascade.js qui écoute le changement de région et met à jour la liste des
départements :
### `static/js/cascade.js`

```javascript
document.getElementById("region").addEventListener("change", async (e) => {
  const regionId = e.target.value;
  const selectDept = document.getElementById("departement");

  // Vider la liste
  selectDept.innerHTML = '<option value=""> -- Choisir --</option>';

  if (!regionId) return;

  // Appel AJAX
  const response = await fetch(`/api/departements/${regionId}`);
  const depts = await response.json();

  // Remplir la liste
  for (const dept of depts) {
    const opt = document.createElement("option");
    opt.value = dept.id;
    opt.textContent = `${dept.code} – ${dept.libelle}`;
    selectDept.appendChild(opt);
  }
});
Vérification
Recharger la page d'accueil, choisir une région : la liste des départements doit se remplir
automatiquement. Les outils développeur du navigateur (F12) affichent la requête vers
/api/departements/X dans l'onglet Réseau.

SAE2.01 – Tutoriel #2
3.1 Pourquoi une classe dédiée -
Plutôt que d'écrire requests.get() dans chaque contrôleur, on regroupe tous les appels à l'API
dans une seule classe : AmeliAPI. Ce service centralise les URLs, la gestion des erreurs, et pourra
être enrichi plus tard (cache, authentification…).
```

POO en action
C'est une application directe du principe d'encapsulation : l'extérieur (les contrôleurs) ne
manipule que des méthodes métier claires comme get_effectifs(). La mécanique HTTP reste
cachée à l'intérieur de la classe.

### 3.2 Création du service

- [x] Réaliser : Création du service

### `services/ameli_api.py`

```python
import requests

class AmeliAPI:
    """Service d'accès à l'API data.ameli.fr."""

    BASE_URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"

    def __init__(self, timeout=10):
        self._timeout = timeout
        self._session = requests.Session()

    def get_effectifs(self, profession, departement_code, annee):
        """Effectifs pour une profession, un département et une année.

        Retourne une liste de dictionnaires {annee, effectif, densite}.
        """
        where = (
            f"profession_sante= \"{profession} \" AND "
            f"departement= \"{departement_code} \" AND "
            f"annee={annee} AND "
            f"libelle_classe_age= \"Tout âge \" AND "
            f"libelle_sexe= \"Tout sexe \""
        )
        return self._requete(
            "demographie-effectifs-et-les-densites",
            {"select": "annee,effectif,densite", "where": where, "limit": 100},
        )

    def get_evolution_effectifs(self, profession, departement_code):
        """Effectifs sur toutes les années disponibles (pour un graphique)."""
        where = (
SAE2.01 – Tutoriel #2
            f"departement= \"{departement_code} \" AND "
            f"libelle_classe_age= \"Tout âge \" AND "
            f"libelle_sexe= \"Tout sexe \""
        )
        return self._requete(
            "demographie-effectifs-et-les-densites",
            {"select": "annee,effectif,densite", "where": where,
             "order_by": "annee", "limit": 100},
        )

    def _requete(self, dataset, params):
        """Méthode privée : effectue une requête GET et gère les erreurs."""
        url = f"{self.BASE_URL}/{dataset}/records"
        try:
            resp = self._session.get(url, params=params, timeout=self._timeout)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.RequestException as e:
            print(f"[AmeliAPI] Erreur : {e}")
            return []
À noter : _timeout et _session sont privés
La convention Python veut que les attributs commençant par _ soient considérés comme
privés. Ils ne doivent pas être utilisés depuis l'extérieur de la classe. Cela concrétise
l'encapsulation : l'utilisateur de la classe ne manipule que l'interface publique.

SAE2.01 – Tutoriel #2
4.1 Contrôleur /effectifs
controllers/effectifs.py
from flask  import Blueprint, render_template, request
from models.db import Session
from models.dimensions import ProfessionSante, Departement
from services.ameli_api import AmeliAPI

bp_effectifs = Blueprint("effectifs", __name__)
api = AmeliAPI()

@bp_effectifs.route("/effectifs")
def afficher():
    """Affiche les effectifs pour la sélection de l'utilisateur."""
    profession_id  = request.args.get("profession_id",  type=int)
    departement_id = request.args.get("departement_id", type=int)
    annee          = request.args.get("annee",          type=int)

    session = Session()
    try:
        prof = session.get(ProfessionSante, profession_id)
        dept = session.get(Departement, departement_id)

        if not prof or not dept or not annee:
            return render_template("erreur.html",
                message="Paramètres manquants."), 400

        resultats = api.get_effectifs(prof.libelle, dept.code, annee)
        evolution = api.get_evolution_effectifs(prof.libelle, dept.code)

        return render_template("effectifs.html",
            prof=prof, dept=dept, annee=annee,
            resultats=resultats, evolution=evolution)
    finally:
        session.close()
```

Et enregistrer le blueprint dans app.py :
from controllers.effectifs import bp_effectifs
app.register_blueprint(bp_effectifs)
SAE2.01 – Tutoriel #2
### `templates/effectifs.html`

```html
{% extends "base.html" %}

{% block titre %}Effectifs{% endblock %}

{% block contenu %}
  <h2>{{ prof.libelle }} – {{ dept.code }} {{ dept.libelle }} – {{ annee  }}</h2>

  {% if resultats %}
    <table>
      <thead><tr><th>Année</th><th>Effectif</th><th>Densité</th></tr></thead>
      <tbody>
        {% for r in resultats %}
          <tr>
            <td>{{ r.annee }}</td>
            <td>{{ r.effectif }}</td>
            <td>{{ r.densite }}</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>Aucune donnée disponible pour cette sélection.</p>
  {% endif %}

  <h3>Évolution sur plusieurs années</h3>
  <canvas id="graphique"></canvas>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    const donnees = {{ evolution|tojson }};
    new Chart(document.getElementById("graphique"), {
      type: "line",
      data: {
        labels: donnees.map(d => d.annee),
        datasets: [{
          label: "Effectif",
          data: donnees.map(d => d.effectif),
          borderColor: "#2E74B5",
          tension: 0.2,
        }],
      },
    });
  </script>
{% endblock %}
```

Le filtre |tojson
Jinja2 propose des filtres, appliqués avec le caractère |. Le filtre tojson convertit une variable
Python en JSON directement utilisable par JavaScript. Très pratique pour passer des données
du serveur au client.

SAE2.01 – Tutoriel #2
### 5.1 Fonctionnement

- [x] Réaliser : Fonctionnement

Chart.js est une bibliothèque JavaScript chargée depuis un CDN (pas besoin d'installation locale).
Elle prend en entrée un élément <canvas> et un objet de configuration décrivant le type de
graphique, les données et les options.
Les types de graphiques les plus utilisés :
• line : courbe (évolution temporelle).
• bar : histogramme (comparaison).
• pie / doughnut : camembert / anneau (répartition).
• scatter : nuage de points.
### 5.2 Aller plus loin

- [x] Réaliser : Aller plus loin

La documentation officielle (https://www.chartjs.org/docs) propose de très nombreux
exemples. Quelques pistes pour enrichir :
• ajouter un second jeu de données (ex : densité) sur le même graphique,
• utiliser les options de style (couleurs, bordures, animations),
• créer un graphique en barres par département pour une même profession,
• rendre le graphique interactif (filtrer au clic).
## 6. Gestion des erreurs

- [x] Réaliser : 6. Gestion des erreurs

### 6.1 Page d'erreur

- [x] Réaliser : Page d'erreur

### `templates/erreur.html`

```html
{% extends "base.html" %}

{% block titre %}Erreur{% endblock %}

{% block contenu %}
  <h2>Oups…</h2>
  <p>{{ message }}</p>
  <p><a href="{{ url_for('accueil.index') }}">Retour à l'accueil</a></p>
{% endblock %}
6.2 Gestionnaire d'erreur global (404, 500)
Ajouter dans app.py :
@app.errorhandler(404)
def page_non_trouvee(e):
    return render_template("erreur.html",
        message="Page non trouvée."), 404

@app.errorhandler(500)
def erreur_serveur(e):
    return render_template("erreur.html",
        message="Erreur interne. Réessayez plus tard."), 500
SAE2.01 – Tutoriel #2
À ce stade, l'application est fonctionnelle. Quelques pistes pour aller plus loin :
• Étendre le service AmeliAPI aux honoraires, prescriptions, patientèle (même principe
que get_effectifs).
• Ajouter une page de comparaison entre deux départements.
• Exporter les résultats au format CSV.
• Ajouter une carte interactive avec Leaflet.
• Écrire des tests unitaires pour AmeliAPI avec pytest.
```

Bilan des deux tutoriels
Vous disposez maintenant d'une application web complète qui :
• s'appuie sur la base MySQL construite en SAE2.04 pour ses listes déroulantes,
• interroge en temps réel l'API data.ameli.fr via une classe dédiée,
• affiche les résultats sous forme de tableau x ET de graphique s interactif s,
• gère les erreurs de manière propre,
• respecte l'architecture MVC et les principes de la POO.
C'est une base solide à enrichir selon votre créativité et le niveau d'ambition de l'équipe. Bon
développement !

## Audit du projet - 2026-06-21

- [x] Prérequis tutoriel 1 vérifiés : application Flask fonctionnelle, route `/` OK, base locale avec 19 régions et 38 professions.
- [x] Le formulaire d'accueil contient les 4 champs demandés : profession, région, département et année.
- [x] Le formulaire redirige vers la route `/effectifs` via `url_for('effectifs.afficher')`.
- [x] La route JSON `/api/departements/<region_id>` existe, retourne du JSON et fournit au minimum `id`, `code` et `libelle` pour chaque département.
- [x] `static/js/cascade.js` écoute le changement de région, appelle la route AJAX et remplit la liste des départements.
- [x] `services/ameli_api.py` contient une classe `AmeliAPI`, une session `requests`, les méthodes `get_effectifs()`, `get_evolution_effectifs()` et une méthode interne de requête avec gestion d'erreur.
- [x] Appel réel à `data.ameli.fr` testé avec `Allergologues`, département `01`, année `2023` : réponse OK et données retournées.
- [x] `controllers/effectifs.py` lit `profession_id`, `departement_id` et `annee`, récupére profession/département en base, appelle `AmeliAPI` et rend `effectifs.html`.
- [x] Correction effectuée : `/effectifs` n'exige plus `region_id`, donc la route respecte le tutoriel 2. Si `region_id` est absent, la région est déduite du département.
- [x] Correction effectuée : les paramétres manquants sont validés avant `session.get()`, ce qui supprime les avertissements SQLAlchemy.
- [x] `templates/effectifs.html` affiche un tableau avec année, effectif et densité, puis expose les données d'évolution pour Chart.js.
- [x] `static/js/charts.js` crée un graphique Chart.js de type `line` pour les effectifs, avec un second jeu de données pour la densité.
- [x] `templates/erreur.html` existe et renvoie vers l'accueil.
- [x] Les gestionnaires globaux `404` et `500` existent dans `app.py`.
- [x] Tests Flask effectués : `/api/departements/<id>` retourne `HTTP 200`, `/effectifs` retourne `HTTP 200` avec et sans `region_id`, `/effectifs` sans paramétres retourne `HTTP 400`, une route inconnue retourne `HTTP 404`.
- [x] Compilation Python effectuée avec `python -m compileall app.py config.py controllers models services`.
- [x] Le projet va plus loin que le tutoriel 2 : carte Leaflet, prévisualisation, export CSV, filtres supplémentaires et graphiques enrichis. Ces ajouts ne bloquent pas les consignes du tutoriel 2.
