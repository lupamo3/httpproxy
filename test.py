import json
import time

def test_proxy():
    # Send a POST request to the proxy
    response = requests.post('http://localhost:8000', json={"test": "data"})

    # Assert that the response is successful
    assert response.status_code == 200

    # Assert that the response contains a valid JWT in the x-my-jwt header
    assert 'x-my-jwt' in response.headers
    try:
        jwt.decode(response.headers['x-my-jwt'], secret, algorithms=['HS512'])
    except jwt.exceptions.InvalidSignatureError:
        assert False

    # Assert that the response contains the expected JSON payload
    response_data = json.loads(response.text)
    assert 'test' in response_data
    assert response_data['test'] == 'data'