from datetime import date
from unittest.mock import patch
from app import plants
from models import Plant, CareSchedule, ActionLog

def test_api_get_overdue_sorting_success(client):
    plants.clear()

    fixed_today = date(2026, 5, 25)