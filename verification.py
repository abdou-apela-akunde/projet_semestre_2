from connexion import connexion
from sqlalchemy.orm import sessionmaker
from models_dimensions import *

engine = connexion()

if engine:
    session = sessionmaker(bind=engine)

    print("=== Contenu de la base ===") 
    print(f"Régions          : {session.query(Region).count():>4}  (attendu : ~18)") 
    print(f"Départements     : {session.query(Departement).count():>4}  (attendu : ~101)") 
    print(f"Professions      : {session.query(ProfessionSante).count():>4}  (attendu : ~32)") 
    print(f"Tranches d’âge  : {session.query(TrancheAge).count():>4}  (attendu : ~8)") 
    print(f"Sexe             : {session.query(Sexe).count():>4}  (attendu : ~3)") 
    print(f"Types exercice   : {session.query(TypeExercice).count():>4}  (attendu : ~5)") 
    print(f"Secteurs conv.   : {session.query(TypeSecteur).count():>4}  (attendu :  4)") 
    print(f"Types honoraires : {session.query(TypeHonoraire).count():>4}  (attendu : ~20)") 
    print(f"Types prescription: {session.query(TypePrescription).count():>4}  (attendu : ~10)") 
    
    # Test de la hiérarchie région -> département 
    print("\n=== Départements d’Île-de-France ===") 
    idf = session.query(Region).filter(Region.libelle == "Île-de-France").first() 
    if idf: 
        for dept in idf.departements: 
            print(f"  {dept.code} – {dept.libelle}") 
    
    session.close()