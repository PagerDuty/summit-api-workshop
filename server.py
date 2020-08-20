from os import environ as ENV
from flask import Flask
from dotenv import load_dotenv
from pdpyras import APISession

load_dotenv()
app = Flask(__name__)

@app.route('/hello-world', methods=['GET'])
def hello_world_route():
    return f"Hello, World. {ENV.get('TEST_KEY')}"

@app.route('/test-pdpyras', methods=['GET'])
def test_pdpyras_route():
    session = APISession(ENV.get('PAGERDUTY_REST_API_KEY'))

    # Using requests.Session.get:
    response = session.get('/users?total=true')
    if response.ok:
        total_users = response.json()['total']
        return f"Account has {total_users} users."

if __name__ == "__main__":
    app.run(debug=True)
