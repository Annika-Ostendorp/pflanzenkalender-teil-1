from datetime import date
from app import plants
from models import Plant

def test_api_plants_id_schedules_success(client):
    plants.clear()

    # wieder Testpflanze vorbereiten
    plant_creation_date = date(2026, 5, 10)
    test_plant = Plant(1, "Monstera", "Deliciosa", "Wohnzimmer", plant_creation_date)
    plants.append(test_plant)

    # Payload für neuen Pflegeplan (Szenario A)
    payload = {
        "care_type": "watering",
        "interval_days": 7
    }

    response = client.post('/api/plants/1/schedules', json=payload) # mit POST Request neuen CareSchedule erzeugen
    data = response.get_json()

    # Überprüfungen
    assert response.status_code == 201 # wurde neuer care schedule erfolgreich angelegt?
    assert data["id"] == 1 # erster Plan der Pflanze --> ID = 1
    assert data["plant_id"] == 1
    assert data["care_type"] == "watering"
    assert data["interval_days"] == 7
    assert len(test_plant._schedules) == 1 # wurde neue Pflanze hinzugefügt -> Liste muss nun Länge von 1 haben