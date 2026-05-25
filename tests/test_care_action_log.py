from datetime import date
from app import plants
from models import Plant

def test_api_post_plants_id_logs_success(client):
    plants.clear()

    # wieder Testpflanze vorbereiten
    plant_creation_date = date(2026, 5, 20)
    test_plant = Plant(1, "Monstera", "Deliciosa", "Garten", plant_creation_date)
    plants.append(test_plant)

    payload = {
        "care_type": "watering",
        "performed_at": "2026-05-24",
        "notes": "Mit viel Regenwasser gegossen"
    }

    response = client.post('/api/plants/1/logs', json=payload)
    data = response.get_json() # wieder Daten holen

    # Überprüfungen
    assert response.status_code == 201 # wurde neuer Log erfolgreich erstellt?
    assert data["id"] == 1 # allererster Log-Eintrag für Testpflanze -> ID = 1
    assert data["plant_id"] == 1
    assert data["care_type"] == "watering"
    assert data["performed_at"] == "2026-05-24"
    assert data["notes"] == "Mit viel Regenwasser gegossen"

    assert len(test_plant._logs) == 1 # ist neuer Log-Eintrag in Liste?


def test_api_post_plants_id_logs_success_with_default_date(client): # damit testen, ob Logik, wenn kein Datum übergeben wird automatisch heute als Default genommen wird
    plants.clear()

    plant_creation_date = date(2026, 5, 20)
    test_plant = Plant(1, "Bogenhanf", "Sansevieria", "Bad", plant_creation_date)
    plants.append(test_plant)

    # Payload diesmal ohne performed_at & notes -> werden Default Werte genommen?
    payload = {
        "care_type": "fertilizing"
    }

    response = client.post('/api/plants/1/logs', json=payload)
    data = response.get_json()

    # Überprüfungen
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["care_type"] == "fertilizing"
    assert data["performed_at"] == str(date.today()) # wurde heutiges Datum genommen?
    assert data["notes"] == "" # fehlende Notes = leerer String?

    assert len(test_plant._logs) == 1


def test_api_post_plants_id_logs_invalid(client):
    plants.clear()

    plant_creation_date = date(2026, 5, 25)
    test_plant = Plant(1, "Goldfruchtpalme", "Palme", "Wohnzimmer", plant_creation_date)
    plants.append(test_plant)

    # care_type fehlt -> muss Fehlermeldung kommen
    payload = {
        "performed_at": "2026-05-25",
        "notes": "Erde nachgeschüttet"
    }

    response = client.post('/api/plants/1/logs', json=payload)
    data = response.get_json()

    # Überprüfungen
    assert response.status_code == 400 # care_type fehlt --> 400 Bad Request
    assert "error" in data
    assert data["error"] == "Bad Request: Missing or invalid care_type"
    assert len(test_plant._logs) == 0 # kein Eintrag in Logs-Liste von Testpflanze! -> Feld fehlt ja