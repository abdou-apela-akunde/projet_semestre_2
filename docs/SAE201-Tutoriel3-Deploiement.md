# Tutoriel #3 - Déploiement sur Alwaysdata

Source : `SAE201-Tutoriel3-Deploiement.pdf`

## Suivi

- [x] Tutoriel lu
- [x] Prérequis vérifiés
- [ ] Toutes les étapes réalisées
- [ ] Résultat final testé

## Consignes détaillées

Déploiement sur Alwaysdata

Mettre l'application en ligne sur sae204.alwaysdata.net dans un sous-dossier d'équipe.

Ce tutoriel est optionnel : votre application fonctionne déjà en local, et cela suffit pour valider le
projet. Il s'adresse aux équipes qui souhaitent rendre leur application accessible en ligne, via un
compte Alwaysdata mutualisé mis à disposition par l'enseignant.
Contexte particulier : un compte partagé en sous-dossiers
Pour cette SAE, un compte Alwaysdata gratuit est partagé par toutes les équipes. Chaque
équipe publie son application dans un SOUS-DOSSIER du même site (par exemple
sae204.alwaysdata.net/sae204_a1, sae204.alwaysdata.net/sae204_b3…). Ce mode est
différent d'un déploiement classique sur un sous-domaine : quelques ajustements sont
nécessaires, notamment sur la génération des URLs.

Prérequis
Avoir terminé les tutoriels #1 et #2 : application Flask qui tourne en local et affiche les
résultats depuis l'API ameli.fr. Toutes les URLs du code doivent être générées via url_for() (pas
de chemins en dur type /effectifs dans les templates).

## 1. Le compte Alwaysdata mutualisé

- [x] Réaliser : 1. Le compte Alwaysdata mutualisé

### 1.1 Ce qui est fourni

- [x] Réaliser : Ce qui est fourni

L'enseignant fournit les informations de connexion au compte Alwaysdata commun :
• Panneau d'administration : https://admin.alwaysdata.com/ — identifiant delechelle@u-
pec.fr (mot de passe communiqué par l'enseignant).
• Accès SFTP (pour FileZilla) : hôte ssh-sae204.alwaysdata.net, identifiant sae204, même mot
de passe que le compte Alwaysdata (voir section 2 et Annexe 2).
`• URL publique du site : https://sae204.alwaysdata.net/`
Important : un compte partagé
Toutes les équipes se connectent avec les MÊMES identifiants. Vous voyez donc les fichiers
des autres équipes : respectez leur espace et ne modifiez que votre dossier. Chaque équipe
travaille dans un sous-dossier nommé sae201_XX (XX = lettre de groupe + numéro d'équipe,
par exemple a1 pour la 1re équipe du groupe FI1A, b3, c6…), qu'elle crée elle -même dans le
dossier www (voir section 4.1).

⚠  SECTION CRITIQUE — COMPTE PARTAGÉ  ⚠
Toutes les équipes utilisent le MÊME compte Alwaysdata : mêmes identifiants, même
panneau d'administration, même espace de fichiers. Vous pouvez donc techniquement
voir, modifier ET supprimer le travail des autres équipes. NE TOUCHEZ JAMAIS à un
dossier (/www/sae201_XX) ou à un site qui n'est pas le vôtre : une seule fausse
manipulation peut détruire le déploiement d'une autre équipe. En cas de doute sur
votre identifiant XX, demandez à l'enseignant AVANT d'agir.

### 1.2 L'URL finale

- [x] Réaliser : L'URL finale

Votre application sera accessible à l'adresse :
`https://sae204.alwaysdata.net/sae201_XX/`
Le XX est à remplacer par votre identifiant d'équipe. Cette URL servira à l'enseignant et à vos
camarades pour tester votre application.
Pourquoi sae201 pour l'application et sae204 pour la base -
Le serveur s'appelle sae204.alwaysdata.net car il a d'abord servi à héberger la base de
données construite en SAE2.04. Mais l'application que vous déployez ici est le livrable de la
SAE2.01 : son dossier se nomme donc sae201_XX. À l'inverse, la base reste un livrable SAE2.04
et garde son nom sae204_XX_bd (utilisateur sae204_XX_user). Règle simple : le préfixe
indique la SAE qui a produit l'élément (sae201 = l'app, sae204 = la base).

## 2. Installation de FileZilla

- [ ] Réaliser : 2. Installation de FileZilla

FileZilla est un client FTP gratuit, multiplateforme et intuitif. Il permet de transférer des fichiers
entre votre poste et le serveur Alwaysdata par simple glisser -déposer.
Première fois avec un transfert de fichiers -  Voir l'Annexe 2
Si vous n'avez jamais utilisé d'outil de transfert (FTP/SFTP), lisez d'abord l'Annexe 2 «
Transférer ses fichiers avec FileZilla » : elle explique tout depuis le début (installation,
connexion, interface, glisser -déposer, filtres). La présente section en reprend uniquement
l'essentiel nécessaire au déploiement.

### 2.1 Téléchargement

- [ ] Réaliser : Téléchargement

Télécharger FileZilla Client (pas FileZilla Server !) depuis le site officiel :
https://filezilla-project.org/download.php- type=client
Installer le logiciel en gardant les options par défaut. Si l'installateur propose d'installer des
logiciels additionnels (barres d'outils, etc.), décocher toutes les cases.
### 2.2 Configuration de la connexion

- [ ] Réaliser : Configuration de la connexion

Ouvrir FileZilla puis se rendre dans : Fichier → Gestionnaire de sites → Nouveau site.
Renseigner les paramètres fournis par l'enseignant :
Champ  Valeur
Protocole  SFTP – SSH File Transfer Protocol
(recommandé)
Hôte  ssh-sae204.alwaysdata.net
Port  22
Type d'authentification  Demander le mot de passe
Utilisateur  sae204
Mot de passe  identique au compte Alwaysdata
(communiqué par l'enseignant)

Cliquer sur « Connexion ». FileZilla tente de se connecter au serveur. À la première connexion,
un avertissement sur la clé SSH de l'hôte peut apparaître : cocher « Toujours faire confiance à
cet hôte » puis valider.
Interface FileZilla
FileZilla affiche deux panneaux : à gauche votre poste local, à droite le serveur distant. Le
transfert se fait par glisser -déposer d'un panneau à l'autre. La queue en bas montre les
transferts en cours.

## 3. Préparation de l'application pour la production

- [x] Réaliser : 3. Préparation de l'application pour la production

### 3.1 Générer le fichier requirements.txt

- [x] Réaliser : Générer le fichier requirements.txt

Ce fichier liste les dépendances Python du projet. Il sera utilisé sur le serveur pour installer les
bibliothèques nécessaires. Depuis le terminal local, à la racine du projet :
```bash
pip freeze > requirements.txt
```

Vérifier que le fichier contient bien flask, sqlalchemy, pymysql, python-dotenv et requests (avec
leurs versions respectives).
### 3.2 Créer le fichier wsgi.py

- [x] Réaliser : Créer le fichier wsgi.py

Le serveur Alwaysdata a besoin d'un point d'entrée WSGI standard. Créer le fichier wsgi.py à la
racine du projet, à côté de app.py :
### `wsgi.py`

```python
"""Point d'entrée WSGI pour le serveur Alwaysdata."""

from app import app as application

# Alwaysdata s'attend à une variable nommée "application"
3.3 Adapter la configuration pour le sous-dossier
```

Comme l'application sera montée à l'URL /sae201_XX/, Flask doit le savoir pour générer
correctement les URLs via url_for(). Bonne nouvelle : Alwaysdata passe automatiquement cette
information à l'application via la variable WSGI SCRIPT_NAME, et Flask l'exploite tout seul.
La seule précaution à prendre : ne JAMAIS écrire d'URL en dur dans le code. Toujours utiliser
url_for('blueprint.route') côté Python et {{ url_for('blueprint.route') }} côté Jinja2. Les tutoriels
précédents respectent déjà cette règle.
Vérification rapide
Dans les templates, chercher les occurrences de href="/ ou src="/. Toute URL commençant
par un slash et non générée par url_for() va casser en production. La remplacer par un appel
url_for() avec le bon nom de route.

### 3.4 Fichiers à NE PAS transférer

- [x] Réaliser : Fichiers à NE PAS transférer

Certains fichiers ne doivent jamais se retrouver sur le serveur :
• .env : contient le mot de passe MySQL. Les variables seront redéfinies côté serveur.
• venv/ : l'environnement virtuel sera recréé directement sur le serveur.
• __pycache__/ et .pyc : fichiers de cache Python, inutiles.
• .git/ : l'historique Git n'a pas sa place en production.
• tests/ et fichiers de développement : optionnel, mais allège le transfert.
## 4. Transfert des fichiers via FileZilla

- [ ] Réaliser : 4. Transfert des fichiers via FileZilla

### 4.1 Se positionner dans le bon dossier

- [ ] Réaliser : Se positionner dans le bon dossier

Après connexion, le panneau de droite affiche l'arborescence du serveur. Naviguer vers :
`/www/`
C'est le dossier racine du site web (le dossier www de votre compte). Votre équipe y crée elle -
même son sous-dossier :
• Clic droit dans le panneau de droite → Créer un répertoire.
• Nommer le dossier sae201_XX (XX = votre identifiant d'équipe, par exemple a1).
• Double-cliquer dessus pour entrer dedans : c'est là que vous déposerez vos fichiers.
Attention : ne touchez QUE votre dossier
Le panneau de droite affiche aussi les dossiers des autres équipes. Créez uniquement le vôtre
(sae201_XX) et ne modifiez, ne renommez ni ne supprimez jamais un dossier qui n'est pas le
vôtre : vous écraseriez le travail d'une autre équipe. Vérifiez bien votre identifiant XX.

Structure finale sur le serveur
Votre dossier /www/sae201_XX/ va contenir toute l'application : app.py, wsgi.py, models/,
services/, controllers/, templates/, static/, requirements.txt.

### 4.2 Transférer les fichiers

- [ ] Réaliser : Transférer les fichiers

Dans le panneau de gauche (votre poste), naviguer jusqu'au dossier du projet. Sélectionner les
fichiers et dossiers à transférer (cf. section 3.4 pour les exclusions).
Glisser -déposer la sélection vers le panneau de droite (dans /www/sae201_XX/). La file
d'attente en bas affiche la progression. Attendre que tous les transferts soient terminés.
Astuce : filtre de transfert
FileZilla propose un filtre qui exclut automatiquement certains fichiers : menu Affichage →
Filtre de fichiers et de dossiers. Créer un filtre qui exclut venv/, __pycache__/, .git/, .env,
*.pyc évite de devoir sélectionner manuellement.

### 4.3 Vérifier la structure

- [ ] Réaliser : Vérifier la structure

Dans le panneau de droite, vérifier que /www/sae201_XX/ contient :
`/www/sae201_XX/`
├── app.py
├── wsgi.py
├── config.py
├── requirements.txt
`├── models/`
`├── services/`
`├── controllers/`
`├── templates/`
`└── static/`
## 5. Environnement virtuel Python

- [ ] Réaliser : 5. Environnement virtuel Python

### 5.1 Pourquoi un environnement virtuel -

- [ ] Réaliser : Pourquoi un environnement virtuel -

Un environnement virtuel (venv) isole les dépendances Python d'un projet. Sur un serveur
partagé comme sae204.alwaysdata.net, chaque équipe aura le sien, ce qui évite les conflits de
versions entre projets.
### 5.2 Créer le venv sur le serveur

- [ ] Réaliser : Créer le venv sur le serveur

Il faut se connecter au serveur en SSH pour exécuter des commandes. Deux options :
• Option A : depuis FileZilla, menu Serveur → Entrer une commande personnalisée
(fonctionne uniquement pour des commandes simples).
• Option B (recommandée) : utiliser la console SSH intégrée au panneau Alwaysdata (Remote
access → SSH → Web console). Un terminal s'ouvre directement dans le navigateur.
Dans la console SSH, se placer dans le dossier du projet et créer le venv :
```bash
cd ~/www/sae201_XX
```

# Créer l'environnement virtuel
```bash
python3 -m venv venv
```

# L'activer
```bash
source venv/bin/activate
```

# Installer les dépendances
```bash
pip install -r requirements.txt
```

L'installation prend quelques secondes. À la fin, la commande pip list doit afficher flask,
sqlalchemy, pymysql, etc.
## 6. Configuration dans le panneau Alwaysdata

- [ ] Réaliser : 6. Configuration dans le panneau Alwaysdata

Se connecter à https://admin.alwaysdata.com/ avec l'identifiant du compte partagé
delechelle@u -pec.fr et le mot de passe communiqué par l'enseignant.
### 6.1 Définir les variables d'environnement

- [ ] Réaliser : Définir les variables d'environnement

Les variables du fichier .env local doivent être redéfinies côté serveur. Sur Alwaysdata, elles ne
se règlent PAS dans un panneau global du compte, mais directement dans la configuration de
VOTRE site, via son champ « Variables d'environnement ». Ce champ fait partie du formulaire de
création du site (étape 6.3) ; on peut aussi l'éditer ensuite depuis Web → Sites → votre site.
Y définir les paires NOM=valeur séparées par des espaces (FLASK_ENV passe à production) :
Nom  Valeur
DB_USER  sae204_XX_user
DB_PASSWORD  mot de passe MySQL
DB_HOST  mysql-sae204.alwaysdata.net
DB_NAME  sae204_XX_bd
FLASK_ENV  production
SECRET_KEY  chaîne aléatoire longue et unique par équipe

Isolation automatique par équipe
Comme ces variables sont attachées à votre site (et non au compte), il n'y a aucun risque de
conflit entre équipes : inutile de préfixer les noms. Chaque équipe renseigne simplement
DB_USER, DB_PASSWORD, etc. dans son propre site. Variante possible : conserver votre
fichier .env dans /www/sae201_XX/ ; config.py le chargera automatiquement via
load_dotenv().

### 6.2 Générer une SECRET_KEY

- [x] Réaliser : Générer une SECRET_KEY

La SECRET_KEY sert à signer les cookies de session Flask. Elle doit être une chaîne aléatoire
longue (≥ 32 caractères) et unique par équipe. Pour en générer une :
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6.3 Créer le site Python WSGI

- [ ] Réaliser : Créer le site Python WSGI

Chaque équipe crée elle -même son site. Depuis le panneau : Web → Sites → Ajouter un site.
Attention : ne modifiez que VOTRE site
Le panneau Web → Sites est partagé : vous y voyez les sites de toutes les équipes. Créez
uniquement le vôtre (Name sae201_XX) et ne modifiez, n'arrêtez ni ne supprimez jamais le
site d'une autre équipe. Vérifiez bien votre identifiant XX avant de valider.

Champ  Valeur
Nom  sae201_XX
Adresses  sae204.alwaysdata.net/sae201_XX
Type  Python WSGI
Chemin de l'application  /home/sae204/www/sae201_XX/wsgi.py
`Répertoire de travail  /home/sae204/www/sae201_XX/`
Variables d'environnement  DB_USER=sae204_XX_user
DB_PASSWORD=…  DB_HOST=mysql -
sae204.alwaysdata.net
DB_NAME=sae204_XX_bd
FLASK_ENV=production  SECRET_KEY=…
(paires NOM=valeur séparées par des
espaces)
Version de Python  Version par défaut (3.10 ou supérieure)
`Répertoire du virtualenv  /home/sae204/www/sae201_XX/venv/`
Chemins statiques  laisser vide (Flask sert /static/ lui -même)

Les chemins sont ABSOLUS, à partir de votre répertoire personnel /home/sae204/ (le ~ utilisé en
SSH correspond à /home/sae204). Le « Chemin de l'application » pointe vers le fichier wsgi.py
(qui expose la variable application) ; le « Répertoire du virtualenv » est le venv créé à l'étape 5.
Le type Python WSGI n'a PAS de champ « Command » : Alwaysdata lance l'application via ces
deux chemins. Valider avec le bouton Submit : le site passe de « Starting » à « Running ».
Chemins statiques et autres réglages
Laisser le champ « Chemins statiques » VIDE : l'application Flask sert elle -même ses fichiers
CSS/JS via la route /static/ (générée par url_for), ce qui fonctionne correctement avec le sous -
dossier. Tous les autres réglages gardent leurs valeurs par défaut. Le HTTPS est automatique
sur sae204.alwaysdata.net (rien à configurer).

Le champ « Adresses »
Indiquer le domaine du serveur suivi du sous-dossier de l'équipe, SANS https:// ni / final :
sae204.alwaysdata.net/sae201_XX (par exemple sae204.alwaysdata.net/sae201_a1). C'est ce
sous -chemin qu'Alwaysdata transmet à Flask via SCRIPT_NAME, ce qui permet à url_for() de
générer automatiquement les bons liens — d'où l'importance de ne jamais écrire d'URL en
dur (voir section 3.3). Le site sera alors accessible à
https://sae204.alwaysdata.net/sae201_XX/.
Redémarrer le site après chaque changement
Toute modification (nouvelles variables d'environnement, nouveaux fichiers uploadés, pip
install) nécessite un redémarrage du site. Depuis la liste des sites : bouton « Restart » à droite
du site concerné.

## 7. Vérification

- [ ] Réaliser : 7. Vérification

Ouvrir dans un navigateur : https://sae204.alwaysdata.net/sae201_XX/. La page d'accueil de
l'application doit apparaître, avec la liste des régions et des professions depuis la base.
Tester ensuite :
• la cascade région → département sur l'accueil,
• la soumission du formulaire (page /effectifs),
• l'affichage du tableau et du graphique,
• le rendu du CSS (si le style ne s'applique pas, c'est qu'une URL statique est en dur).
### 7.1 En cas d'erreur

- [ ] Réaliser : En cas d'erreur

Consulter les logs depuis le panneau Alwaysdata : Web → Sites → votre site → onglet Logs.
Message  Cause probable
500 Internal Server Error  Erreur Python côté serveur. Consulter les logs
pour la trace d'exécution.
404 Not Found sur une route  URL écrite en dur dans un template. La
remplacer par url_for().
ModuleNotFoundError  pip install -r requirements.txt a échoué ou n'a
pas été exécuté dans le venv.
Access denied (MySQL)  Variables d'environnement DB_* mal
configurées dans le panneau.

Debug temporaire
Pour diagnostiquer une erreur obscure, activer temporairement le mode debug en ajoutant
FLASK_DEBUG = 1 dans les variables d'environnement, puis redémarrer le site. ATTENTION :
ne jamais laisser le mode debug actif en production (il expose du code sensible au public). Le
désactiver dès que le problème est résolu.

## 8. Mettre à jour l'application

- [ ] Réaliser : 8. Mettre à jour l'application

À chaque modification de code, la mise en production suit ce workflow :
## 1. Tester la modification en local (python app.py).

- [x] Réaliser : 1. Tester la modification en local (python app.py).

## 2. Dans FileZilla, transférer les fichiers modifiés vers /www/sae201_XX/.

- [ ] Réaliser : 2. Dans FileZilla, transférer les fichiers modifiés vers /www/sae201_XX/.

## 3. Si requirements.txt a changé : ouvrir la console SSH, activer le venv, relancer pip install -r

- [x] Réaliser : 3. Si requirements.txt a changé : ouvrir la console SSH, activer le venv, relancer pip install -r

requirements.txt.
## 4. Dans le panneau Alwaysdata, redémarrer le site (bouton Restart).

- [ ] Réaliser : 4. Dans le panneau Alwaysdata, redémarrer le site (bouton Restart).

## 5. Vérifier le résultat en ligne.

- [ ] Réaliser : 5. Vérifier le résultat en ligne.

Pour aller plus loin (optionnel)
Les équipes qui utilisent Git peuvent automatiser le déploiement en clonant leur dépôt
directement sur le serveur, puis en mettant à jour par git pull. C'est plus rapide qu'un
transfert FTP manuel, mais cela suppose une bonne maîtrise de Git. Cette approche est
proposée aux équipes intéressées : demandez conseil à l'enseignant.

Bilan du déploiement
Votre application est maintenant :
• accessible en ligne à https://sae204.alwaysdata.net/sae201_XX/,
• exécutée dans un environnement virtuel Python isolé,
• configurée via des variables d'environnement (pas de mot de passe dans le code),
• prête à être partagée avec l'enseignant et vos camarades pour démonstration.
Félicitations : vous maîtrisez désormais la chaîne complète, du développement local jusqu'à la
mise en production d'une application web !

## Audit du projet - 2026-06-21

- [x] Identifiants MySQL ajoutés dans `.env` : `DB_USER=sae204_b6_user`, `DB_NAME=sae204_b6_bd`, `DB_HOST=mysql-sae204.alwaysdata.net`.
- [x] Connexion à la vraie base MySQL testée avec SQLAlchemy/PyMySQL : connexion OK.
- [x] Comptes vérifiés dans la base MySQL : 19 régions, 100 départements, 38 professions.
- [x] URL finale attendue pour l'équipe b6 : `https://sae204.alwaysdata.net/sae201_b6/`.
- [x] `requirements.txt` contient les dépendances nécessaires au déploiement : Flask, SQLAlchemy, PyMySQL, python-dotenv et requests.
- [x] `wsgi.py` expose bien `application` avec `from app import app as application`.
- [x] `SECRET_KEY` locale remplacée par une chaîne aléatoire longue.
- [x] `.gitignore` protége les fichiers à ne pas transférer : `.env`, `.git/`, `venv/`, `.vscode/`, `__pycache__/`, `*.pyc`.
- [x] Recherche d'URLs locales en dur dans `templates/`, `static/`, `controllers/` et `app.py` : aucune occurrence bloquante de `href="/`, `src="/`, `action="/` ou `fetch("/` trouvée.
- [x] Test sous-dossier avec `SCRIPT_NAME=/sae201_b6` : Flask génére bien les URLs préfixées (`/sae201_b6/static/...`, `/sae201_b6/effectifs`, `/sae201_b6/api/...`).
- [x] Test local avec la vraie base MySQL : `/` retourne `HTTP 200` et `/api/departements/<id>` retourne `HTTP 200`.
- [x] Compilation Python effectuée avec `python -m compileall app.py config.py controllers models services wsgi.py`.
- [ ] FileZilla non vérifié depuis ce poste : installation, connexion SFTP et transfert restent à faire manuellement.
- [ ] Dossier serveur `/www/sae201_b6/` non vérifié : je n'ai pas accédé au compte SFTP/Alwaysdata partagé.
- [ ] Environnement virtuel serveur non créé depuis ici : commandes à exécuter sur Alwaysdata dans `~/www/sae201_b6`.
- [ ] Site Python WSGI non créé dans le panneau Alwaysdata : à configurer avec `sae204.alwaysdata.net/sae201_b6`, `wsgi.py`, le venv, et les variables d'environnement.
- [ ] Vérification en ligne non faite : l'URL publique `https://sae204.alwaysdata.net/sae201_b6/` doit être testée après transfert et redémarrage du site.

### Valeurs à utiliser sur Alwaysdata

- Nom du site : `sae201_b6`
- Adresse : `sae204.alwaysdata.net/sae201_b6`
- Chemin de l'application : `/home/sae204/www/sae201_b6/wsgi.py`
- Répertoire de travail : `/home/sae204/www/sae201_b6/`
- Répertoire du virtualenv : `/home/sae204/www/sae201_b6/venv/`
- Variables : `DB_USER=sae204_b6_user DB_PASSWORD=<mot de passe fourni> DB_HOST=mysql-sae204.alwaysdata.net DB_NAME=sae204_b6_bd FLASK_ENV=production SECRET_KEY=<clé longue>`
- Chemins statiques : laisser vide
