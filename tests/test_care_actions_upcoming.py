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
        