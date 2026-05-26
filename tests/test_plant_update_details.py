from app import plants

def test_api_put_plants_id_partial_update_success(client):

    # vorbereiteter Payload -> Pflanze anlegen für Ausgangszustand
    setup_payload = {
        "name": "Goldfruchtpalme",
        "species": "Palme",
        "location": "Büro"
    }

    post_response = client.post('/api/plants', json=setup_payload) # hier wird das obige Setup als JSON-Payload mitgegeben für POST-Anfrage
    post_id = post_response.get_json()["id"] # get_json wandelt wieder die Antwort von Server in Dictionary um -> ID/ Adresse wird dann rausgegriffen mit ["id"]

    update = {"location": "Balkon"} # jetzt Feld location updaten -> nur location, um zu testen, ob auch Teil-Updates funktionieren
    put_response = client.put(f'/api/plants/{post_id}', json=update) # hier dann vorigen Wert für ID von Pflanze in Pfad einsetzen -> json=update -> schickt dann neue location-Info von Zeile drüber mit

    # Überprüfungen
    assert put_response.status_code == 200 # konnte Update erfolgreich durchgeführt werden?
    data = put_response.get_json()

    assert data["location"] == "Balkon" # stimmt nun geänderter Wert?
    assert data["name"] == "Goldfruchtpalme" # bleiben name und species unverändert?
    assert data["species"] == "Palme"

def test_api_put_plants_id_forbidden_fields(client):
    # wieder Pflanze anlegen, um gültige ID zu haben
    setup = {
        "name": "Monstera",
        "species": "Deliciosa",
        "location": "Schlafzimmer"
    }

    # Gleiche Logik wie bei erfolgreichem Test oben
    post_response = client.post('/api/plants', json=setup)
    post_id = post_response.get_json()["id"]

    forbidden_payload = {
        "id": 99, # übergeben nun falsche ID -> Versuch diese zu ändern, aber ist Teil von forbidden_fields!
        "name": "Schmetterlingsorchidee"
    }
    response = client.put(f'/api/plants/{post_id}', json=forbidden_payload)

    # Überprüfungen
    assert response.status_code == 400 # falsche ID muss mit Bad Request Fehlermeldung abgelehnt werden
    data = response.get_json()

    assert "error" in data # ist Fehlermeldung in Response von Server?
    assert data["error"] == "Bad Request: Updating id, status, created_at or schedules is not allowed"

def test_api_put_plants_id_empty_value(client): # 2. Möglichkeit, dass ungültige Werte übergeben werden (leerer String, etc.)
    setup = {
        "name": "Efeu",
        "species": "Hedera",
        "location": "Bad"
    }

    post_response = client.post('/api/plants', json=setup)
    post_id = post_response.get_json()["id"]
    
    # Übergabe von gültigem Feld name aber mit ungültigem, leeren Inhalt
    response = client.put(f'/api/plants/{post_id}', json={"name": "   "})
    data = response.get_json()

    # Überprüfungen
    assert response.status_code == 400
    assert "error" in data
    assert data["error"] == "Bad Request: name cannot be empty" # kommt wieder richtige Fehlermeldung für ungültiges, leeres Feld?

def test_api_put_plants_id_not_found(client):
    response = client.put('/api/plants/999', json={"name": "Topf"})

    data = response.get_json()
    
    # Überprüfungen
    assert response.status_code == 404 # ID ist ungültig -> richtiger Status Code?
    assert "error" in data
    assert data["error"] == "Plant not found" # richtige Fehlerbeschreibung?