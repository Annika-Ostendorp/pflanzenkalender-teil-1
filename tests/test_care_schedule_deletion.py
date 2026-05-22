from datetime import date
from app import plants
from models import Plant, CareSchedule

def test_api_delete_plants_id_care_schedules_care_type_success(client):
    