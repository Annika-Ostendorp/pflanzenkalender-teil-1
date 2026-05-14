import pytest
from app import app

@pytest.fixture # Fixture, um Code-Duplikationen zu vermeiden --> kann dann in allen Tests verwendet werden
                # und muss so später nur an einer Stelle etwas ändern, Bsp.daten für unsere API-Tests anlegen
def client():
    app.config['TESTING'] = True # Setup/ Vorbereitung -> Test-Konfiguration aktivieren
    with app.test_client() as client:
        yield client