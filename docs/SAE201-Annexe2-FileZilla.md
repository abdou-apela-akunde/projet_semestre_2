# SAE201 - Annexe 2 - FileZilla

Source : `SAE201-Annexe2-FileZilla.pdf`

## Contenu extrait

## Page 1

SAE 2.01 – Annexe 2
Transférer ses fichiers avec FileZilla
Mettre son application en ligne par SFTP, pas à pas

BUT Informatique  ·  IUT de Créteil -Vitry  ·  Département Informatique

## Objectif de cette annexe

Cette annexe accompagne le tutoriel #3 (déploiement). Déposer des fichiers sur un serveur
distant est une opération nouvelle pour vous: on l'explique donc ici depuis le début, sans rien
supposer connu. À la fin, vous saurez installer FileZilla, vous connecter au serveur Alwaysdata
et y transférer votre application en toute sécurité.

## Page 2

## 1. Le principe: déposer des fichiers sur un serveur distant

Jusqu'ici, votre application vivait uniquement sur votre ordinateur. Pour qu'elle soit accessible
en ligne, ses fichiers doivent être copiés sur une autre machine, allumée en permanence et
reliée à Internet: le serveur. Cette opération de copie s'appelle le transfert de fichiers.
Le transfert suit un modèle client / serveur: un logiciel installé sur votre poste (le client) se
connecte au serveur distant et y envoie (ou en récupère) des fichiers. Ce logiciel client, ici, c'est
FileZilla.
FTP et SFTP: quelle différence -
FTP (File Transfer Protocol) est le protocole historique de transfert de fichiers, mais il fait
circuler les données et les mots de passe en clair. SFTP (SSH File Transfer Protocol) fait la
même chose de façon chiffrée, à travers une connexion SSH sécurisée (port 22). C'est SFTP
que nous utiliserons: plus sûr, et recommandé par Alwaysdata.

## 2. Installer FileZilla

FileZilla est un client de transfert gratuit, en français, qui fonctionne sous Windows, macOS et
Linux.
Télécharger FileZilla Client (et surtout PAS FileZilla Server) depuis le site officiel:
https://filezilla-project.org/download.php- type=client
Lancer l'installation en gardant les options par défaut. Si l'installateur propose des logiciels
additionnels (barres d'outils, antivirus, etc.), décocher toutes ces cases avant de continuer.
⚠  CLIENT, PAS SERVER  ⚠
Téléchargez bien « FileZilla Client ». « FileZilla Server » est un autre logiciel, qui sert à
HÉBERGER des fichiers, pas à en envoyer: il ne vous servirait à rien ici.

## 3. Se connecter au serveur Alwaysdata

Plutôt que de retaper les paramètres à chaque fois, on enregistre la connexion dans le
Gestionnaire de sites. Ouvrir: Fichier → Gestionnaire de sites → Nouveau site. Donner un nom
au site (par exemple « SAE2.01 Alwaysdata ») puis renseigner les paramètres fournis par
l'enseignant:
Champ  Valeur
Protocole  SFTP – SSH File Transfer Protocol
Hôte  ssh-sae204.alwaysdata.net
## Page 3

Port  22
Type d'authentification  Demander le mot de passe
Utilisateur  sae204
Mot de passe  identique au compte Alwaysdata
(communiqué par l'enseignant)

Cliquer sur « Connexion ». À la toute première connexion, FileZilla affiche un avertissement sur
la clé de l'hôte (la signature du serveur): c'est normal. Cocher « Toujours faire confiance à cet
hôte » puis valider. Cet avertissement n'apparaîtra plus ensuite.
Gestionnaire de sites ou Connexion rapide -
La barre « Connexion rapide » (en haut) permet de se connecter en une fois, mais n'enregistre
rien durablement. Le Gestionnaire de sites mémorise la configuration: vous la retrouverez à
chaque ouverture de FileZilla, sans tout retaper. Préférez -le.

## 4. Comprendre l'interface

Une fois connecté, la fenêtre de FileZilla se lit en trois zones:
Zone  Rôle
Panneau de GAUCHE  « Site local »: les fichiers de VOTRE
ordinateur.
Panneau de DROITE  « Site distant »: les fichiers du SERVEUR
Alwaysdata.
Bande du BAS  La file d'attente: la liste des transferts en
cours et terminés.

Dans chaque panneau, la partie haute montre l'arborescence des dossiers, la partie basse le
contenu du dossier sélectionné. Pour naviguer: double -cliquer sur un dossier pour entrer
dedans, et utiliser la ligne «.. » en haut de la liste pour remonter d'un niveau.
## 5. Aller dans le dossier de votre équipe

Dans le panneau de DROITE (le serveur), naviguer jusqu'au dossier racine des sites web:
/www/
Le sous-dossier de votre équipe, nommé sae201_XX (XX = votre identifiant), y a déjà été créé
par l'enseignant. Double-cliquer dessus pour entrer dedans: c'est là, et uniquement là, que vous
déposerez vos fichiers.
## Page 4

⚠  COMPTE PARTAGÉ — NE TOUCHEZ QUE VOTRE DOSSIER  ⚠
Toutes les équipes se connectent avec les MÊMES identifiants: le panneau de droite
affiche donc aussi les dossiers des autres équipes. N'ouvrez pas, ne modifiez pas, ne
supprimez pas un dossier qui n'est pas le vôtre — vous écraseriez le travail d'une autre
équipe. En cas de doute sur votre identifiant XX, demandez à l'enseignant AVANT d'agir.

## 6. Transférer les fichiers (glisser -déposer)

Le transfert se fait par simple glisser -déposer d'un panneau à l'autre:
## 1. Dans le panneau de GAUCHE, naviguer jusqu'au dossier de votre projet.

## 2. Sélectionner les fichiers et dossiers à envoyer (voir la section 7 pour les exclusions).

## 3. Les faire glisser vers le panneau de DROITE, dans votre dossier /www/sae201_XX/.

## 4. Surveiller la file d'attente en bas: attendre que tout soit en « Transferts réussis ».

Dans quel sens se fait le transfert -
De GAUCHE vers DROITE (local → serveur) = envoyer / mettre en ligne: c'est ce que vous
ferez pour déployer. De DROITE vers GAUCHE (serveur → local) = télécharger: utile pour
récupérer un fichier depuis le serveur. Le sens dépend simplement de la direction du glisser -
déposer.

## 7. Exclure les fichiers inutiles ou sensibles

Certains fichiers ne doivent JAMAIS être envoyés sur le serveur. Pour les exclure
automatiquement, créer un filtre: menu Affichage → Filtres de fichiers et de dossiers →
Nouveau filtre. Y ajouter les éléments suivants:
À exclure  Pourquoi
`.env  Contient le mot de passe MySQL: il ne doit`
jamais se retrouver en ligne. Les variables
sont redéfinies côté serveur.
venv/  L'environnement virtuel est recréé
directement sur le serveur (il est propre à
chaque machine).
__pycache__/ et *.pyc  Fichiers de cache générés par Python, inutiles
sur le serveur.
.git/  L'historique Git n'a pas sa place en
production.
## Page 5

Pourquoi un filtre plutôt qu'une sélection manuelle -
Une fois le filtre activé, FileZilla masque ces fichiers: impossible de les transférer par erreur,
`même en sélectionnant tout. C'est surtout une sécurité pour le fichier.env, qui ne doit jamais`
être exposé.

## 8. Mettre à jour après une modification

Chaque fois que vous modifiez un fichier en local, il faut le re -transférer pour que le serveur
prenne en compte le changement. En glissant à nouveau un fichier déjà présent, FileZilla
demande quoi faire: choisir « Écraser » (Remplacer). Vous pouvez cocher « Toujours utiliser
cette action » pour ne plus avoir la question pendant ce transfert.
N'oubliez pas de redémarrer le site
Transférer les fichiers ne suffit pas toujours: après une mise à jour, pensez à redémarrer
votre site depuis le panneau Alwaysdata (Web → Sites → Restart), comme indiqué dans le
tutoriel #3.

## 9. En cas de problème

Symptôme  Piste à vérifier
Connexion impossible / délai dépassé  Vérifier le protocole (SFTP), l'hôte (ssh -
sae204.alwaysdata.net) et le port (22), ainsi
que votre connexion Internet.
Identifiants refusés  Re-saisir l'utilisateur et le mot de passe
fournis par l'enseignant (attention aux
espaces et à la casse).
« Permission denied » à l'envoi  Vous n'êtes probablement pas dans votre
dossier /www/sae201_XX/: replacez -vous
dedans avant de transférer.
`Le.env est parti sur le serveur  Le supprimer côté serveur immédiatement,`
puis activer le filtre d'exclusion (section 7).
Certains fichiers échouent  Le fichier est peut -être ouvert/verrouillé. Le
fermer, puis relancer le transfert depuis la file
d'attente.

✦  ✦  ✦
## Audit du projet - 2026-06-21

- [x] Le projet contient les fichiers ? transf?rer : `app.py`, `wsgi.py`, `config.py`, `requirements.txt`, `controllers/`, `models/`, `services/`, `templates/`, `static/`.
- [x] `.gitignore` exclut les ?l?ments sensibles ou inutiles : `.env`, `.git/`, `venv/`, `.vscode/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `data/sae201_local.db`.
- [x] `requirements.txt` est pr?sent et contient les d?pendances n?cessaires au serveur.
- [x] `wsgi.py` est pr?sent pour le d?ploiement Alwaysdata.
- [x] Les variables MySQL locales sont configur?es dans `.env`, mais ce fichier ne doit pas ?tre transf?r?.
- [x] Test sous-dossier effectu? avec `SCRIPT_NAME=/sae201_b6` : les liens g?n?r?s par Flask sont bien pr?fix?s.
- [ ] Installation de FileZilla non v?rifi?e depuis cette session.
- [ ] Connexion SFTP ? `ssh-sae204.alwaysdata.net` non v?rifi?e depuis cette session.
- [ ] Transfert vers `/www/sae201_b6/` non effectu? depuis cette session.
- [ ] Red?marrage du site Alwaysdata non effectu? depuis cette session.
