import requests
from sqlalchemy.orm import sessionmaker

from connexion import engine
from models_dimensions import TypeExercice, TypeSecteur


BASE_URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"