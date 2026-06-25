from controllers import dashboard


def test_pages_principales_repondent(monkeypatch):
    monkeypatch.setattr(dashboard.api_ameli, "get_pathologies", lambda: ["Diabete"])
    monkeypatch.setattr(dashboard.api_ameli, "derniere_erreur", None)

    from app import app

    client = app.test_client()
    for route in [
        "/",
        "/indicateurs",
        "/comparaisons",
        "/prescriptions",
        "/honoraires",
        "/pathologies",
        "/a-propos",
    ]:
        response = client.get(route)
        assert response.status_code == 200


def test_anciennes_routes_supprimees():
    from app import app

    client = app.test_client()
    assert client.get("/secteurs").status_code == 404
    assert client.get("/effectifs").status_code == 404


def test_api_departements_retourne_du_json():
    from app import app

    client = app.test_client()
    response = client.get("/api/departements/1")
    assert response.status_code == 200
    assert response.is_json
