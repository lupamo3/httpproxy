import requests
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from jose import jwt
from jose.backends import RSAKey
from datetime import datetime

requests_processed = 0
start_time = datetime.now()


app = Flask(__name__)
secret = "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf"

def generate_nonce():
    return str(uuid.uuid4())

@app.route("/", methods=["POST"])
def proxy():
    
    global requests_processed
    requests_processed += 1
    # Get the current timestamp
    iat = int(datetime.utcnow().timestamp())
    # Generate a unique nonce
    jti = generate_nonce()
    # Get the JSON payload
    payload = request.get_json(silent=True, cache=True)
    print("sho payload", payload)
    # Add the iat, jti, and payload claims to the payload
    payload["iat"] = iat
    payload["jti"] = jti
    username = payload['username']
    payload["payload"] = {"user": username, "date": datetime.today().strftime('%Y-%m-%d')}
    print("payload full", payload)
    # Sign the payload with the secret
    token = jwt.encode(payload, secret, algorithm='HS512')
    # Forward the request to the upstream endpoint
    headers = {'x-my-jwt': token}
    response = requests.post('https://reqres.in/api/register', json=payload, headers=headers)
    # Return the response
    return jsonify(response.json())

@app.route("/status")
def status():
    # Return the time from start and the number of requests processed
    current_time = datetime.now()
    uptime = current_time - start_time
    return jsonify(requests_processed=requests_processed, uptime=str(uptime))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)