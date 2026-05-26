import pytest
from app import app
import app as flask_app # damit wir auf next_id zugreifen können!

@pytest.fixture # Fixture, um Code-Duplikationen zu vermeiden --> kann dann in allen Tests verwendet werden
                # und muss so später nur an einer Stelle etwas ändern, Bsp.daten für unsere API-Tests anlegen
def client():
    app.config['TESTING'] = True # Setup/ Vorbereitung -> Test-Konfiguration aktivieren
    with app.test_client() as client:
        # vor jedem Test Zustand komplett zurücksetzen
        flask_app.plants.clear()
        flask_app.next_id = 1

        yield client

        # nach dem Test Zustand wieder aufräumen
        flask_app.plants.clear()
        flask_app.next_id = 1