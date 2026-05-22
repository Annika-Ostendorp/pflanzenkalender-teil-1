from datetime import date
from app import plants
from models import Plant, CareSchedule

def test_api_delete_plants_id_care_schedules_care_type_success(client):
    plants.clear()

    # wieder Pflanze vorbereiten mit Pflegeplan
    plant_creation_date = date(2026, 5, 22)
    test_plant = Plant(1, "Schmetterlingsorchidee","Phalaenopsis", "Terrasse", plant_creation_date)

    # neuen Pflegeplan der Pflanze hinzufügen
    test_schedule = CareSchedule(1, 1, "fertilizing", 30, None)
    test_plant._schedules.append(test_schedule)
    plants.append(test_plant)

    # Ist Plan sicher in Liste drin? -> ansonsten könnten wir ihn ja nicht löschen
    assert len(test_plant._schedules) == 1

    response = client.delete('/api/plants/1/schedules/fertilizing')

    # Überprüfungen -> muss erfolgreich gelöscht sein
    assert response.status_code == 204
    assert len(test_plant._schedules) == 0 # darf kein Plan mehr enthalten sein!


def test_api_delete_plants_id_schedules_care_type_plant_not_found(client):
    plants.clear()

    response = client.delete('/api/plants/999/schedules/watering') # ID existiert nicht -> Fehler
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data
    assert data["error"] == "Plant not found"