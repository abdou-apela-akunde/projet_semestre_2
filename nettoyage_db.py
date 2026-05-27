from connexion import connexion

engine = connexion()

if engine:
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS formation"))
        conn.execute(text("DROP TABLE IF EXISTS departement"))
        conn.commit()
        print("Tables de test supprimées.")