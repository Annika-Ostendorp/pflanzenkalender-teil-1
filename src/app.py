from flask import Flask, jsonify, request, Response

app = Flask(__name__)

plants = []

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