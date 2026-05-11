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
    
# Route für Endpoint POST /api/plants
@app.route('/api/plants', methods=['POST'])
def create_plant() -> Response:
    new_plant = request.get_json()

    mandatory_fields = ["name", "species", "location"]
    for field in mandatory_fields:
        # Fehlen Attribute oder gibt es leere Strings?
        if field not in new_plant or new_plant[field] == "":
            return jsonify({"error": "Bad Request: Missing or invalid JSON body"}), 400 # in diesem Fall Error zurückgeben
    
    plants.append(new_plant) # neue Pflanze zur Liste hinzufügen
    
    return jsonify(new_plant), 201