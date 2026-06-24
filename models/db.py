"""Connexion SQLAlchemy et initialisation de la base locale."""

import ast
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from models.dimensions import (
    Base,
    Departement,
    ProfessionSante,
    Region,
    Sexe,
    TrancheAge,
    TypeExercice,
    TypeHonoraire,
    TypePrescription,
    TypeSecteur,
)


engine = create_engine(Config.db_url(), pool_recycle=3600)
Session = sessionmaker(bind=engine)


MODEL_BY_TABLE = {
    "region": Region,
    "departement": Departement,
    "profession_sante": ProfessionSante,
    "sexe": Sexe,
    "tranche_age": TrancheAge,
    "type_exercice": TypeExercice,
    "type_honoraire": TypeHonoraire,
    "type_prescription": TypePrescription,
    "type_secteur": TypeSecteur,
}


def init_database():
    """Prépare la base locale SQLite utilisée quand aucun .env MySQL n'est configuré."""
    if not Config.db_url().startswith("sqlite"):
        return

    Base.metadata.create_all(engine)
    session = Session()
    try:
        if session.query(Region).first():
            return
        _seed_sqlite(session)
        session.commit()
    finally:
        session.close()


def _seed_sqlite(session):
    """Importe les donnees de reference du fichier SQL dans SQLite."""
    sql_path = Config.SEED_SQL_PATH
    if not sql_path.exists():
        return

    contenu = sql_path.read_text(encoding="utf-8")
    motif = re.compile(
        r"INSERT INTO `(?P<table>[^`]+)` \((?P<cols>.*?)\) VALUES\s*(?P<values>.*?);",
        re.S,
    )

    for match in motif.finditer(contenu):
        table = match.group("table")
        modele = MODEL_BY_TABLE.get(table)
        if not modele:
            continue

        colonnes = [c.strip(" `") for c in match.group("cols").split(",")]
        valeurs_sql = match.group("values").replace("NULL", "None")
        lignes = ast.literal_eval(f"[{valeurs_sql}]")

        for ligne in lignes:
            donnees = dict(zip(colonnes, ligne))
            session.merge(modele(**donnees))
