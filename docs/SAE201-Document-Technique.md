# SAE201 - Document technique

Source : `SAE201-Document-Technique.pdf`

## Contenu extrait

## Page 1

SAE 2.01
Développement d'une application
Application web Flask autour des données de santé

Document technique du projet

BUT Informatique  ·  IUT de Créteil -Vitry  ·  Département Informatique

À propos de ce document
Ce document technique est le fil conducteur du projet. Il présente l'application à réaliser,
explique les concepts mobilisés (POO, MVC) et accompagne les trois tutoriels pas à pas. Lisez -
le en entier avant de commencer, puis suivez les tutoriels #1 et #2 pour construire
l'application, et enrichissez -la avec les fonctionnalités du chapitre 6. Le tutoriel #3
(déploiement en ligne) est optionnel.

Compétence visée
Compétence 3 – Développer des applications informatiques simples.
• AC1 – Adopter de bonnes pratiques de conception et de programmation (architecture MVC,
séparation des responsabilités, documentation).
• AC2 – Apprendre à travailler en équipe: répartition des tâches, partage du code, revue
mutuelle.
• AC3 – Développer des interfaces utilisateurs (formulaires, visualisations, ergonomie web).
## Page 2

## 1. Introduction

Cette SAE prolonge directement la SAE2.04: la base de données de dimensions que vous avez
construite va maintenant être exploitée par une véritable application web. L'enjeu est de
transformer des données brutes en information utile pour un utilisateur final.
Concrètement, l'application développée permettra à un utilisateur de:
• choisir une profession de santé (médecin généraliste, kinésithérapeute…) et un territoire
(région ou département),
• consulter en temps réel les effectifs, densités, honoraires ou prescriptions correspondants,
• visualiser les données sous forme de tableaux et de graphiques,
• comparer plusieurs territoires ou plusieurs professions.
Articulation avec la SAE2.04
Les 9 tables de dimensions créées en SAE2.04 alimentent les listes déroulantes sans appel API.
Les valeurs chiffrées (effectifs, honoraires…) sont récupérées dynamiquement via l'API
ameli.fr. Cette répartition donne une application rapide côté interface et toujours à jour côté
données.

1.1 Pourquoi cette SAE -
Au-delà du résultat visible, cette SAE est l'occasion de mobiliser et de consolider trois blocs de
compétences fondamentales en informatique:
• La programmation orientée objet (POO) en Python: classes, objets, attributs, méthodes,
encapsulation, héritage. Ces notions, déjà abordées en R1.01, prennent ici tout leur sens
dans un projet réaliste.
• Le développement web: comprendre le protocole HTTP, les routes, les templates,
l'architecture MVC, et l'interaction client/serveur.
• Le travail en équipe: répartition des tâches, séparation propre des rôles dans le code,
partage et revue mutuelle. Une application bien structurée se développe à plusieurs sans se
marcher dessus.
1.2 Trois tutoriels pour démarrer
Trois tutoriels accompagnent cette SAE. Les deux premiers sont indispensables et proposent une
mise en œuvre pas à pas de l'application avec tout le code de démarrage nécessaire. Le
troisième est optionnel:
Tutoriel  Contenu
Tutoriel #1  Mise en place de Flask et connexion à la base
SAE2.04. Premier template, affichage des
régions et professions.
Tutoriel #2  Formulaire de sélection, cascade AJAX, appel
à l'API ameli.fr, tableau de résultats et
## Page 3

graphique Chart.js.
Tutoriel #3 (optionnel)  Déploiement de l'application sur le compte
Alwaysdata partagé sae204.alwaysdata.net,
dans un sous-dossier d'équipe. Transfert des
fichiers via FileZilla, environnement virtuel,
## configuration du site Python WSGI.

À l'issue des deux tutoriels, vous disposez d'une application fonctionnelle. Le travail consiste
ensuite à l'enrichir avec les fonctionnalités décrites au chapitre 6.
1.3 Votre feuille de route
Pour mener le projet à bien, suivez ces étapes dans l'ordre. Chacune s'appuie sur ce document
et sur les tutoriels:
## 1. Lire ce document technique en entier pour comprendre l'objectif, l'architecture et les

attendus.
## 2. Suivre le tutoriel #1: installer Flask, se connecter à la base SAE2.04, afficher une première

page.
## 3. Suivre le tutoriel #2: formulaire de sélection, cascade AJAX, appels à l'API ameli.fr, tableau

et graphique.
## 4. Enrichir l'application avec les fonctionnalités du chapitre 6 (selon le niveau visé par l'équipe).

## 5. Préparer les livrables du chapitre 8 (code, README, démonstration).

## 6. Optionnel: suivre le tutoriel #3 pour déployer l'application en ligne sur Alwaysdata.

Se répartir le travail dès le départ
Les tutoriels #1 et #2 sont à faire ensemble au début (toute l'équipe part sur les mêmes
bases). L'enrichissement du chapitre 6 se prête bien à une répartition par pages ou par
fonctionnalités entre coéquipiers. Voir la section 7.3 pour l'organisation en équipe.

## 2. La programmation orientée objet au cœur du projet

La POO n'est pas un ornement dans ce projet: elle structure chaque composant. Les données,
l'accès à l'API, les pages, les services sont des classes. Cette section rappelle les concepts clés et
indique comment ils se manifestent concrètement dans l'application.
2.1 Les concepts à mobiliser
Concept  Application dans le projet
Classe & instance  Une classe Departement représente la
structure d'un département. Chaque ligne de
la table est une instance de cette classe.
Encapsulation  Les attributs internes (connexion HTTP,
## Page 4

cache, session SQL) sont cachés derrière des
méthodes publiques claires. L'appelant n'a
pas à connaître les détails.
Héritage  Les templates Jinja2 héritent d'un template
parent base.html, ce qui factorise les
éléments communs (menu, en -tête, pied).
Polymorphisme  Un même service peut exposer des méthodes
identiques quelle que soit la source des
données (API, base, cache).
Composition  Un contrôleur utilise à la fois un modèle
(accès base) et un service (accès API), sans les
créer lui -même.

2.2 Deux classes emblématiques
Deux classes centrales illustrent parfaitement la démarche orientée objet dans le projet:
• Les modèles ORM (Region, Departement, ProfessionSante, etc.), déjà écrits en SAE2.04. Ils
représentent les données métier et sont manipulés comme de simples objets Python.
• La classe AmeliAPI, qui encapsule tous les appels à l'API data.ameli.fr. Plutôt que de
disséminer des appels HTTP un peu partout, on centralise toute la logique dans une seule
classe aux méthodes métier claires (get_effectifs, get_honoraires…).
Pourquoi encapsuler les appels API -
Si l'URL change, si l'API évolue, ou s'il faut ajouter un système de cache: un seul endroit du
code est à modifier. L'encapsulation garantit que les contrôleurs restent simples et lisibles.
C'est un principe applicable bien au -delà de ce projet.

## 3. Architecture MVC

3.1 Le principe
Le MVC (Modèle – Vue – Contrôleur) est un patron de conception qui sépare une application en
trois responsabilités distinctes. Cette séparation rend le code plus lisible, plus testable, et plus
facile à faire évoluer.
Rôle  Contenu dans le projet
Modèle (M)  Les données et leur logique: classes ORM,
services métier, accès à la base.
Vue (V)  L'affichage: templates HTML (Jinja2), fichiers
CSS/JS. La vue ne contient pas de logique
métier.
## Page 5

Contrôleur (C)  Le chef d'orchestre: routes Flask qui
reçoivent la requête, interrogent les modèles
et rendent une vue.

3.2 Cycle de vie d'une requête
## Exemple: l'utilisateur clique sur « Afficher les effectifs ».

## 7. Le navigateur envoie une requête HTTP GET vers /effectifs- profession=3&dept=75.

## 8. Flask route la requête vers le CONTRÔLEUR correspondant.

## 9. Le contrôleur interroge le MODÈLE pour récupérer les libellés depuis la base.

## 10. Le contrôleur interroge le SERVICE API pour récupérer les effectifs.

## 11. Le contrôleur envoie les données à la VUE (template Jinja2).

## 12. La vue génère le HTML, qui est renvoyé au navigateur.

Bonne pratique: vue fine, contrôleur fin, modèle gras
Le template ne doit contenir que de l'affichage (pas de calcul). Le contrôleur ne doit contenir
que de l'aiguillage (pas de logique métier). Toute la logique métier vit dans les modèles et les
services. Ce principe porte un nom: « fat model, thin controller ».

## 4. Stack technique

Brique  Rôle
Python 3  Langage principal (version 3.10 ou supérieure
recommandée).
Flask  Framework web léger: routes, templates,
sessions.
Jinja2  Moteur de templates intégré à Flask.
SQLAlchemy  ORM déjà utilisé en SAE2.04 pour accéder à
la base MySQL.
requests  Bibliothèque HTTP pour appeler l'API
ameli.fr.
Chart.js  Bibliothèque JavaScript pour les graphiques
interactifs.

Toutes les étapes d'installation et de configuration sont détaillées dans le tutoriel #1.
## Page 6

## 5. Structure du projet

Une bonne structure facilite le travail d'équipe et la maintenance. L'organisation recommandée
applique directement le MVC:
```text
SAE201-app/
```

`├── app.py                    ← point d'entrée Flask`
`├── config.py                 ← configuration (chargement.env)`
`├──.env                      ← identifiants (NON versionné)`
`├──.env.example              ← modèle de.env (versionné)`
`├── requirements.txt          ← dépendances Python`
│
`├── models/                   ← MODÈLE`
│   ├── db.py                 ← moteur SQLAlchemy + session
│   └── dimensions.py         ← classes ORM (Region, Departement…)
│
├── services/                 ← SERVICES MÉTIER
│   └── ameli_api.py          ← classe AmeliAPI
│
`├── controllers/              ← CONTRÔLEURS (routes)`
│   ├── accueil.py
│   ├── effectifs.py
│   └── api.py                ← routes JSON pour AJAX
│
`├── templates/                ← VUES (HTML Jinja2)`
│   ├── base.html
│   ├── accueil.html
│   └── erreur.html
│
`└── static/                   ← RESSOURCES STATIQUES`
├── css/
└── js/
Pourquoi cette structure -
Chaque dossier a une responsabilité claire: si on cherche un bug d'affichage, on va dans
`templates/; si c'est un problème d'API, on va dans services/; si c'est une nouvelle page, on`
`ajoute un fichier dans controllers/. Cette discipline rend le projet lisible pour n'importe quel`
membre de l'équipe.

## Page 7

## 6. Fonctionnalités à implémenter

6.1 Fonctionnalités minimales (niveau attendu)
Les fonctionnalités suivantes sont le socle que chaque équipe doit livrer. Elles sont en grande
partie couvertes par les deux tutoriels:
• Page d'accueil avec un formulaire de sélection (profession, région, département, année).
• Cascade région → département: la liste des départements se met à jour automatiquement
quand on change de région.
• Page de résultats affichant les effectifs et densités dans un tableau.
• Au moins un graphique (courbe ou histogramme) illustrant les données.
• Gestion d'erreur propre: page 404, message explicite si l'API ne répond pas.
6.2 Fonctionnalités avancées (valorisées)
• Page « Honoraires » avec sélection du type d'honoraire (secteurs, dépassements).
• Page « Prescriptions » avec sélection du poste de prescription.
• Page de comparaison entre deux départements (double formulaire, graphiques superposés).
• Mise en cache des appels API pour accélérer l'application.
• Export des données au format CSV ou PDF.
• Authentification simple (login administrateur pour accéder à des statistiques).
6.3 Fonctionnalités d'ouverture (pour les équipes à l'aise)
• Tests unitaires avec pytest (au moins la classe AmeliAPI).
• Déploiement sur un compte Alwaysdata gratuit (optionnel).
• Dashboard interactif avec Plotly ou Chart.js avancé.
• Carte interactive des densités par département (Leaflet).
## 7. Environnement de développement

7.1 Base de données
La base MySQL est la même que celle de la SAE2.04. Aucune migration n'est nécessaire: vos 9
tables de dimensions sont déjà prêtes à être interrogées. Chaque équipe dispose de sa propre
base nommée sae204_XX_bd (XX = identifiant d'équipe), avec son utilisateur sae204_XX_user,
`sur le serveur MySQL fourni par l'enseignant. Le fichier.env local pointe vers ce serveur distant`
(détails et identifiants dans le tutoriel #1).
7.2 Exécution locale
L'application tourne en local sur le poste de développement, via le serveur intégré de Flask. Elle
est alors accessible sur http://localhost:5000 dans le navigateur.
Déploiement sur Alwaysdata: optionnel
## Page 8

Les équipes à l'aise pourront déployer leur application en ligne sur le compte Alwaysdata
mutualisé sae204.alwaysdata.net, dans un sous-dossier d'équipe. La marche à suivre est
détaillée dans le tutoriel #3. Ce n'est pas un prérequis: une application qui tourne en local et
qui est démontrée correctement en soutenance suffit pour valider le projet.

7.3 S'organiser en équipe
Le projet est développé à plusieurs. Plusieurs approches sont possibles pour partager le code
entre coéquipiers:
• Approche simple: partage via un dossier commun (OneDrive, Drive partagé, clé USB) ou
envoi d'archives ZIP. C'est suffisant pour démarrer, mais à éviter pour la modification
simultanée d'un même fichier.
• Approche recommandée: utiliser un dépôt Git partagé (GitHub, GitLab). Git permet de
travailler à plusieurs sur un même code, de garder l'historique des modifications et de
revenir en arrière en cas de problème. Les notions de base vues en R1.01 (clone, commit,
push, pull) suffisent à démarrer.
Git: proposé, non imposé
Les équipes à l'aise avec Git sont encouragées à l'utiliser: c'est un vrai atout pour la suite de la
formation. Les équipes moins à l'aise peuvent démarrer avec un partage simple et adopter Git
plus tard si elles le souhaitent. L'essentiel est que chaque membre puisse contribuer sans
écraser le travail des autres.

Quelques règles à respecter, quelle que soit l'approche:
• Se répartir clairement les tâches (qui fait quoi, avec quelle échéance).
• Communiquer régulièrement (fichier modifié par un binôme = à signaler).
`• Ne JAMAIS partager le fichier.env (il contient le mot de passe MySQL).`
• Ne JAMAIS mettre de mot de passe ou clé d'API en dur dans le code.
## 8. Livrables attendus

Chaque équipe remet à la fin du projet:
8.1 Le code source
Le code peut être remis sous forme d'archive ZIP ou via un lien vers un dépôt Git partagé
(GitHub, GitLab) — l'équipe choisit l'option qui lui convient le mieux.
• Structure de projet conforme à la section 5.
`• Fichier.env.example présent; le fichier.env (avec les vrais identifiants) doit être ABSENT de`
la livraison.
`• Fichier requirements.txt à jour (généré avec pip freeze).`
## Page 9

`• Si Git est utilisé: un fichier.gitignore correct (exclut.env, venv/, __pycache__/).`
8.2 Documentation
• Un fichier README.md avec:
• présentation du projet et composition de l'équipe,
• prérequis et étapes d'installation,
• commande de lancement,
• captures d'écran des pages principales,
• liste des fonctionnalités implémentées (minimales + avancées).
8.3 Application fonctionnelle
`• Application lançable en local via python app.py.`
• Toutes les fonctionnalités minimales de la section 6.1 opérationnelles.
• Aucune erreur 500 sur le chemin principal (accueil → résultats).
8.4 Soutenance
Démonstration orale de l'application (durée précisée par l'enseignant) couvrant:
• une démo du chemin principal de l'application,
• une explication de l'architecture MVC mise en place,
• la présentation d'une ou deux classes représentatives,
• la répartition du travail dans l'équipe (qui a fait quoi),
• les difficultés rencontrées et les solutions apportées.
Critères de qualité valorisés
Au-delà du bon fonctionnement: la qualité du code (POO respectée, noms clairs,
commentaires pertinents), la structure du projet, la maîtrise de Git (branches, commits),
l'ergonomie de l'interface, et la capacité de chaque membre à expliquer le code écrit par ses
coéquipiers.

## 9. Pour aller plus loin

Les équipes qui souhaitent approfondir peuvent explorer plusieurs pistes au -delà du minimum
attendu:
9.1 Tests automatisés
Écrire des tests unitaires avec pytest pour les classes critiques (notamment AmeliAPI). Cette
démarche améliore la fiabilité du code et documente le comportement attendu.
## Page 10

9.2 Mise en cache
Les appels à l'API ameli.fr peuvent être lents. Implémenter une classe de cache qui mémorise les
réponses pendant quelques minutes réduit drastiquement les temps de chargement. C'est aussi
une belle illustration du principe de décoration (design pattern).
9.3 Déploiement sur Alwaysdata
Mettre l'application en ligne sur le compte Alwaysdata mutualisé sae204.alwaysdata.net, dans
le sous-dossier de l'équipe (nommé sae201_XX — le préfixe sae201 indique qu'il s'agit de
l'application, livrable de cette SAE, tandis que la base garde son nom sae204_XX_bd). Cette
étape implique la création d'un environnement virtuel Python, le transfert des fichiers via
FileZilla, la configuration des variables d'environnement, et la création d'un site Python WSGI
dans le panneau Alwaysdata. Le tutoriel #3 détaille l'ensemble de la procédure pas à pas.
9.4 Accessibilité et ergonomie
Soigner le design (CSS, responsive, contraste), ajouter des attributs d'accessibilité (aria -*, labels
explicites), et tester au clavier. Une application bien conçue est une application utilisable par
tous.

✦  ✦  ✦
## Audit du projet - 2026-06-21

- [x] Architecture MVC respect?e : `models/`, `controllers/`, `templates/`, `services/`, `static/`.
- [x] POO pr?sente : mod?les ORM SQLAlchemy, classe `AmeliAPI`, d?corateur de cache et wrapper `CachedAmeliAPI`.
- [x] Base SAE2.04 utilis?e : connexion MySQL active, avec 19 r?gions, 100 d?partements et 38 professions v?rifi?s.
- [x] Page d'accueil avec formulaire profession, r?gion, d?partement et ann?e.
- [x] Cascade AJAX r?gion vers d?partement via `/api/departements/<region_id>` et `static/js/cascade.js`.
- [x] Page `/effectifs` avec tableau effectif/densit? et graphique Chart.js.
- [x] Gestion d'erreur pr?sente : page `templates/erreur.html`, handlers 404 et 500, messages API.
- [x] Fonctionnalit?s avanc?es pr?sentes : secteurs, honoraires, prescriptions, indicateurs, comparaisons, carte Leaflet, pr?visualisation, export CSV.
- [x] Mise en cache des appels API impl?ment?e.
- [x] Export CSV op?rationnel : `/export/effectifs.csv` retourne un fichier `text/csv` et g?re les param?tres invalides en 400.
- [x] D?ploiement pr?par? : `.env.example`, `requirements.txt`, `wsgi.py`, URLs compatibles sous-dossier.
- [x] README pr?sent avec pr?sentation, membres, installation, commande de lancement, configuration, structure et d?ploiement.
- [ ] Captures d'?cran des pages principales non pr?sentes dans le README.
- [ ] Tests unitaires `pytest` non pr?sents dans le projet ; c'est une piste avanc?e du document technique.
- [ ] D?ploiement public Alwaysdata non v?rifi? depuis cette session.
- [ ] R?partition r?elle du travail et soutenance orale non v?rifiables depuis le code.
