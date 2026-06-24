# SAE201 - Annexe 1 - Cache

Source : `SAE201-Annexe1-Cache.pdf`

## Contenu extrait

## Page 1

SAE 2.01 – Annexe 1
Mettre en place un cache
Du simple dictionnaire au patron de conception « Décorateur »

BUT Informatique  ·  IUT de Créteil -Vitry  ·  Département Informatique

## Objectif de cette annexe

Cette annexe prolonge la section 9.2 du document technique. Elle explique, de manière
progressive et accessible, comment implémenter un système de cache pour les appels à l'API
ameli.fr. L'occasion de découvrir deux notions nouvelles: les décorateurs Python et le patron
de conception Décorateur (sans avoir besoin de connaissances préalables sur les design
patterns).

## Page 2

## 1. Pourquoi mettre en place un cache -

1.1 Le problème
Chaque fois que votre application appelle l'API ameli.fr, trois choses coûteuses se produisent:
• un aller -retour réseau entre votre application et les serveurs d'Alwaysdata / ameli.fr,
• un temps de traitement côté serveur distant pour calculer la réponse,
• la bande passante nécessaire pour transférer la réponse JSON.
Résultat typique: une requête API met entre 200 millisecondes et quelques secondes. Si
l'utilisateur rafraîchit la page ou demande deux fois la même information, on refait tout le
travail pour rien.
1.2 Le principe du cache
Un cache est simplement une mémoire temporaire: quand l'application reçoit une réponse de
l'API, elle la garde sous le coude. Si la même question est posée à nouveau quelques secondes
ou minutes plus tard, on renvoie la réponse stockée sans refaire l'appel réseau.
Un cache utile se définit par trois caractéristiques
1) Une clé qui identifie la requête (profession + département + année…). 2) Une valeur (la
réponse de l'API). 3) Une durée de vie au -delà de laquelle la valeur est considérée comme
périmée et doit être rafraîchie.

## 2. Première approche: un cache manuel

Avant d'introduire des concepts avancés, commençons par une implémentation simple et lisible.
On va stocker les réponses dans un dictionnaire Python, et associer à chaque entrée un
horodatage pour gérer l'expiration.
2.1 Une classe Cache dédiée
services/cache.py
"""Cache simple en mémoire avec durée de vie."""

import time

class Cache:
def __init__(self, duree_vie_seconde=300):
self._duree = duree_vie_seconde
self._entrees = {}   # {cle: (valeur, horodatage)}

def get(self, cle):
"""Retourne la valeur si présente et pas expirée, None sinon."""
if cle not in self._entrees:
return None
## Page 3

valeur, horodatage = self._entrees[cle]
if time.time() - horodatage > self._duree:
# Entrée expirée, on la retire
del self._entrees[cle]
return None
return valeur

def set(self, cle, valeur):
self._entrees[cle] = (valeur, time.time())
2.2 Utilisation directe dans AmeliAPI
Il suffit ensuite de modifier la classe AmeliAPI pour qu'elle consulte le cache avant de faire un
appel réseau:
class AmeliAPI:
def __init__(self, timeout=10):
self._timeout = timeout
self._session = requests.Session()
self._cache   = Cache(duree_vie_seconde=300)  # 5 minutes

def get_effectifs(self, profession, departement_code, annee):
cle = f"effectifs:{profession}:{departement_code}:{annee}"

# 1. Regarder dans le cache
valeur = self._cache.get(cle)
if valeur is not None:
return valeur

# 2. Sinon, appel API + stockage
resultat = self._requete(...)  # comme avant
self._cache.set(cle, resultat)
return resultat
Ça marche, mais...
Ce code fonctionne. Mais si on a 10 méthodes (get_effectifs, get_honoraires,
get_patientele…), il faut répéter les 5 lignes « vérifier cache / appeler / stocker » dans
chacune. C'est lourd, répétitif, et sujet aux erreurs. Peut -on faire mieux -

## Page 4

## 3. Les décorateurs Python

3.1 Qu'est -ce qu'un décorateur -
Un décorateur Python est une fonction qui en enveloppe une autre pour lui ajouter un
comportement, SANS modifier son code. On l'applique avec la syntaxe @.
## Exemple simple: mesurer le temps d'exécution d'une fonction.

import time

def chronometrer(fonction):
"""Décorateur qui affiche le temps d'exécution de la fonction."""
def enveloppe(*args, **kwargs):
debut = time.time()
resultat = fonction(*args, **kwargs)
duree = time.time() - debut
print(f"{fonction.__name__} a pris {duree:.3f}s")
return resultat
return enveloppe

@chronometrer
def calculer_somme(n):
return sum(range(n))

calculer_somme(1_000_000)
# Affiche: calculer_somme a pris 0.043s
Ce qui se passe, pas à pas:
## 1. La syntaxe @chronometrer au -dessus de calculer_somme équivaut à écrire calculer_somme

= chronometrer(calculer_somme).
## 2. Le décorateur reçoit la fonction originale, la garde en mémoire, et renvoie une NOUVELLE

fonction (ici enveloppe) qui sait faire le chronométrage avant et après l'appel.
## 3. Quand on appelle calculer_somme(...) dans le reste du code, on appelle en réalité

l'enveloppe: elle démarre le chrono, appelle la fonction d'origine, affiche la durée, et
renvoie le résultat.
L'idée clé
Un décorateur ajoute un comportement AUTOUR d'une fonction (avant l'appel, après l'appel,
ou les deux). La fonction d'origine n'est pas modifiée: on la rend juste plus intelligente de
l'extérieur.

3.2 Un décorateur @cache
On peut maintenant écrire un décorateur dédié à la mise en cache. Il prend une méthode, et
renvoie une version qui mémorise ses résultats.
## Page 5

services/cache.py (suite)
import time
from functools import wraps

def avec_cache(duree_vie_seconde=300):
"""Décorateur: mémorise le résultat d'une méthode pendant N secondes."""
def decorateur(methode):
memoire = {}  # {cle: (valeur, horodatage)}

@wraps(methode)
def enveloppe(self, *args):
cle = (methode.__name__,) + args
if cle in memoire:
valeur, horodatage = memoire[cle]
if time.time() - horodatage <= duree_vie_seconde:
return valeur
resultat = methode(self, *args)
memoire[cle] = (resultat, time.time())
return resultat

return enveloppe
return decorateur
@wraps(methode) -
functools.wraps copie le nom et la documentation de la méthode d'origine sur l'enveloppe.
Sans cela, une fonction décorée perdrait son nom et ses informations internes. C'est un
réflexe à adopter systématiquement quand on écrit un décorateur.

3.3 Utilisation dans AmeliAPI
from services.cache import avec_cache

class AmeliAPI:
#...

@avec_cache(duree_vie_seconde=300)
def get_effectifs(self, profession, departement_code, annee):
return self._requete(...)  # code inchangé

@avec_cache(duree_vie_seconde=300)
def get_honoraires(self, profession, departement_code, annee):
return self._requete(...)

@avec_cache(duree_vie_seconde=600)
def get_evolution_effectifs(self, profession, departement_code):
return self._requete(...)
## Page 6

C'est tout! Chaque méthode décorée bénéficie automatiquement du cache, avec sa propre
durée de vie, sans aucune duplication de code. Si on veut désactiver le cache plus tard, il suffit
de retirer la ligne @avec_cache — la méthode continue de fonctionner.
Le bénéfice concret
On est passé de « 5 lignes de logique cache répétées dans chaque méthode » à « 1 ligne
@avec_cache(…) ». C'est plus lisible, plus fiable, et plus simple à faire évoluer (on peut
améliorer le cache sans toucher aux méthodes).

## Page 7

## 4. Le patron de conception « Décorateur »

4.1 Qu'est -ce qu'un patron de conception -
Un patron de conception (ou design pattern en anglais) est une recette éprouvée pour résoudre
un problème récurrent dans la conception de programmes. Ce ne sont pas des bouts de code à
copier, mais des structures que l'on reconnaît et que l'on adapte à son propre projet.
Les patrons de conception ont été répertoriés dans un livre célèbre (le « Gang of Four » ou GoF,
1994). Parmi les plus connus: Singleton, Observateur, Fabrique, Stratégie… et le patron
Décorateur.
4.2 Le patron Décorateur en pratique
Le patron Décorateur consiste à enrober un objet dans un autre qui ajoute une fonctionnalité,
tout en respectant la même interface. Dit autrement: on emballe un objet dans un « cadeau »
qui se comporte comme lui, mais avec une capacité supplémentaire.
Appliqué à notre cas: au lieu de modifier la classe AmeliAPI, on crée une nouvelle classe
CachedAmeliAPI qui contient une AmeliAPI et lui ajoute le cache. Vu de l'extérieur, les deux
classes ont les mêmes méthodes.
services/cached_ameli_api.py
import time

from services.ameli_api import AmeliAPI

class CachedAmeliAPI:
"""Enveloppe une AmeliAPI pour ajouter un cache aux méthodes."""

def __init__(self, api_sous_jacente, duree_vie_seconde=300):
self._api = api_sous_jacente       # l'objet « décoré »
self._duree = duree_vie_seconde
self._memoire = {}

def get_effectifs(self, profession, departement_code, annee):
cle = ("effectifs", profession, departement_code, annee)
return self._lire_ou_calculer(
cle, lambda: self._api.get_effectifs(profession, departement_code,
annee)
)

def get_honoraires(self, profession, departement_code, annee):
cle = ("honoraires", profession, departement_code, annee)
return self._lire_ou_calculer(
cle, lambda: self._api.get_honoraires(profession, departement_code,
annee)
)
## Page 8

def _lire_ou_calculer(self, cle, produire):
if cle in self._memoire:
valeur, ts = self._memoire[cle]
if time.time() - ts <= self._duree:
return valeur
resultat = produire()
self._memoire[cle] = (resultat, time.time())
return resultat
4.3 Comment ça s'utilise -
from services.ameli_api import AmeliAPI
from services.cached_ameli_api import CachedAmeliAPI

# On enveloppe l'API brute dans son décorateur
api = CachedAmeliAPI(AmeliAPI())

# Ensuite, on l'utilise exactement de la même façon
resultats = api.get_effectifs("Médecin généraliste", "75", 2023)
Principe de substitution
Le contrôleur Flask ne voit pas la différence entre AmeliAPI et CachedAmeliAPI: les deux
offrent les mêmes méthodes. On pourra même en chaîner plusieurs plus tard (par exemple un
LoggedAmeliAPI qui journalise les appels et englobe CachedAmeliAPI). C'est toute la force du
pattern.

4.4 Décorateurs Python vs patron Décorateur
Les deux approches présentées dans cette annexe partagent le même esprit: ajouter une
fonctionnalité sans modifier le code d'origine. Mais elles se distinguent sur le plan technique:
Critère  Décorateur Python (@)  Patron Décorateur (OOP)
Niveau  Fonction / méthode
individuelle  Classe entière
Complexité  Faible, concis  Plus verbeux mais plus
souple
Chaînabilité  Oui (plusieurs @ empilables)  Oui (imbriquer les objets)
Cas d'usage idéal  Ajouter un comportement
ciblé à une méthode  Varier les comportements
d'objets à l'exécution

Pour votre projet, les deux solutions sont valides. L'approche à décorateur Python est suffisante
et plus concise. L'approche à patron Décorateur est un excellent exercice pour comprendre la
POO avancée.
## Page 9

## 5. Pour aller plus loin

5.1 Forcer le rafraîchissement du cache
Parfois, on veut ignorer le cache et forcer un nouvel appel (par exemple sur un bouton «
Rafraîchir »). Deux approches possibles:
• ajouter un paramètre rafraichir=False aux méthodes: si rafraichir=True, on saute la lecture
du cache;
• exposer une méthode vider_cache() qui efface toutes les entrées mémorisées.
5.2 Un cache partagé entre utilisateurs
Le cache présenté ici vit dans la mémoire du processus: chaque utilisateur bénéficie
uniquement de ses propres appels précédents. Pour un vrai cache partagé, on utilise
généralement Redis ou Memcached. C'est un sujet pour plus tard (2ème année).
5.3 La bibliothèque functools.lru_cache
Python fournit en standard un décorateur de cache prêt à l'emploi: functools.lru_cache. Il limite
automatiquement la taille du cache (politique « Least Recently Used »). Inconvénient: il ne gère
pas la durée de vie. À connaître, mais pas adapté tel quel pour une API qui renvoie des données
évolutives.
from functools import lru_cache

class AmeliAPI:
@lru_cache(maxsize=128)
def get_effectifs(self, profession, departement_code, annee):
...
5.4 Mesurer l'effet du cache
Pour illustrer l'intérêt du cache dans votre soutenance, chronométrez deux appels identiques:
le premier déclenchera un appel réseau (≈ 500ms), le second devra revenir en quelques
microsecondes. C'est une démonstration très parlante de la valeur ajoutée.
import time

t = time.time(); api.get_effectifs("...", "75", 2023); print(time.time() - t)
# 1er appel: ~0.5s

t = time.time(); api.get_effectifs("...", "75", 2023); print(time.time() - t)
# 2e appel: ~0.00002s
En résumé
Le cache n'est pas un gadget: c'est une technique classique d'optimisation qui transforme une
application lente en application réactive, sans coût supplémentaire pour l'API. Il se prête très
bien à deux concepts importants:
## Page 10

• Les décorateurs Python, qui permettent d'ajouter un comportement autour d'une méthode
sans toucher à son code.
• Le patron de conception Décorateur, qui consiste à enrober un objet dans un autre qui
ajoute une fonctionnalité tout en respectant la même interface.
Implémenter l'une de ces deux approches dans votre projet est un vrai plus pour la soutenance:
vous montrez que vous avez compris comment factoriser du code répétitif et vous introduisez
un vocabulaire de conception que vous réutiliserez tout au long de votre formation.

✦  ✦  ✦
## Audit du projet - 2026-06-21

- [x] `services/cache.py` contient un d?corateur `avec_cache(duree_vie_seconde=...)` bas? sur un dictionnaire m?moire et un horodatage.
- [x] Le d?corateur utilise `functools.wraps`, comme recommand? dans l'annexe.
- [x] Les entr?es expir?es sont supprim?es quand leur dur?e de vie est d?pass?e.
- [x] `services/ameli_api.py` applique `@avec_cache` sur `get_effectifs()` et `get_evolution_effectifs()`.
- [x] Le cache fonctionne avec les arguments positionnels et nomm?s, ce qui couvre les filtres optionnels `sexe` et `age`.
- [x] `services/cached_ameli_api.py` impl?mente aussi le patron D?corateur orient? objet autour d'une API compatible.
- [x] `CachedAmeliAPI` expose `get_effectifs()`, `get_evolution_effectifs()`, `derniere_erreur` et `vider_cache()`.
- [x] Test local effectu? : deux appels identiques via `CachedAmeliAPI` ne d?clenchent qu'un seul appel ? l'API sous-jacente.
- [x] `scripts/benchmark_cache.py` permet de mesurer un premier appel puis un second appel identique.
- [ ] Cache partag? Redis/Memcached non impl?ment?, mais l'annexe le pr?sente comme une piste avanc?e pour plus tard.
