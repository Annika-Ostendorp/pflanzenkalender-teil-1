from models import Plant, CareSchedule
from datetime import date
from unittest.mock import patch

def test_api_get_plants_id_success(client): # hier wieder mit MagicMock (wie bei test_plant_overview.py), um zu prüfen, ob Pflanze auch wirklich korrekt zurückgegeben ("ok") wird -> dafür Mock-Datum
    set_today = date(2026, 5, 13)
    plant_created = date(2026, 5, 10) # Pflanze 3 Tage vor heute erstellt
    desired_next_due = date(2026, 5, 15) # in 2 Tagen fällig -> "soon"-> AttributeError (next_due of Care Schedule object has no setter) lösen -> desired_next_due

    with patch('models.date') as mock_date:
        mock_date.today.return_value = set_today

        from app import plants # wieder Liste mit allen Pflanzen holen & leeren für sauberen Test
        plants.clear()

        test_plant = Plant(1, "Bogenhanf", "Sansevieria", "Schlafzimmer", plant_created) # wieder Testpflanze erstellen mit Mock-Datum
        
        real_schedule = CareSchedule(3, 1, "watering", 5, desired_next_due) # brauchen hier echten Plan, da Objekt nur so mit to_json()-Methode von Flask verarbeitet werden kann
                                                                            # Intervall auf 5 Tage -> Dynamische Berechnung 10.05 + 5 = 15.05

        test_plant._schedules.append(real_schedule) # Pflanze braucht ja Liste an care schedules
        plants.append(test_plant)

        response = client.get('/api/plants/1')
        data = response.get_json()

        # Überprüfungen
        assert response.status_code == 200 # kommt richtiger Statuscode?
        assert data["name"] == "Bogenhanf"
        assert data["status"] == "soon"
        assert len(data["schedules"]) == 1 # werden Schedules zurückgegeben als Liste?

def test_api_get_plants_id_not_found(client): # diesselbe Logik wie wenn Löschen von Pflanze nicht geht
    response = client.get('/api/plants/99') # Bsp.ID nehmen
    data = response.get_json()

    # Überprüfen, ob richtiger Statuscode & Fehlermeldung kommt
    assert response.status_code == 404
    assert "error" in data # kommt dieses Feld?
    assert data["error"] == "Plant not found" # richtige Fehlermeldung?