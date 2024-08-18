from flask import Flask, request, jsonify
import requests
import redis
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# Setup Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Local Cache (Note: LRU cache does not have TTL)
def get_recommendations_from_cache(viewerid):
    return r.get(viewerid)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    viewerid = data.get('viewerid')  # Use 'viewerid' as per your Postman test

    # Check local cache first
    recommendations = get_recommendations_from_cache(viewerid)
    if recommendations:
        return jsonify(json.loads(recommendations))

    # If not in cache, run cascade
    recommendations = runcascade(viewerid)
    r.setex(viewerid, 10, json.dumps(recommendations))  # Set cache with TTL
    return jsonify(recommendations)

def runcascade(viewerid):
    models = ['ModelA', 'ModelB', 'ModelC', 'ModelD', 'ModelE']
    results = {}
    
    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor() as executor:
        future_to_model = {executor.submit(get_recommendation, model, viewerid): model for model in models}
        for future in as_completed(future_to_model):
            model = future_to_model[future]
            try:
                results[model] = future.result()  # Store the result
            except Exception as exc:
                print(f'Model {model} generated an exception: {exc}')
                results[model] = None  # Optional: Set a fallback for failed requests
    
    return results

def get_recommendation(model, viewerid):
    response = requests.post(f'http://generator-service:5000/generate', json={'modelname': model, 'viewerid': viewerid})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json().get('result')  # Return the generated result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
