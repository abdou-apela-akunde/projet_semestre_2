# Présentation orale - DataSanté

Durée visée : environ 10 minutes.  
La démonstration du site est placée à la fin.

## Personne 1 : introduction et contexte

Bonjour, nous allons vous présenter DataSanté, notre projet de SAE 2.01.

DataSanté est une application web développée avec Flask. Son objectif est de rendre plus lisibles des données de santé en France, en particulier les effectifs de professionnels de santé, les densités, les honoraires, les prescriptions et certaines données liées aux pathologies.

Le projet s'appuie sur deux sources principales. La première est la base de données construite en SAE 2.04, qui contient les dimensions de référence : régions, départements, professions de santé, tranches d'âge, sexes, types d'honoraires et postes de prescription. La deuxième source est l'API publique Data Ameli, qui fournit les valeurs chiffrées utilisées dans les tableaux et les graphiques.

Nous avons organisé le projet selon une architecture MVC adaptée à Flask. Les modèles sont dans le dossier `models`, les routes dans `controllers`, les services dans `services`, les pages HTML dans `templates`, et les fichiers CSS, JavaScript et GeoJSON dans `static`.

Cette organisation correspond au tutoriel 1 : l'application Flask est structurée, les blueprints séparent les routes, SQLAlchemy gère la connexion à la base, et la page d'accueil est alimentée par les données de référence.

Notre objectif n'était pas seulement d'afficher des données brutes, mais de permettre à un utilisateur de faire une recherche, de comprendre les résultats rapidement, puis de les comparer ou de les exporter.

## Personne 2 : données, API et pipeline

Je vais maintenant expliquer la partie données.

Au démarrage, l'application lit la configuration dans le fichier `.env`. Si les identifiants MySQL sont présents, elle se connecte à la base SAE 2.04 sur Alwaysdata. Sinon, elle utilise une base SQLite locale créée à partir du fichier `data/sae204_ideal.sql`. Cela permet de lancer le projet même sans accès immédiat à la base distante.

Les tables de dimensions servent à remplir les menus de sélection. Par exemple, les régions et les départements viennent de la base, tout comme les professions de santé et les postes de prescription. Cela évite d'écrire ces listes en dur dans les templates.

Les données chiffrées ne sont pas stockées localement. Elles sont récupérées à la demande depuis Data Ameli grâce au service `AmeliAPI`. Ce service centralise les appels HTTP, construit les filtres de recherche, nettoie les valeurs reçues et renvoie des listes de résultats exploitables par les routes Flask.

Pour limiter les appels répétés, nous avons ajouté un cache mémoire. Si une même recherche est relancée rapidement, l'application peut réutiliser la réponse déjà obtenue au lieu d'interroger à nouveau l'API.

Le pipeline est donc le suivant : l'utilisateur choisit ses filtres, JavaScript envoie une requête à une route `/api`, Flask vérifie les paramètres, interroge Data Ameli, prépare les données, puis renvoie du JSON. Le navigateur met ensuite à jour les KPI, les tableaux et les graphiques.

Cette partie répond au tutoriel 2 : formulaire dynamique, cascade région vers département, appel API, affichage d'un tableau et d'un graphique.

## Personne 3 : pages et fonctionnalités

Je vais présenter les principales pages de l'application.

La page d'accueil regroupe les critères de recherche directement sur la première page. On peut choisir une profession, une région entière ou un département, puis une année. La carte interactive permet aussi de sélectionner un territoire. Les vues sous la carte s'actualisent avec les filtres : effectif, densité, variation annuelle, variation en pourcentage, moyenne, graphique d'évolution et tableaux.

La page Indicateurs présente une synthèse du projet : nombre de régions, départements, professions, postes de prescription et période exploitable. Elle sert de vue générale sur les référentiels disponibles.

La page Comparaisons permet de comparer deux séries. Chaque série peut avoir sa profession, sa région, son département et sa période. La page affiche un histogramme du dernier point disponible, une courbe d'évolution, une répartition par sexe, une répartition par âge, ainsi qu'un tableau année par année.

Les pages Prescriptions et Honoraires fonctionnent sur le même principe. L'utilisateur choisit une profession, un type de donnée, un territoire et une période. L'application affiche ensuite le montant total, le montant moyen, une évolution annuelle et un tableau exportable.

La page Pathologies remplace l'ancienne page Secteurs. Elle permet de choisir une pathologie, un territoire et une période. Elle affiche le nombre de personnes concernées, la prévalence, un graphique et un tableau.

Tous les tableaux peuvent être triés par colonne et téléchargés en CSV. Cela rend l'application plus utile pour analyser les résultats en dehors du site.

## Personne 4 : conformité, déploiement et bilan

Je vais terminer la partie technique avant la démonstration.

Pour le tutoriel 3, le projet contient un fichier `requirements.txt` avec les dépendances nécessaires, ainsi qu'un fichier `wsgi.py` qui expose la variable `application`, attendue par Alwaysdata.

Les informations sensibles ne sont pas écrites dans le code. Le fichier `.env` existe seulement en local et il est ignoré par Git, car il contient les vrais identifiants de la base. Les URLs internes sont générées avec `url_for`, ce qui permet au site de fonctionner même s'il est déployé dans un sous-dossier comme `/sae201_b6/`.

Nous avons aussi prévu des pages d'erreur claires pour les erreurs 404 et 500. Si l'API Data Ameli ne renvoie pas de données, l'interface affiche un message au lieu de bloquer complètement la navigation.

Le projet a quelques limites. Il dépend de la disponibilité de Data Ameli, et certaines combinaisons de filtres ne donnent pas de résultat parce que les données n'existent pas dans l'API. En revanche, la structure permet d'ajouter facilement d'autres pages ou d'autres jeux de données.

En résumé, DataSanté respecte les trois tutoriels : structure Flask et base de données pour le tutoriel 1, formulaires et API pour le tutoriel 2, préparation au déploiement pour le tutoriel 3. Nous avons ajouté des améliorations utiles : carte interactive, comparaisons, export CSV, page pathologies et vues plus détaillées.

## Démonstration du site

Nous passons maintenant à la démonstration.

Personne 1 :

Je lance l'application avec la commande `python app.py`, puis j'ouvre l'adresse locale `http://127.0.0.1:5000`.

Sur la page d'accueil, je sélectionne une profession de santé, par exemple les médecins, puis une région. Je peux choisir toute la région ou préciser un département. La carte se synchronise avec les filtres : si je clique sur un département, le formulaire se met à jour automatiquement.

Je montre ensuite les vues sous la carte : effectif, densité, variation annuelle, variation en pourcentage, effectif moyen, graphique d'évolution et historique complet. Les années affichées sont limitées à la période disponible, de 2015 à 2023.

Personne 2 :

Je vais maintenant sur la page Indicateurs. Cette page résume les données disponibles : nombre de territoires, professions, postes de prescription, types d'honoraires et période analysable.

Ensuite, j'ouvre la page Comparaisons. Je configure deux séries, par exemple une même profession dans deux régions différentes. Je lance la comparaison. On obtient un histogramme, une courbe d'évolution, une répartition par sexe, une répartition par âge, et un tableau année par année.

Personne 3 :

Je présente maintenant la page Prescriptions. Je choisis une profession, un poste de prescription, une région ou un département, puis une plage d'années. Après validation, l'application affiche le montant prescrit total, le montant moyen, un graphique d'évolution et un tableau.

Je montre aussi que le tableau est triable : on peut cliquer sur une colonne pour inverser l'ordre. On peut également télécharger les résultats en CSV.

Personne 4 :

Je continue avec la page Honoraires. Le fonctionnement est similaire : je choisis une profession, un type d'honoraire, un territoire et une période. Les résultats affichent les montants totaux et moyens avec un graphique clair.

Enfin, je vais sur la page Pathologies. Je sélectionne une pathologie, une région ou un département, puis une période. L'application affiche le nombre de personnes concernées, la prévalence, l'évolution annuelle et le tableau correspondant.

Il n'y a pas de page admin, d'inscription ou de connexion dans notre application, car les consignes et le besoin du projet portent sur la consultation de données publiques. Nous terminons donc la démonstration avec la page À propos, qui rappelle le contexte, les membres du groupe, les technologies et les sources de données.

Merci pour votre attention.
