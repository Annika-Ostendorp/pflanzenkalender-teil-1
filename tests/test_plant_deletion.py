from app import Plant # brauchen nicht alles, nur testen, ob Pflanze erfolgreich gelöscht wurde
from datetime import date

def test_api_plants_id_delete_success(client):
    from app import plants
    plants.clear() # mit leerer Liste starten -> extra Pflanze zum Löschen anlegen (das ist Vorbereitung)

    test_plant = Plant(1, "Goldfruchtpalme", "Palme", "Schlafzimmer", date.today()) # wurde heute erstellt
    plants.append(test_plant)

    # Löschanfrage wird gesendet
    response = client.delete('/api/plants/1') # ID von angelegter Bsp.-Pflanze

    # Überprüfungen
    assert response.status_code == 204 # für erfolgreiche Löschung -> No Content
    assert len(plants) == 0 # nach Löschen, darf ja kein Objekt mit dieser ID in Liste sein -> da nur 1 Objekt vorhin hinzugefügt, müsste Liste nun leer sein -> len(plants) == 0

def test_api_plants_id_delete_not_found(client): # falls ID nicht vorhanden ist
    response = client.delete('/api/plants/99') # Bsp.ID nehmen
    data = response.get_json()

    # Überprüfen, ob richtiger Statuscode & Fehlermeldung kommt
    assert response.status_code == 404
    assert "error" in data # kommt dieses Feld?
    assert data["error"] == "Plant not found"
