from flask import Flask, jsonify, request, Response
from datetime import datetime # um Datums-Bedingung (created_at) umzusetzen

app = Flask(__name__)

plants = []

class Plant:
    def __init__(self, id: int, name: str, species: str, location: str, created_at: str = None) -> None:
        self._id = id
        self._name = name
        self._species = species
        self._location = location
        self._created_at = created_at if created_at else datetime.now().isoformat() # Falls kein Datum übergeben wird, soll jetziges Datum genommen werden
        self._schedules = []
        self._logs = []
    
    def to_json(self) -> dict: # Nutzen to_json, um Zugriff auf private Member-Variablen von Klasse Plant zu bekommen für JSON-Ausgabe
        return {
            "id": self._id,
            "name": self._name,
            "species": self._species,
            "location": self._location,
            "created_at": self._created_at,
            "schedules": self._schedules,
            "logs": self._logs
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

    new_plant = Plant(
        id = next_id,
        name = data["name"],
        species = data["species"],
        location = data["location"],
        created_at = data.get("created_at") # mit .get(), um Fehler zu vermeiden, falls Datum nicht existieren sollte --> gibt dann per Default das jetzige Datum aus
    )

    plants.append(new_plant) # neue Pflanze zur Liste hinzufügen
    next_id += 1 # nachdem Pflanzen-Objekt erstellt wurde -> Zähler hochsetzen, damit neue Pflanze = neue ID
    
    return jsonify(new_plant.to_json()), 201 # Pflanzen-Objekt nun erfolgreich erstellt -> 201 