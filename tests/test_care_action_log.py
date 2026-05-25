from datetime import date
from app import plants
from models import Plant

def test_api_post_plants_id_logs_success(client):
    plants.clear()

    # wieder Testpflanze vorbereiten
    plant_creation_date = date(2026, 5, 20)
    test_plant = Plant(1, "Monstera", "Deliciosa", "Garten", plant_creation_date)
    plants.append(test_plant)