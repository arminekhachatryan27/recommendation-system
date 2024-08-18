from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    model_name = request.json.get('modelname')
    viewer_id = request.json.get('viewerid')
    random_number = random.randint(1, 100)
    return jsonify({"reason": model_name, "result": random_number})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
