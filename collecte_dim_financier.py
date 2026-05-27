from sqlalchemy.orm import sessionmaker
from connexion import connexion
from models_dimensions import TypeHonoraire, TypePrescription
from utils_api import collecter_tout

engine = connexion()

if engine:
    Session = sessionmaker(bind=engine)
    session = Session()

    print("=== Collecte types d'honoraires et prescriptions ===")

    # ── Types d'honoraires ─────────────────────────────
    SELECT_H = "type_honoraires_niveau_1,type_honoraires_niveau_2,type_honoraires_niveau_3"

    resultats = collecter_tout(
        dataset_id="honoraires-detailles",
        select=SELECT_H,
        group_by=SELECT_H
    )

    for rec in resultats:
        n1 = rec.get("type_honoraires_niveau_1") or ""
        n2 = rec.get("type_honoraires_niveau_2") or None
        n3 = rec.get("type_honoraires_niveau_3") or None

        if n1:
            existe = session.query(TypeHonoraire).filter_by(
                niveau_1=n1,
                niveau_2=n2,
                niveau_3=n3
            ).first()

            if not existe:
                session.add(
                    TypeHonoraire(
                        niveau_1=n1,
                        niveau_2=n2,
                        niveau_3=n3
                    )
                )

    session.commit()

    print(f"Types d'honoraires : {session.query(TypeHonoraire).count()}")

    # ── Types de prescriptions ─────────────────────────
    resultats = collecter_tout(
        dataset_id="prescriptions",
        select="libelle_poste_prescription",
        group_by="libelle_poste_prescription"
    )

    for rec in resultats:
        libelle = rec.get("libelle_poste_prescription")

        if libelle:
            existe = session.query(TypePrescription).filter_by(
                libelle=libelle
            ).first()

            if not existe:
                session.add(TypePrescription(libelle=libelle))

    session.commit()

    print(f"Types de prescriptions : {session.query(TypePrescription).count()}")

    session.close()

    print("=== Terminé ===")