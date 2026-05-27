from connexion import connexion
from models_dimensions import Base

engine = connexion()

if engine:
    Base.metadata.create_all(engine)
    print("Tables créées :")
    for t in Base.metadata.tables:
        print(f"  ✓ {t}")