from datetime import date
from unittest.mock import patch, MagicMock # patch, um Tests zeitunabhängig zu machen
from app import Plant, CareSchedule # beide wichtig für calculate_status Methode

def test_api_plants_get_success(client): # Happy Path (200) & korrekte JSON-Struktur testen
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


def test_api_plants_get_status_soon_with_mock(): # müssen ja auch Magic Mocks nutzen
    # AAA-Prinzip: ARRANGE (Vorbereiten)
    # Simulation von festem Datum und Pflege-Objekt
    set_today = date(2026, 5, 13)
    due_soon = date(2026, 5, 15) # fällig in 2 Tagen -> soon
    
    with patch('app.date') as mock_date:
        mock_date.today.return_value = set_today # gewünschtes Ergebnis ist ja simuliertes heutiges Datum -> soll zurückgegeben werden

        mock_schedule = MagicMock(spec = CareSchedule) # Bsp.-Pflegeplan aufsetzen
        mock_schedule.next_due = due_soon # nutzen next_due Variable von Klasse CareSchedule von vorhin

        plant = Plant(1, "Goldfruchtpalme", "Palme", "Wohnzimmer", set_today) # wurde heute kreiert -> simuliertes heutiges Datum nehmen
        plant._schedules.append(mock_schedule)

        # ACT -> Logik aufrufen, die wir ja prüfen wollen
        result = plant.calculate_status()

        # ASSERT -> Überprüfung
        assert result == "soon" # ist Status bei soon? -> hatten ja oben next_due Variable mit due_soon Datum gesetzt
        mock_date.today.assert_called_once() # hat unsere Logik auch wirklich das Datum abgefragt?