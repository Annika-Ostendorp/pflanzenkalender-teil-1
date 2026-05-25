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