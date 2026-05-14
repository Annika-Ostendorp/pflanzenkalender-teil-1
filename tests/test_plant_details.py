from app import Plant
from datetime import date
from unittest.mock import patch

def test_api_plants_id_get_success(client): # hier wieder mit MagicMock (wie bei test_plant_overview.py), um zu prüfen, ob Pflanze auch wirklich korrekt zurückgegeben ("ok") wird -> dafür Mock-Datum
    set_today = date(2026, 5, 13)
    due_soon = date(2026, 5, 15) # in 2 Tagen fällig -> "soon"

    with patch('app.date') as mock_date:
        mock_date.today.return_value = set_today

        from app import plants, CareSchedule # wieder Liste mit allen Pflanzen holen & leeren für sauberen Test
        plants.clear()

        test_plant = Plant(1, "Bogenhanf", "Sansevieria", "Schlafzimmer", set_today) # wieder Testpflanze erstellen mit Mock-Datum
        real_schedule = CareSchedule(3, "watering", 7, date(2026, 5, 20)) # brauchen hier echten Plan, da Objekt nur so mit to_json()-Methode von Flask verarbeitet werden kann
        real_schedule.next_due = due_soon

        test_plant._schedules.append(real_schedule) # Pflanze braucht ja Liste an care schedules
        plants.append(test_plant)

        response = client.get('/api/plants/1')
        data = response.get_json()

        # Überprüfungen
        assert response.status_code == 200 # kommt richtiger Statuscode?
        assert data["name"] == "Bogenhanf"
        assert data["status"] == "soon"
        assert len(data["schedules"]) == 1 # werden Schedules zurückgegeben als Liste?