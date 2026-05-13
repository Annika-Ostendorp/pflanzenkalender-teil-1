import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock # patch, um Tests zeitunabhängig zu machen
from app import Plant, CareSchedule # beide wichtig für calculate_status Methode

def test_get_plants_success(client): # Happy Path (200) & korrekte JSON-Struktur testen
    from app import plants # geht ja darum, dass die Liste der Pflanzen zurückgegeben wird
    plants.clear() # erstmal alles leeren, für Neustart -> sauberen Test, ob Pflanzen-Objekt existiert

    test_plant = Plant(1, "Goldfruchtpalme", "Palme", "Wohnzimmer", date(2026, 7, 1))
    plants.append(test_plant)

    response = client.get('/api/plants') # Daten werden hier wieder per GET an Endpoint gesendet 
    data = response.get_json() 

    # Prüfungen
    assert response.status_code == 200 # existiert eine Liste mit Pflanzen? -> erfolgreiche Rückmeldung
    assert len(data) == 1 # bisher nur eine Pflanzen-Instanz in Liste -> stimmt das?

    # JSON-Struktur validieren
    plant_json = data[0] # an erster Stelle in Liste ist Eintrag (0. Stelle bei Python)

    expected_fields = ["id", "name", "species", "location", "created_at", "status"] # diese Felder hat Plant-Objekt
    for field in expected_fields:
        assert field in plant_json # Gibt es Feld in Pflanzenobjekt-Eintrag?
    
    assert plant_json["name"] == "Goldfruchtpalme" # ist diesem field auch etwas zugeordnet? -> hat Datenübertragung geklappt?
    assert plant_json["status"] == "ok" # schauen, ob calculate_status Methode funktioniert hat
    # nur für 2 fields Asserts, um Tests lesbar zu halten 