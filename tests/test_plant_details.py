from app import Plant
from datetime import date
from unittest.mock import patch

def test_api_plants_id_get_success(client): # hier wieder mit MagicMock (wie bei test_plant_overview.py), um zu prüfen, ob Pflanze auch wirklich korrekt zurückgegeben ("ok") wird -> dafür Mock-Datum
    set_today = date(2026, 5, 13)
    desired_next_due = date(2026, 5, 15) # in 2 Tagen fällig -> "soon"-> AttributeError (next_due of Care Schedule object has no setter) lösen -> desired_next_due

    with patch('app.date') as mock_date:
        mock_date.today.return_value = set_today

        from app import plants, CareSchedule # wieder Liste mit allen Pflanzen holen & leeren für sauberen Test
        plants.clear()

        test_plant = Plant(1, "Bogenhanf", "Sansevieria", "Schlafzimmer", set_today) # wieder Testpflanze erstellen mit Mock-Datum
        
        last_done = date(2026, 5, 8) # damit bei 7 Tagen Intercall von schedule dann automatisch der 15.05. als next_due rauskommt
        real_schedule = CareSchedule(3, "watering", 7, last_done) # brauchen hier echten Plan, da Objekt nur so mit to_json()-Methode von Flask verarbeitet werden kann

        test_plant._schedules.append(real_schedule) # Pflanze braucht ja Liste an care schedules
        plants.append(test_plant)

        response = client.get('/api/plants/1')
        data = response.get_json()

        # Überprüfungen
        assert response.status_code == 200 # kommt richtiger Statuscode?
        assert data["name"] == "Bogenhanf"
        assert data["status"] == "soon"
        assert len(data["schedules"]) == 1 # werden Schedules zurückgegeben als Liste?