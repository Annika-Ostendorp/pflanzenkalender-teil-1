from datetime import date
from app import plants
from models import Plant, CareSchedule

def test_api_get_plants_id_schedules_success(client):
    plants.clear()

    # Test Pflanze wieder anlegen
    plant_creation_date = date(2026, 5, 22)
    test_plant = Plant(1, "Goldfruchtpalme", "Palme", "Terrasse", plant_creation_date)

    # Test Pflegeplan Testpflanze hinzufügen und dann der gesamten Pflanzen-Liste hinzufügen
    test_schedule = CareSchedule(1, 1, "repotting", 7, None)
    test_plant._schedules.append(test_schedule)
    plants.append(test_plant)