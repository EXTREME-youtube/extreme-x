from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary storage for scores (replace this with a database for production)
scores = {}

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    if 'player' in data and 'score' in data:
        scores[data['player']] = data['score']
        return jsonify({"message": "Score submitted successfully!"}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route('/get_score/<player>', methods=['GET'])
def get_score(player):
    if player in scores:
        return jsonify({"player": player, "score": scores[player]}), 200
    return jsonify({"error": "Player not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
