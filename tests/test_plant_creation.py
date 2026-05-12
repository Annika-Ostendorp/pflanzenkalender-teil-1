import pytest
from app import app

@pytest.fixture # Fixture, um Code-Duplikationen zu vermeiden --> kann dann in allen Tests verwendet werden
                # und muss so später nur an einer Stelle etwas ändern, Bsp.daten für unsere API-Tests anlegen
def client():
    app.config['TESTING'] = True # Setup/ Vorbereitung -> Test-Konfiguration aktivieren
    with app.test_client() as client:
        yield client


def test_create_plant_success(client): # Beispieldaten hier verwenden --> Gültige Testdaten (Payload Aspekt in User Story)
    payload = {
        "name": "Monstera",
        "species": "Deliciosa",
        "location": "Wohnzimmer"
    }

    response = client.post('/api/plants', json=payload) # Daten werden per POST an Endpoint gesendet 
    data = response.get_json() # da Content-Type ja application/json sein muss 

    # Überprüfungen
    assert response.status_code == 201 # Ist Statuscode von erzeugtem Pflanzenobjekt 201 für erfolgreiche Erstellung?
    assert data["name"] == "Monstera" # Hat erzeugtes Objekt diesen Namen bzw. Namen richtig übernommen?
    assert "id" in data # Wurde spezifische ID vergeben? (siehe Task 3)
    assert "created_at" in data # Existiert ein Erstellungsdatum/ das heutige Datum als Default? (siehe Task 3)

