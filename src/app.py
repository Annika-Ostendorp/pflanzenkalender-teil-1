from flask import Flask, jsonify, request, Response
from datetime import timedelta, date # timedelta, um Zeitdifferenz zwischen 2 Zeiten zu berechnen -> Tage, Stunden, Minuten, Sekunden addieren oder subtrahieren
                                             # wichtig für "soon" Status z.B.
                                             # date, um Datums-Bedingung (created_at) umzusetzen

app = Flask(__name__)

plants = []

class Plant:
    def __init__(self, id: int, name: str, species: str, location: str, created_at: date) -> None:
        self._id = id
        self._name = name
        self._species = species
        self._location = location
        self._created_at = created_at
        self._schedules = [] # Liste mit CareSchedule Objekten
        self._logs = [] # Liste mit ActionLog Objekten
    
    def to_json(self) -> dict: # Nutzen to_json, um Zugriff auf private Member-Variablen von Klasse Plant zu bekommen für JSON-Ausgabe
        return {
            "id": self._id,
            "name": self._name,
            "species": self._species,
            "location": self._location,
            "created_at": str(self._created_at), # in string umwandeln für richtige Ausgabe 
            "status": self.calculate_status(),
            "schedules": [schedule.to_json() for schedule in self._schedules], # jedes Objekt in der Liste soll zu einem Dictionary umgewandelt werden, und trotzdem leere Listen ausgeben für Variablen schedules, logs falls es diese nicht gibt 
                                                                               # --> bessere Darstellung/ Struktur, um Pflanzen zusammen mit ihren Pflegeplänen etc. anzuzeigen
            "logs": [log.to_json() for log in self._logs]
        }
    
    def calculate_status(self) -> str:
        today = date.today() # heutiges Datum als Bsp. festlegen, damit Berechnung für z.B. "overdue"-Logik funktioniert
        three_days_from_now = today + timedelta(days = 3)

        for schedule in self._schedules: # erst alles prüfen, ob etwas "overdue" ist
            if schedule.next_due < today: # wenn mind. eine Aktion schon überfällig ist  
                return "overdue"

        for schedule in self._schedules: # danach prüfen, ob etwas "soon" ist
            if schedule.next_due <= three_days_from_now: # wenn mind. eine Aktion in 3 oder weniger Tagen fällig ist
                return "soon"
        
        return "ok" # wenn alle Aktionen mehr als 3 Tage in der Zukunft liegt -> wenn 2 Schleifen durchgelaufen, aber keine Übereinstimmung gefunden haben
               
class CareSchedule:
    def __init__(self, id: int, care_type: str, interval_days: int, next_due: date) -> None:
        self._id = id
        self._care_type = care_type
        self._interval_days = interval_days
        self._next_due = next_due
    
    @property # Property-Dekorator, um nicht immer Klammern mitschreiben zu müssen bei Methode -> auf Methode zugriefen wie auf normale Variablen
    def next_due(self) -> date:
        return self._next_due

    def to_json(self) -> dict:
        return {
            "id": self._id,
            "care_type": self._care_type,
            "interval_days": self._interval_days,
            "next_due": str(self._next_due) # next_due hinzufügen für calculate_status Methode, damit Tests nicht fehlschlagen
        }

class ActionLog:
    def __init__(self, id: int, care_type: str, performed_at: date, notes: str) -> None:
        self._id = id
        self._care_type = care_type
        self._performed_at = performed_at
        self._notes = notes

    def to_json(self) -> dict:
        return {
            "id": self._id,
            "care_type": self._care_type,
            "performed_at": str(self._performed_at),
            "notes": self._notes
        }   
    
next_id = 1 # Zähler festlegen für ID, damit jede Pflanze ihre eindeutige ID bekommt

# Route für Endpoint POST /api/plants
@app.route('/api/plants', methods=['POST'])
def create_plant() -> Response:
    data = request.get_json() # new_plant umbenannt in data, da hiermit ja noch kein richtiges Plant-Objekt erzeugt wird -> nur Daten geholt

    mandatory_fields = ["name", "species", "location"]
    for field in mandatory_fields:
        # Fehlen Attribute oder gibt es leere Strings?
        if field not in data or data[field] == "":
            return jsonify({"error": "Bad Request: Missing or invalid JSON body"}), 400 # in diesem Fall Error zurückgeben
    
    global next_id # mit global next_id außerhalb der Funktion abändern

    date_str = data.get("created_at") # mit .get(), um Fehler zu vermeiden, falls Datum nicht existieren sollte --> gibt dann per Default das jetzige Datum aus (siehe else Bedingung)
    if date_str: # falls gültig, also nicht leer o.ä.
        actual_date = date.fromisoformat(date_str) # Datum hier wieder in date-Objekt umwandeln zur besseren Überprüfung

    else:
        actual_date = date.today()

    new_plant = Plant(
        id = next_id,
        name = data["name"],
        species = data["species"],
        location = data["location"],
        created_at = actual_date
    )

    plants.append(new_plant) # neue Pflanze zur Liste hinzufügen
    next_id += 1 # nachdem Pflanzen-Objekt erstellt wurde -> Zähler hochsetzen, damit neue Pflanze = neue ID
    
    return jsonify(new_plant.to_json()), 201 # Pflanzen-Objekt nun erfolgreich erstellt -> 201 


# Route für Endpoint GET /api/plants
@app.route('/api/plants', methods=['GET'])
def get_plants() -> Response:
    return jsonify([plant.to_json() for plant in plants]), 200 # wollen jede Pflanze aus Liste im Dictionary-Format bekommen -> Sammlung

# Route für Endpoint DELETE /api/plants/<id>
@app.route('/api/plants/<int:plant_id>', methods=['DELETE']) # brauchen Pflanzen-ID -> damit wir wissen, welche Pflanze wir löschen
def delete_plant(plant_id: int) -> Response:
    global plants # wollen wieder außerhalb von Funktion auf Liste mit all unseren Pflanzen zugreifen

    for plant in plants:
        if plant._id == plant_id: # hat Pflanzenobjekt diesselbe ID wie die Übergebene?
            plants.remove(plant) # falls ja, dann dieses Objekt löschen
            return '', 204 # erfolgreiches Löschen von Pflanze -> 204 No Content -> leerer String als Body
    
    return jsonify({"error": "Plant not Found"}), 404 # falls ID nicht existieren sollte -> Fehlermeldung zurückgeben


if __name__ == "__main__": # damit App aufgerufen werden kann mit Port 5000
    app.run(debug=True, port=5000) 