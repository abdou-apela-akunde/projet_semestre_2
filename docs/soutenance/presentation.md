# Script de soutenance - DataSante

Projet : SAE 2.01 - Developpement d'une application web  
Sujet : DataSante, exploration et comparaison de donnees de sante francaises  
Duree totale visee : 15 minutes  
Repartition : 10 minutes de presentation + 5 minutes de demonstration  
Groupe :

- ALLOUNE Abdelwadoud
- APELA AKUNDE Abdou
- BERRICHE Djibril
- WASEL Yassine

## Objectif du document

Ce document sert de support oral pour la soutenance. Il est construit pour suivre le diaporama DataSante : page de garde, contexte, objectifs, architecture, donnees, interface, fonctionnalites, bilan, puis demonstration.

La partie orale doit durer environ 10 minutes. La demonstration doit ensuite durer environ 5 minutes. Le texte ci-dessous peut etre appris tel quel ou utilise comme base pour une presentation plus naturelle.

## Repartition globale

| Partie | Intervenant | Duree |
| --- | --- | --- |
| Introduction, contexte et objectifs | ALLOUNE Abdelwadoud | 2 min 30 |
| Architecture, base et API | APELA AKUNDE Abdou | 2 min 30 |
| Interface, pages et visualisations | BERRICHE Djibril | 2 min 30 |
| Conformite, bilan et transition demo | WASEL Yassine | 2 min 30 |
| Demonstration de l'application | Groupe complet | 5 min |

---

# Partie 1 - Introduction, contexte et objectifs

Intervenant : ALLOUNE Abdelwadoud  
Duree visee : 2 min 30  
Diapositives concernees : page de garde, contexte, objectifs

Bonjour, nous allons vous presenter notre projet de SAE 2.01 : DataSante.

DataSante est une application web developpee avec Flask. Son objectif est de rendre plus lisibles et plus exploitables des donnees publiques de sante en France. L'application permet principalement de consulter les effectifs de professionnels de sante, leur densite par territoire, mais aussi d'explorer des donnees d'honoraires, de prescriptions et de pathologies.

Le projet s'inscrit dans la continuite de la SAE 2.04. Dans cette SAE precedente, nous avions travaille sur une base de donnees contenant des tables de dimensions : les regions, les departements, les professions de sante, les sexes, les tranches d'age, les types d'honoraires, les prescriptions et les secteurs. Dans la SAE 2.01, nous reutilisons cette base pour construire une vraie application web.

L'enjeu n'est donc pas seulement d'afficher des donnees. Il faut proposer une interface claire, organiser le projet proprement, suivre une architecture MVC, interroger une API externe et presenter les resultats sous plusieurs formes : KPI, tableaux, graphiques et carte interactive.

Notre application repond a trois grands objectifs.

Premier objectif : permettre a l'utilisateur de filtrer facilement les donnees. Il peut choisir une profession, une region, un departement et une annee ou une periode.

Deuxieme objectif : afficher les resultats de maniere visuelle. Au lieu de montrer uniquement un tableau brut, l'application propose des indicateurs cles, des graphiques Chart.js et une carte interactive de la France.

Troisieme objectif : garder un projet maintenable. Les fichiers sont ranges par role : les routes Flask dans les controleurs, les modeles SQLAlchemy dans les modeles, la logique API dans les services, les vues dans les templates et les fichiers CSS ou JavaScript dans static.

Le nom DataSante resume donc l'idee du projet : transformer des donnees de sante parfois difficiles a lire en une interface plus simple, plus interactive et plus utile pour comparer les territoires.

Transition :

Je vais maintenant laisser la parole a Abdou, qui va presenter l'organisation technique du projet, la base de donnees et le fonctionnement avec l'API Data Ameli.

---

# Partie 2 - Architecture, base de donnees et API

Intervenant : APELA AKUNDE Abdou  
Duree visee : 2 min 30  
Diapositives concernees : stack technique, architecture MVC, pipeline de donnees

Je vais presenter la partie technique de l'application.

Le projet est construit avec Flask, qui est un framework web Python. Nous avons utilise Jinja2 pour les templates HTML, SQLAlchemy pour la connexion aux donnees de reference, JavaScript pour les interactions cote navigateur, Chart.js pour les graphiques et Leaflet pour la carte interactive.

L'application suit une architecture MVC adaptee a Flask.

La partie modele se trouve dans le dossier `models`. Elle contient la configuration de la base et les classes qui representent les tables de dimensions. Ces tables viennent de la SAE 2.04 et permettent de remplir les listes de selection : regions, departements, professions, types de prescriptions, types d'honoraires, etc.

La partie controleur se trouve dans le dossier `controllers`. Elle contient les routes Flask. Certaines routes affichent des pages HTML, par exemple l'accueil, les indicateurs, les comparaisons, les honoraires ou les pathologies. D'autres routes renvoient du JSON pour le JavaScript, notamment les departements d'une region ou les resultats d'une recherche.

La partie vue se trouve dans le dossier `templates`. Les pages utilisent l'heritage Jinja2 avec un fichier principal `base.html`. Cela permet de garder une navbar, un footer et une structure commune sur tout le site.

Nous avons aussi un dossier `services`, qui contient la logique metier. Par exemple, `ameli_api.py` centralise les appels vers l'API Data Ameli. Cela evite de mettre les requetes directement dans les routes Flask.

Concernant les donnees, l'application utilise deux sources.

La premiere source est la base de donnees de la SAE 2.04. Elle sert surtout de referentiel. Cela signifie qu'elle donne les noms, les codes et les relations entre les elements, par exemple une region et ses departements.

La deuxieme source est l'API publique Data Ameli. C'est elle qui fournit les donnees chiffrees : effectifs, densites, honoraires, prescriptions ou pathologies selon les pages.

Le fonctionnement est le suivant : l'utilisateur choisit ses filtres dans l'interface. Le navigateur envoie une requete a Flask. Flask verifie les parametres, construit une requete vers Data Ameli, recupere les donnees, les nettoie, puis renvoie une reponse JSON. Ensuite, JavaScript met a jour les cartes de KPI, les graphiques et les tableaux sans obliger l'utilisateur a changer de page.

Nous avons aussi ajoute un cache memoire. Si une meme recherche est relancee rapidement, l'application peut reutiliser la reponse deja obtenue. Cela limite les appels repetes a l'API et rend l'utilisation plus fluide.

Enfin, le projet est prepare pour le deploiement. Le fichier `requirements.txt` liste les dependances, `wsgi.py` expose l'application pour Alwaysdata et les informations sensibles sont mises dans un fichier `.env`, qui n'est pas versionne sur GitHub.

Transition :

Nous avons donc une base technique organisee. Djibril va maintenant presenter ce que l'utilisateur voit concretement dans l'application : les pages, les graphiques et les fonctionnalites principales.

---

# Partie 3 - Interface, pages et visualisations

Intervenant : BERRICHE Djibril  
Duree visee : 2 min 30  
Diapositives concernees : interface, accueil, carte, pages d'analyse, comparaisons

Je vais maintenant presenter l'interface et les principales fonctionnalites visibles par l'utilisateur.

La page d'accueil est la page centrale de l'application. Elle contient les filtres principaux : profession, region, departement et annee. Elle contient aussi une carte interactive de la France. Cette carte permet de selectionner une region ou un departement directement en cliquant dessus.

Un point important est que la carte et les filtres sont synchronises. Si l'utilisateur choisit une region ou un departement dans le formulaire, la carte se met a jour. Et inversement, si l'utilisateur clique sur la carte, les filtres se remplissent automatiquement. Cela rend la recherche plus intuitive.

Sur la meme page, nous avons ajoute une zone de resultats. Quand aucun filtre n'est selectionne, l'interface affiche des messages de previsualisation, par exemple "Selectionnez une profession", "Selectionnez une region ou un departement" ou "Selectionnez une annee". L'utilisateur comprend donc immediatement quelles informations seront affichees apres une recherche.

Quand les filtres sont remplis, cette zone se met a jour directement sur l'accueil. Elle affiche les KPI principaux, comme l'effectif, la densite, la variation annuelle ou la moyenne sur la periode. Elle affiche aussi un graphique d'evolution et un tableau de donnees.

L'application contient ensuite plusieurs pages specialisees.

La page Indicateurs donne une vue generale du projet. Elle presente des chiffres utiles sur les donnees disponibles : nombre de regions, nombre de departements, nombre de professions, periode exploitable et autres elements de reference.

La page Comparaisons permet de comparer deux ensembles de donnees. L'utilisateur peut choisir des criteres differents pour chaque serie : annee, profession, region, departement et periode. La page affiche ensuite des graphiques complementaires : un graphique pour comparer les valeurs et un autre pour observer l'evolution dans le temps. L'objectif est d'eviter les doublons et de montrer des informations vraiment differentes.

La page Prescriptions permet d'analyser les montants prescrits selon une profession, un poste de prescription, un territoire et une periode. La page Honoraires fonctionne de maniere proche, mais avec les types d'honoraires. La page Pathologies permet d'observer le nombre de personnes concernees et la prevalence d'une pathologie sur un territoire.

Pour toutes ces pages, nous avons cherche a garder une presentation coherente avec la maquette : une interface claire, des blocs bien organises, des graphiques lisibles et des informations importantes mises en avant.

Nous avons aussi ajoute des tableaux triables et des exports CSV. Cela permet a l'utilisateur de recuperer les resultats pour les retravailler dans un tableur si besoin.

Transition :

Je vais maintenant passer la parole a Yassine, qui va conclure sur la conformite avec les consignes, les limites du projet et la preparation de la demonstration.

---

# Partie 4 - Conformite, bilan et transition vers la demonstration

Intervenant : WASEL Yassine  
Duree visee : 2 min 30  
Diapositives concernees : conformite, bilan, demonstration

Je vais terminer la presentation en expliquant comment le projet respecte les consignes et ce que nous avons retenu.

Le premier tutoriel demandait de construire une application Flask avec une organisation claire de type MVC. Dans notre projet, cette structure est bien presente : `models` pour les donnees, `controllers` pour les routes, `templates` pour les vues et `static` pour les fichiers CSS, JavaScript, images et GeoJSON. Les routes sont separees avec des blueprints, ce qui rend le projet plus facile a maintenir.

Le deuxieme tutoriel portait sur les formulaires, l'API et les visualisations. Notre application propose des formulaires dynamiques avec une cascade entre region et departement. Elle interroge l'API Data Ameli avec des routes JSON. Elle affiche les resultats sous forme de tableaux et de graphiques Chart.js. Nous avons aussi ajoute une carte Leaflet, des KPI, des comparaisons et des exports CSV.

Le troisieme tutoriel concernait le deploiement, qui etait presente comme optionnel. Le projet est prepare pour cela avec `requirements.txt`, `wsgi.py`, l'utilisation de variables d'environnement et des chemins generes proprement avec `url_for`. Cela permet de l'adapter a un hebergement comme Alwaysdata.

Nous avons egalement supprime ce qui n'etait pas utile pour le besoin final, comme une page admin. L'application se concentre sur la consultation et l'analyse de donnees publiques. Il n'y a donc pas de connexion obligatoire, car ce n'est pas necessaire pour l'objectif du projet.

Les principales limites viennent des donnees elles-memes. Certaines combinaisons de filtres ne renvoient pas de resultat, car l'API Data Ameli ne contient pas toujours toutes les valeurs pour toutes les professions, tous les territoires ou toutes les annees. L'application gere ce cas en affichant des messages plutot qu'en bloquant.

En bilan, ce projet nous a permis de travailler sur plusieurs competences : structurer une application web, reutiliser une base de donnees, consommer une API externe, creer des interfaces dynamiques, visualiser des donnees et preparer un projet pour GitHub et pour un deploiement.

Nous allons maintenant passer a la demonstration. L'objectif de la demo est de montrer un parcours utilisateur complet : partir de l'accueil, appliquer des filtres, utiliser la carte, consulter les KPI, comparer deux territoires, puis montrer les pages d'analyse complementaires.

---

# Demonstration de l'application

Duree visee : 5 minutes  
Objectif : montrer rapidement que l'application est fonctionnelle, interactive et conforme au diaporama.

## Preparation avant la demo

Avant le passage, verifier que le serveur Flask est lance :

```powershell
python app.py
```

Ouvrir ensuite :

```text
http://127.0.0.1:5000
```

Preparer une recherche simple qui renvoie des donnees, par exemple une profession courante, une region connue et une annee disponible entre 2015 et 2023.

## Demo - minute 0 a 1 : accueil, filtres et carte

Intervenant conseille : ALLOUNE Abdelwadoud

Nous sommes sur la page d'accueil de DataSante. On retrouve directement les filtres principaux en haut de page : profession, region, departement et annee.

Je commence par selectionner une profession. Ensuite, je choisis une region dans le formulaire. On voit que la carte se met a jour et que le territoire selectionne est mis en evidence.

Je peux aussi faire l'inverse : cliquer directement sur une region ou un departement dans la carte. Dans ce cas, les filtres se remplissent automatiquement. Cela montre que la carte et le formulaire sont synchronises dans les deux sens.

Point a montrer :

- selection d'une region depuis le filtre ;
- selection d'un departement depuis la carte ;
- zoom ou deplacement sur la carte si necessaire ;
- panneau de donnees de la region ou du departement selectionne.

## Demo - minute 1 a 2 : resultats dynamiques sur l'accueil

Intervenant conseille : APELA AKUNDE Abdou

Quand les filtres sont appliques, l'utilisateur reste sur la page d'accueil. L'application ne redirige pas vers une autre page. Les resultats apparaissent directement dans la zone de previsualisation.

On voit les KPI principaux, par exemple l'effectif, la densite ou l'evolution. Le graphique permet de visualiser la tendance sur la periode disponible. Le tableau donne le detail des valeurs par annee.

Si aucun filtre n'est choisi, la page affiche des cartes vides avec des messages d'aide. Cela permet de comprendre ce qui sera affiche apres la recherche.

Point a montrer :

- les KPI principaux ;
- le graphique d'evolution ;
- le tableau de resultats ;
- le comportement sans filtre si besoin.

## Demo - minute 2 a 3 : page Comparaisons

Intervenant conseille : BERRICHE Djibril

Je passe maintenant a la page Comparaisons. Cette page permet de comparer deux series de donnees.

Pour chaque serie, on peut choisir une profession, une region ou un departement et une periode. L'interet est de comparer deux territoires ou deux professions avec des criteres differents.

Une fois la comparaison lancee, les graphiques du bas donnent deux lectures complementaires. L'un sert a comparer les valeurs, l'autre montre l'evolution dans le temps. Le tableau permet ensuite de lire les donnees plus precisement.

Point a montrer :

- choix de deux territoires ou deux professions ;
- lancement de la comparaison ;
- lecture rapide des deux graphiques ;
- tableau comparatif.

## Demo - minute 3 a 4 : pages d'analyse

Intervenant conseille : WASEL Yassine

Je montre maintenant les pages d'analyse complementaires.

La page Prescriptions permet d'analyser les montants prescrits selon une profession, un poste de prescription, un territoire et une periode.

La page Honoraires permet d'observer les honoraires ou les depassements selon les criteres disponibles.

La page Pathologies donne une autre approche : on ne regarde plus une profession, mais une pathologie, avec le nombre de personnes concernees et la prevalence.

Ces pages gardent la meme logique d'interface : filtres, indicateurs, graphiques et tableau.

Point a montrer :

- ouvrir rapidement Prescriptions ;
- ouvrir Honoraires ;
- ouvrir Pathologies ;
- insister sur la coherence de l'interface.

## Demo - minute 4 a 5 : export, a propos et conclusion

Intervenant conseille : groupe complet, conclusion par WASEL Yassine

Pour finir, nous montrons que les tableaux peuvent etre tries par colonne et exportes en CSV. C'est utile si l'utilisateur veut continuer l'analyse dans un tableur.

Nous ouvrons ensuite la page A propos. Elle rappelle le nom de la SAE, les membres du groupe, les technologies utilisees, les sources de donnees et l'architecture du projet.

Conclusion orale :

Pour conclure, DataSante est une application Flask complete qui respecte les consignes de la SAE 2.01. Elle reutilise la base de donnees de la SAE 2.04, interroge l'API Data Ameli, affiche des formulaires dynamiques, des graphiques, des tableaux, une carte interactive et des comparaisons. L'objectif etait de rendre les donnees de sante plus lisibles et plus faciles a explorer.

Merci pour votre attention.

---

# Conseils pour tenir les 15 minutes

- Ne pas lire trop vite : viser une parole claire et posee.
- La presentation orale doit durer environ 10 minutes, soit environ 2 min 30 par personne.
- La demo doit rester simple : ne pas multiplier les recherches.
- Si l'API est lente, commenter ce qui est en train de se passer : l'application interroge Data Ameli et met a jour les resultats.
- Prevoir une combinaison de filtres qui fonctionne avant la soutenance.
- Eviter de passer trop de temps sur les details techniques pendant la demo : ils ont deja ete presentes dans les 10 premieres minutes.

# Questions possibles du jury

## Pourquoi utiliser une API au lieu de stocker toutes les donnees ?

Parce que les donnees chiffrees viennent de Data Ameli et peuvent etre consultees a la demande. Cela evite de dupliquer de gros jeux de donnees et garde l'application plus proche des donnees publiques disponibles.

## A quoi sert la base SAE 2.04 ?

Elle sert de referentiel. Elle fournit les listes propres de regions, departements, professions et autres dimensions utilisees dans les formulaires.

## Pourquoi avoir supprime la page admin ?

Le projet porte sur la consultation de donnees publiques. Une page admin, une connexion ou une inscription n'etaient pas necessaires pour repondre au besoin principal.

## Que se passe-t-il si l'API ne renvoie pas de donnees ?

L'application affiche un message indiquant qu'aucune donnee n'est disponible pour les filtres choisis. Cela evite une erreur bloquante pour l'utilisateur.

## Quelles ameliorations seraient possibles ?

On pourrait ajouter un deploiement final verifie sur Alwaysdata, enrichir les tests automatises, ajouter d'autres jeux de donnees Data Ameli et proposer davantage d'exports.
