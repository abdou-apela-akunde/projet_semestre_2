import requests
from sqlalchemy.orm import sessionmaker

from connexion import engine
from models_dimensions import TypeExercice, TypeSecteur


BASE_URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"

def recuperer_valeurs_distinctes(dataset_id, champ):
    url = f"{BASE_URL}/{dataset_id}/records"

    params = {
        "select": champ,
        "group_by": champ,
        "limit": 100
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])

def ajouter_types_exercice(session):
    dataset_id = "demographie-exercices-liberaux"
    champ = "libelle_type_exercice_liberal"

    resultats = recuperer_valeurs_distinctes(dataset_id, champ)

    for ligne in resultats:
        libelle = ligne.get(champ)

        if libelle:
            existe = session.query(TypeExercice).filter_by(libelle=libelle).first()

            if not existe:
                session.add(TypeExercice(libelle=libelle))

    session.commit()
    print("Types d'exercice ajoutés.")
