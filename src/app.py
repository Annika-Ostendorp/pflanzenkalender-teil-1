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
        try:
            actual_date = date.fromisoformat(date_str) # Datum hier wieder in date-Objekt umwandeln zur besseren Überprüfung
        
        except ValueError: # fängt falsche Formate ab und gibt 400 Bad Request zurück
            return jsonify({"error": "Bad Request: Invalid date format. Must be YYYY-MM-DD"}), 400
    
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
    for plant in plants:
        if plant._id == plant_id: # hat Pflanzenobjekt diesselbe ID wie die Übergebene?
            plants.remove(plant) # falls ja, dann dieses Objekt löschen
            return '', 204 # erfolgreiches Löschen von Pflanze -> 204 No Content -> leerer String als Body
    
    return jsonify({"error": "Plant not found"}), 404 # falls ID nicht existieren sollte -> Fehlermeldung zurückgeben


# Route für Endpoint GET /api/plants/<id>
@app.route('/api/plants/<int:plant_id>', methods=['GET'])
def get_plants_id(plant_id: int) -> Response: # ähnlicher Aufbau wie bei DELETE route, wo es auch um ID ging
    for plant in plants:
        if plant._id == plant_id:
            return jsonify(plant.to_json()), 200 # spezifische Pflanze existiert --> Erfolg (200) --> enthält bereits schedules und status
        
    return jsonify({"error": "Plant not found"}), 404 # falls ID wieder nicht existiert -> Fehlermeldung


# Route für Endpoint PUT /api/plants/<id>
@app.route('/api/plants/<int:plant_id>', methods=['PUT'])
def update_plant(plant_id: int) -> Response:
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

    # Validierung des care_types einbauen
    allowed_care_types = ["watering", "fertilizing", "repotting"]
    care_type = data.get("care_type")

    if care_type not in allowed_care_types:
        return jsonify({"error": "Bad Request: Invalid care_type"}), 400

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
        new_schedule = CareSchedule(new_id, plant_id, care_type, interval_days)

        test_plant._schedules.append(new_schedule)

        return jsonify(new_schedule.to_json()), 201 # neuer Plan wurde erfolgreich hinzugefügt


# Route für Endpoint GET /api/plants/<id>/schedules
@app.route('/api/plants/<int:plant_id>/schedules', methods=['GET'])
def get_plant_schedules(plant_id: int) -> Response:
    test_plant = None

    # wieder Logik wie bei voriger Route -> existiert Pflanze überhaupt?
    for plant in plants:
        if plant._id == plant_id:
            test_plant = plant
            break
    
    if test_plant is None:
        return jsonify({"error": "Plant not found"}), 404 # Pflanze existiert nicht -> Fehlermeldung (404)

    # alle Pflegepläne mit dieser bestimmten plant_id filtern + in JSON umwandeln
    schedules = []

    for schedule in test_plant._schedules: # jeden schedule einzeln durchgehen und Liste hinzufügen
        schedules.append(schedule.to_json())

    return jsonify(schedules), 200 # neue Liste mit gefilterten schedules (die bestimmte plant_id haben) erfolgreich zurückgegeben


# Route für Endpoint DELETE /api/plants/<id>/schedules/<care_type>
@app.route('/api/plants/<int:plant_id>/schedules/<string:care_type>', methods=['DELETE'])
def delete_plant_schedule(plant_id: int, care_type: str) -> Response:
    test_plant = None

    # wieder Logik wie vorhin -> existiert Pflanze mit spezieller ID überhaupt in Liste?
    for plant in plants:
        if plant._id == plant_id:
            test_plant = plant
            break # Pflanze wurde gefunden -> hier wieder Schleife abbrechen+
    
    # falls trotzdem test_plant weiterhin None --> Fehler
    if test_plant is None:
        return jsonify({"error": "Plant not found"}), 404
    
    # jetzt schauen, ob Pflanze Pflegeplan mit spezifischem care_type besitzt
    specific_schedule = None
    for schedule in test_plant._schedules:
        if schedule._care_type == care_type:
            specific_schedule = schedule
            break # schedule mit spezifischem care_type gefunden -> Schleife kann abgebrochen werden

    if specific_schedule is None: # falls aber dieser Pflegeplan mit spezifischem care_type nicht existiert -> Fehler
        return jsonify({"error": "Care schedule not found"}), 404
    
    # diesen speziellen Pflegeplan dann dauerhaft aus Pflanze entfernen
    test_plant._schedules.remove(specific_schedule)

    return '', 204 # erfolgreich gelöscht (204) -> leerer Body ('')


# Route für Endpoint POST /api/plants/<id>/logs
@app.route('/api/plants/<int:plant_id>/logs', methods=['POST'])
def create_plant_log(plant_id: int) -> Response:
    data = request.get_json()
    test_plant = None

    # wieder gleiche Logik wie bei vorigem DELETE Endpoint
    for plant in plants:
        if plant._id == plant_id:
            test_plant = plant
            break
    
    if test_plant is None: # falls Pflanze nicht existiert -> Fehlermeldung
        return jsonify({"error": "Plant not found"}), 404

    # Validierung von Pflichtfeld care_type und deren Werten -> wie bei POST /api/plants Route oben
    care_type = data.get("care_type")

    if type(care_type) is not str or str(care_type).strip() == "": # fehlt care_type, ist None oder leerer String/ ungültig? -> Fehlermeldung
        return jsonify({"error": "Bad Request: Missing or invalid care_type"}), 400
    
    allowed_care_types = ["watering", "fertilizing", "repotting"]
    if care_type not in allowed_care_types:
        return jsonify({"error": "Bad Request: Invalid care_type"}), 400 # wenn falscher care_type übergeben wird -> nicht einer von den 3 Geforderten entspricht

    # Logik für optionales Attribut performed_at -> speziell das "performed_at" Feld aus data holen
    desired_date_str = data.get("performed_at")
    
    if desired_date_str: # also gültig, kein leerer String o.Ä.
        try:
            actual_date = date.fromisoformat(desired_date_str) # string von zurückgegebenem Datum in richtiges Datum umwandeln -> muss ja Format YYYY-MM-DD haben

        except ValueError:
            return jsonify({"error": "Bad Request: Invalid date format. Must be YYYY-MM-DD"}), 400
    
    else:
        actual_date = date.today() # ansonsten wenn es ungültig ist -> per Default auf heute setzen

    # für neues ActionLog Objekt, auch notes-Feld holen
    notes_str = data.get("notes")

    if not notes_str: # falls keine notes übergeben wurden, trotzdem leerer String -> besserer Überblick über alle möglichen Felder
        notes_str = ""
    
    # wieder wie vorhin mit max_id für eindeutige ID für neuen Log
    max_id = 0
    for log in test_plant._logs:
        if log._id > max_id:
            max_id = log._id
    
    new_log_id = max_id + 1 # für neuen Eintrag wieder neue ID

    # neues ActionLog-Objekt erstellen und hinzufügen
    new_log = ActionLog(new_log_id, plant_id, care_type, actual_date, notes_str)
    test_plant._logs.append(new_log)

    return jsonify(new_log.to_json()), 201 # neuer Log-Eintrag erfolgreich zurückgegeben


# Route für Endpoint GET /api/plants/<id>/logs
@app.route('/api/plants/<int:plant_id>/logs', methods=['GET'])
def get_plants_logs(plant_id: int) -> Response:
    test_plant = None

    # wieder prüfen, ob Pflanze überhaupt existiert
    for plant in plants:
        if plant._id == plant_id:
            test_plant = plant
            break

    if test_plant is None:
        return jsonify({"error": "Plant not found"}), 404 # Pflanze existiert nicht -> Fehler 404

    # Logs für spezielle plant_id holen & in JSON umwandeln
    unsorted_logs = [log.to_json() for log in test_plant._logs]
    sorted_logs = []

    # jetzt logs in Reihenfolge mit absteigendem Datum sortieren
    while len(unsorted_logs) > 0:
        newest_log = unsorted_logs[0] # 1. momentaner Log ist Startpunkt -> mit diesem nun alle anderen Logs vergleichen & sortieren

        for log in unsorted_logs:
            if log["performed_at"] > newest_log["performed_at"]:
                newest_log = log # neues Datum neu zuweisen, wenn es aktueller ist als momentan "höchstes" gefundenes

        sorted_logs.append(newest_log) # neustes Datum in neue Liste hinzufügen und dann aus alter löschen
        unsorted_logs.remove(newest_log)

    return jsonify(sorted_logs), 200 # sortierte Liste mit allen Logs erfolgreich zurückgegeben


# Route für Endpoint GET /api/plants/<id>/next-actions
@app.route('/api/plants/<int:plant_id>/next-actions', methods=['GET'])
def get_plant_next_actions(plant_id: int) -> Response:
    test_plant = None

    # wieder prüfen, ob Pflanze existiert
    for plant in plants:
        if plant._id == plant_id:
            test_plant = plant
            break

    if test_plant is None:
        return jsonify({"error": "Plant not found"}), 404
    
    unsorted_actions = []
    today = date.today()

    for schedule in test_plant._schedules:
        # jetzt haben wir ja neuen next_due-Property-Dekorator aus früherem Bugfix (stored-next-due-issue)
        # entweder basierend auf letztem ActionLog oder falls kein Log existiert, basierend auf dem Erstellungsdatum
        schedule._plant = test_plant # Testpflanze zuweisen, damit man auf Property-Dekorator zugreifen kann

        next_due_date = schedule.next_due

        days_until = (next_due_date - today).days # mit .days Anzahl der Tage zwischen zwei bestimmten Daten berechnen

        is_overdue = next_due_date < today # prüfen, dass Aktionen, die genau heute fällig sind nicht overdue sind

        action_log_object = {
            "care_type": schedule._care_type,
            "interval_days": schedule._interval_days,
            "next_due": next_due_date.isoformat(),
            "days_until": days_until,
            "overdue": is_overdue
        }

        unsorted_actions.append(action_log_object)

    sorted_actions = [] # wieder Sortiermechanismus wie bei voriger POST Route
    
    while len(unsorted_actions) > 0:
        soonest_action = unsorted_actions[0] # wieder 1. Aktion als Startpunkt
        
        for action in unsorted_actions:
            if action["next_due"] < soonest_action["next_due"]: # aufsteigend sortieren -> je älter das Datum, desto dringender ist Aktion
                soonest_action = action
        
        sorted_actions.append(soonest_action)
        unsorted_actions.remove(soonest_action)
    
    return jsonify(sorted_actions), 200 # fertig sortierte Liste erfolgreich zurückgeben


 # Route für Endpoint GET /api/overdue
@app.route('/api/overdue', methods=['GET'])
def get_all_overdue_tasks() -> Response: 
    unsorted_overdue = []
    today = date.today()

    # Globaler Filter der alle Pflanzen & Pläne durchgeht
    for plant in plants:
        for schedule in plant._schedules:
            schedule._plant = plant # Pflegeplan aktuelle Pflanze zuweisen -> damit dann next_due Property verwenden kann
            next_due_date = schedule.next_due

            if next_due_date < today: # filtern, ob Aktion bereits überfällig ist
                days_overdue = (today - next_due_date).days # wieder wie vorhin Tage berechnen, die die Aktion schon überfällig ist
               
                overdue_object = { # mit Feldern nach Projektbeschreibung
                    "plant_id": plant._id,
                    "plant_name": plant._name,
                    "plant_location": plant._location,
                    "care_type": schedule._care_type,
                    "next_due": next_due_date.isoformat(), # wieder in gültiges "YYYY-MM-DD" umwandeln
                    "days_overdue": days_overdue
                }
    
                unsorted_overdue.append(overdue_object)

    # Absteigende Sortierung nach days_overdue
    sorted_overdue = []
    while len(unsorted_overdue) > 0:
        most_overdue = unsorted_overdue[0] # wieder gleiche Logik wie vorige Route

        for action in unsorted_overdue:
            if action["days_overdue"] > most_overdue["days_overdue"]: # falls aktuelle Aktion mehr Tage überfällig ist -> kommt an neue erste Stelle
                most_overdue = action

        sorted_overdue.append(most_overdue)
        unsorted_overdue.remove(most_overdue)

    return jsonify(sorted_overdue), 200


if __name__ == "__main__": # damit App aufgerufen werden kann mit Port 5000
    app.run(debug=True, port=5000) 