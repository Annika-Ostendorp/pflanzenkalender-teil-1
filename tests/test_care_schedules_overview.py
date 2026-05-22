from datetime import date
from app import plants
from models import Plant, CareSchedule

def test_api_get_plants_id_schedules_success(client):
    plants.clear()

    # Test Pflanze wieder anlegen
    plant_creation_date = date(2026, 5, 22)
    test_plant = Plant(1, "Goldfruchtpalme", "Palme", "Terrasse", plant_creation_date)

    # Test Pflegeplan Testpflanze hinzufügen und dann der gesamten Pflanzen-Liste hinzufügen
    test_schedule = CareSchedule(1, 1, "repotting", 7, None)
    test_plant._schedules.append(test_schedule)
    plants.append(test_plant)

    response = client.get('/api/plants/1/schedules')
    data = response.get_json()

    # Überprüfungen
    assert response.status_code == 200
    assert len(data) == 1 # Liste muss ja hier genau 1 Plan enthalten

    # jetzt genau diese CareSchedule Liste durchgehen -> ist an 1. Stelle der großen Liste -> deshalb [0] (Python beginnt ja bei 0 mit zählen)
    assert data[0]["id"] == 1
    assert data[0]["plant_id"] == 1
    assert data[0]["care_type"] == "repotting"
    assert data[0]["interval_days"] == 7


def test_api_get_plants_id_schedules_not_found(client):
    plants.clear()

    # nicht existierende ID nehmen für GET-Request
    response = client.get('/api/plants/999/schedules')
    data = response.get_json()

    # Überprüfungen
    assert response.status_code == 404 # ID existiert nicht -> Fehler
    assert "error" in data
    assert data["error"] == "Plant not found" # richtige Fehlermeldung?