from app import plants

def test_api_plants_id_put_partial_success(client):
    # wieder zur Vorbereitung Liste leeren für klare IDs der Pflanzen
    plants.clear()

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