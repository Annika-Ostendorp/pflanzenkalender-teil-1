from flask import Flask, jsonify, request, Response, render_template
from flask_cors import CORS # fehlendes CORS-Modul importieren
from datetime import date
from models import ActionLog, CareSchedule, Plant

app = Flask(__name__)
CORS(app) # brauchen CORS ja für gesamte API

plants = []
    
next_id = 1 # Zähler festlegen für ID, damit jede Pflanze ihre eindeutige ID bekommt

# Route, damit Webseite nun direkt geladen wird ohne 404 Not Found-Fehler
@app.route("/")
def index():
    return render_template("index.html")


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
    
    return jsonify({"error": "Plant not found"}), 404 # falls ID nicht existieren sollte -> Fehlermeldung zurückgeben


# Route für Endpoint GET /api/plants/<id>
@app.route('/api/plants/<int:plant_id>', methods=['GET'])
def get_plants_id(plant_id: int) -> Response: # ähnlicher Aufbau wie bei DELETE route, wo es auch um ID ging
    global plants

    for plant in plants:
        if plant._id == plant_id:
            return jsonify(plant.to_json()), 200 # spezifische Pflanze existiert --> Erfolg (200) --> enthält bereits schedules und status
        
    return jsonify({"error": "Plant not found"}), 404 # falls ID wieder nicht existiert -> Fehlermeldung


# Route für Endpoint PUT /api/plants/<id>
@app.route('/api/plants/<int:plant_id>', methods=['PUT'])
def update_plant(plant_id: int) -> Response:
    global plants

    data = request.get_json() # erstmal wieder alle Daten holen
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # id, status, created_at und schedules dürfen nicht geändert werden!
    forbidden_fields_for_update = ["id", "status", "created_at", "schedules"]

    for field in forbidden_fields_for_update:
        if field in data:
            return jsonify({"error": "Bad Request: Updating id, status, created_at or schedules is not allowed"}), 400
    
    # Herausfinden, welche Felder für ein Update erlaubt sind -> die anderen müssen aber unverändert bleiben
    allowed_fields = ["name", "species", "location"]
    for field in allowed_fields:
        if field in data:
            if data[field] is None or str(data[field]).strip() == "": # umwandeln in str und dann strip -> damit man z.b. auch nicht einfach nur Leerzeichen für Namen eingeben kann
                return jsonify({"error": f"Bad Request: {field} cannot be empty"}), 400
            
    for plant in plants:
        if plant._id == plant_id: # erlaubte Felder sind name, species und location -> schauen, ob sie auch in data sind -> nur dann updaten
            if "name" in data:
                plant._name = data["name"]
            
            if "species" in data:
                plant._species = data["species"]

            if "location" in data:
                plant._location = data["location"]
            
            return jsonify(plant.to_json()), 200 # Felder wurden erfolgreich geupdatet
    
    return jsonify({"error": "Plant not found"}), 404 # falls Schleufe durchläuft, aber keine ID gefunden hat -> Fehlermeldung


# Route für Endpoint POST /api/plants/<id>/schedules
@app.route('/api/plants/<int:plant_id>/schedules', methods=['POST'])
def create_or_update_schedule(plant_id: int) -> Response:
    test_plant = None # Ausgangszustand

    for plant in plants:
        if plant._id == plant_id: # existiert Pflanze überhaupt im Speicher/ Liste?
            test_plant = plant
            break # gefunden -> brauchen keine weitere Bedingung -> break, Schleife abbrechen
    
    if test_plant is None:
        return jsonify({"error": "Plant not found"}), 404 # es existiert noch keine Pflanze -> Fehlermeldung
    
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400 # es existieren keine Daten
    
    # Pflichtfelder care_type oder interval_days fehlen 
    if "care_type" not in data or "interval_days" not in data:
        return jsonify({"error": "Missing care_type or interval_days"}), 400
    
    care_type = data["care_type"]
    interval_days = data["interval_days"]

    # Pflichtfelder sind ungültig -> gleiche Logik wie bei Route PUT /api/plants/<id> -> hier aber mit Sicherheit bei Typarten
    if type(care_type) is not str or str(care_type).strip() == "":
        return jsonify({"error": "Bad Request: care_type cannot be empty"}), 400
    
    if type(interval_days) is not int or interval_days < 1:
        return jsonify({"error": "Bad Request: interval_days must be a positive integer >= 1"}), 400
    

    # Existiert für bestimmten Pflegetyp schon Pflegeplan?
    existing_schedule = None # gibt bisher noch keinen Pflegeplan
    for schedule in test_plant._schedules:
        if schedule._care_type == care_type: # gleiche Logik wie oben --> existiert Pflegetyp in Liste --> existing_schedule = schedule
            existing_schedule = schedule
            break

    # Szenario B -> Falls schedule mit diesem care_type existiert -> Update von interval_days
    if existing_schedule is not None:
        existing_schedule._interval_days = interval_days
        return jsonify(existing_schedule.to_json()), 201 # interval_days konnte geupdatet werden -> Erfolg (201)
    
    # Szenario A -> Falls schedule mit diesem care_type aber nicht existiert -> neuen schedule anlegen
    if existing_schedule is None:
        max_id = 0 # aktuell höchste ID

        for schedule in test_plant._schedules:
            if schedule._id > max_id: # falls ID von bestehendem schedule größer als momentane max_id -> neu zuweisen
                max_id = schedule._id
        
        new_id = max_id + 1 # für neuen Plan wieder neue ID

        # jetzt neuen Plan erstellen & in Pflanzenliste speichern
        new_schedule = CareSchedule(new_id, plant_id, care_type, interval_days, None)

        test_plant._schedules.append(new_schedule)

        return jsonify(new_schedule.to_json()), 201 # neuer Plan wurde erfolgreich hinzugefügt


# Route für Endpoint GET /api/plants/<id>/schedules
@app.route('/api/plants/<int:plant_id>/schedules', methods=['GET'])
def get_plant_schedules(plant_id: int) -> Response:
    


if __name__ == "__main__": # damit App aufgerufen werden kann mit Port 5000
    app.run(debug=True, port=5000) 