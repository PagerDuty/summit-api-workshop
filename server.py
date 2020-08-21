from os import environ as ENV
from flask import Flask
from dotenv import load_dotenv
from pdpyras import APISession, PDClientError

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

@app.route('/get-escalation-policy', methods=['GET'])
def test_get_ep_route():
    session = APISession(ENV.get('PAGERDUTY_REST_API_KEY'))
    try:
        ep = session.rget(
            '/escalation_policies',
            params={'query': 'Default'})
        return f"EP {ep}."
    except PDClientError as e:
        return e.msg

@app.route('/create-service', methods=['GET'])
def test_create_service_route():
    session = APISession(ENV.get('PAGERDUTY_REST_API_KEY'))

    # Using requests.Session.get:
    try:
        service = session.rpost(
            '/services',
            json={
                'name': '#PDSummit Twitter',
                'type': 'service',
                'description': 'hey',
                "escalation_policy": {
                    "id": "P7U5VP4",
                    "type": "escalation_policy_reference"
                },
                "alert_creation": "create_alerts_and_incidents"
            })
        return f"Service {service}."
    except PDClientError as e:
        return e.msg


if __name__ == "__main__":
    app.run(debug=True)
