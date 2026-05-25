from datetime import date
from app import plants
from models import Plant, ActionLog

def test_api_get_plants_id_logs_success_sorted(client):
    # wieder Testpflanze und Logs vorbereiten
    plants.clear()
    plant_creation_date = date(2026, 5, 10)
    test_plant = Plant(1, "Orchidee", "Phalaenopsis", "Schlafzimmer", plant_creation_date)

    # 2 Test Logs -> für Test von Sortiermechanismus
    older_log = ActionLog(1, 1, "repotting", date(2026, 5, 14), "Altes Log")
    newer_log = ActionLog(2, 1, "watering", date(2026, 5, 24), "Neues Log")

    # logs unsortiert hinzufügen -> altes Log zuerst und danach erst das neuere Log
    test_plant._logs.append(older_log)
    test_plant._logs.append(newer_log)
    plants.append(test_plant)