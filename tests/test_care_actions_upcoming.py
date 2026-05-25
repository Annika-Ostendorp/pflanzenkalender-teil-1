from datetime import date
from unittest.mock import patch
from app import plants
from models import Plant, CareSchedule, ActionLog

def test_api_get_plants_id_next_actions_sorting_success(client):
    plants.clear()

    # wieder MagicMock weil wir ja mit Datum arbeiten -> wie bei status Tests früher
    fixed_today = date(2026, 5, 25)

    with patch('app.date') as mock_date:
        mock_date.today.return_value = fixed_today

        test_plant = Plant(1, "Goldfruchtpalme", "Palme", "Flur", date(2026, 5, 10))
    
        # Szenario A: overdue ist False, da noch Zeit, bis Aktion ausgeführt werden muss
        # 27. Mai - 25. Mai = 2 Tage übrig (interval_days + 20. Mai = 27. Mai)
        schedule_watering = CareSchedule(1, 1, "watering", 7, None)
        log_watering = ActionLog(1, 1, "watering", date(2026, 5, 20), "Gegossen")
        test_plant._logs.append(log_watering)

        # Szenario B: overdue ist True, da Aktion bereits überfällig -> negatives days_until
        # 20. Mai - 25. Mai = -5 Tage
        schedule_fertilizing = CareSchedule(2, 1, "fertilizing", 10, None)

        test_plant._schedules.append(schedule_watering)
        test_plant._schedules.append(schedule_fertilizing)
        plants.append(test_plant)

        # Daten holen
        response = client.get('/api/plants/1/next-actions')
        data = response.get_json()

        # Überprüfungen
        assert response.status_code == 200
        assert len(data) == 2 # sind 2 Pflegepläne in Liste der kommenden Aktionen?

        # Aufsteigende Sortierung prüfen
        assert data[0]["care_type"] == "fertilizing"
        assert data[0]["next_due"] == "2026-05-20"
        assert data[0]["days_until"] == -5 # als erstes (Index 0) muss in Liste die überfällige Aktion kommen
        assert data[0]["overdue"] is True # ist überfällig -> True

    # das Gießen was erst in 2 Tagen fällig ist kommt danach
    assert data[1]["care_type"] == "watering"
    assert data[1]["next_due"] == "2026-05-27"
    assert data[1]["days_until"] == 2
    assert data[1]["overdue"] is False

    # wieder prüfen, ob wirklich simuliertes Datum benutzt wurde
    mock_date.today.assert_called_once()