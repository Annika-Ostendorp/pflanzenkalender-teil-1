from flask import Flask, jsonify, request, Response

app = Flask(__name__)

plants = []

# Route für Endpoint POST /api/plants
@app.route('/api/plants', methods=['POST'])
def create_plant() -> Response:
    new_plant = request.get_json()
    plants.append(new_plant) # neue Pflanze zur Liste hinzufügen
    return jsonify(new_plant), 201