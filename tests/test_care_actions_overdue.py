from datetime import date
from unittest.mock import patch
from app import plants
from models import Plant, CareSchedule, ActionLog

def test_api_get_overdue_sorting_success(client):
    plants.clear()

    fixed_today = date(2026, 5, 25)

    with patch('app.date') as mock_date: # wieder MagicMock, da wir wieder mit Datum arbeiten
        mock_date.today.return_value = fixed_today

        # Pflanze mit überfälligem Plan erstellen für Test
        # alle 5 Tage gießen, fällig am 15. Mai --> am 25. Mai aber schon 10 Tage überfällig
        plant_monstera = Plant(1, "Monstera", "Deliciosa", "Wohnzimmer", date(2026, 5, 10))
        schedule_monstera = CareSchedule(1, 1, "watering", 5, None)
        plant_monstera._schedules.append(schedule_monstera)

        # Neue Pflanze mit überfälligem Plan erstellen
        # alle 12 Tage düngen -> fällig am 22. Mai --> aber am 25. Mai schon 3 Tage überfällig
        plant_goldfruchtpalme = Plant(2, "Goldfruchtpalme", "Palme", "Küche", date(2026, 5, 10))
        schedule_goldfruchtpalme = CareSchedule(2, 2, "fertilizing", 12, None)
        plant_goldfruchtpalme._schedules.append(schedule_goldfruchtpalme)

        # beide Pflanzen in plants-Liste hinzufügen
        plants.append(plant_monstera)
        plants.append(plant_goldfruchtpalme)

        # wieder Daten holen/ API abrufen
        response = client.get('/api/overdue')
        data = response.get_json()

        # Überprüfungen
        assert response.status_code == 200
        assert len(data) == 2 # wurden 2 Pflanzen hinzugefügt?

        # Absteigende Sortierung prüfen -> Monstera die 10 Tage überfällig ist, muss vor Goldfruchtpalme stehen
        assert data[0]["plant_name"] == "Monstera"
        assert data[0]["days_overdue"] == 10
        assert data[0]["plant_location"] == "Wohnzimmer"

        assert data[1]["plant_name"] == "Goldfruchtpalme"
        assert data[1]["days_overdue"] == 3
        assert data[1]["plant_location"] == "Küche"

        # und wieder testen, ob Mock-Datum auch benutzt wurde
        mock_date.today.assert_called_once()


def test_api_get_overdue_empty_list(client):
    plants.clear() # keine Pflanze im System -> es kann dann ja nichts überfällig sein

    fixed_today = date(2026, 5, 25)

    with patch('app.date') as mock_date:
        mock_date.today.return_value = fixed_today

        # wieder Daten holen
        response = client.get('/api/overdue')
        data = response.get_json()

        # Überprüfungen
        assert response.status_code == 200
        assert data == [] # Test muss erfolgreich leere Liste zurückgeben

        # auch hier wieder prüfen, ob Mock-Datum genutzt wurde
        mock_date.today.assert_called_once()