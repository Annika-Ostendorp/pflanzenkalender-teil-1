from datetime import date
from app import plants
from models import Plant, CareSchedule

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


def test_api_plants_id_schedules_update_success(client):
    plants.clear()

    # wieder Vorbereitung von Testpflanze
    plant_creation_date = date(2026, 5, 14)
    test_plant = Plant(1, "Monstera", "Deliciosa", "Büro", plant_creation_date)

    old_schedule = CareSchedule(1, 1, "watering", 7, None) # wurde noch nicht geupdatet -> old_schedule
    test_plant._schedules.append(old_schedule) # bestehenden alten Plan der Pflanze geben
    plants.append(test_plant)

     # neues Intervall festlegen
    payload = {
        "care_type": "watering",
        "interval_days": 14
    }

    response = client.post('/api/plants/1/schedules', json=payload)
    data = response.get_json()

    # Überprüfungen
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["interval_days"] == 14 # wurde Intervall erfolgreich aktualisiert?
    assert len(test_plant._schedules) == 1


def test_api_plants_id_schedules_errors_care_type(client):
    plants.clear()

    # Pflanze existiert nicht im Speicher
    payload = {
        "care_type": "repotting",
        "interval_days": 7
    }

    response = client.post('/api/plants/999/schedules', json=payload)
    assert response.status_code == 404 # ungültige ID -> Fehlermeldung mit Status Code 404

    # brauchen jetzt wieder Testpflanze für Überprüfung von ungültigem care_type
    test_plant = Plant(1, "Monstera", "Deliciosa", "Schlafzimmer", date(2026, 5, 19))
    plants.append(test_plant)

    # care_type ist leer
    invalid_payload = {
        "care_type": "  ",
        "interval_days": 7
    }
    response = client.post('/api/plants/1/schedules', json=invalid_payload)
    assert response.status_code == 400 # care_type ist ungültig wegen Leerzeichen -> Fehlermeldung & Statuscode 400

    # care_type hat falschen Typ
    payload_wrong_type = {
        "care_type": 246,
        "interval_days": 7
    }
    response = client.post('/api/plants/1/schedules', json=payload_wrong_type)
    assert response.status_code == 400 # care_type hat falschen Typ (nicht str) -> 400


def test_api_plants_id_schedules_errors_interval_days(client):
    plants.clear()

    test_plant = Plant(1, "Monstera", "Deliciosa", "Schlafzimmer", date(2026, 5, 19))
    plants.append(test_plant)

    # Attribut interval_days fehlt 
    payload_missing = {
        "care_type": "repotting"
    }
    response = client.post('/api/plants/1/schedules', json=payload_missing)
    assert response.status_code == 400 # interval_days fehlt komplett -> Fehler (400)

    # interval_days ist ein ungültiger Typ -> Nachkommazahl statt ganze Zahl
    payload_float = {
        "care_type": "watering",
        "interval_days": 3.5
    }
    response = client.post('/api/plants/1/schedules', json=payload_float)
    assert response.status_code == 400

    # interval_days ist ungültig -> kleiner als 1
    payload_zero = {
        "care_type": "repotting",
        "interval_days": 0
    }
    response = client.post('/api/plants/1/schedules', json=payload_zero)
    assert response.status_code == 400