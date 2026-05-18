from dotenv import load_dotenv
import os
from pathlib import Path
from sqlalchemy import create_engine

def connexion():
    load_dotenv(Path(__file__).parent / "config" / ".env")

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")

    url = f"mysql+pymysql://{user}:{password}@{host}/{database}"

    engine = create_engine(url)

    try:
        with engine.connect() as connection:
            print("Connexion réussie !")
    except Exception as e:
        print("Échec de la connexion.", e)
        return None
    
    return engine