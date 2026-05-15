
def test_api_plants_post_success(client): # Beispieldaten hier verwenden --> Gültige Testdaten (Payload Aspekt in User Story)
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

def test_api_plants_post_missing_fields(client):
    payload = { # erzeugen nun extra unvollständiges JSON-Objekt -> wollen ja error erzeugen
        "name": "Goldfruchtpalme"
    }

    response = client.post('/api/plants', json=payload)
    data = response.get_json()

    assert response.status_code == 400 # erwarten ja Fehler Status Code, da JSON-Objekt unvollständig 
    assert "error" in data # wird Fehlermeldung ausgegeben?
    assert "Bad Request: Missing or invalid JSON body" in data["error"] # Richtige Beschreibung der Fehlermeldung?

def test_api_plants_post_with_date_success(client):
    payload = {
        "name": "Schmetterlingsorchidee",
        "species": "Phalaenopsis",
        "location": "Büro",
        "created_at": "2026-01-01" # damit die Missing Zeile 98 (actual_date = date.fromisoformat(date_str)) aufgerufen wird für bessere Code Coverage --> davor immer direkt in else Schleife gesprungen, da nie Datum mitgegeben
    }

    response = client.post('/api/plants', json=payload)
    data = response.get_json()

    assert data["created_at"] == "2026-01-01"
    assert data["name"] == "Schmetterlingsorchidee"