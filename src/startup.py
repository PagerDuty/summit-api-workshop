from pdpyras import APISession, PDClientError
from os import environ as ENV


SERVICE_NAME="PDSummit Twitter Service"
PagerDutyAPISession = APISession(ENV.get('PAGERDUTY_REST_API_KEY'))

def startup():
    print("doing startup things.")
    service_id = create_or_get_service_id()
    print (f"Service ID: {service_id}")


def create_or_get_service_id():
    print("Create or get Services.")
    escalation_policy_id = get_default_escalation_policy_id()
    try:
        service = PagerDutyAPISession.rget(
            '/services',
            params={'query': SERVICE_NAME}
        )
        if len(service) == 1:
            print ("Service already exists.")
            return service[0]['id']
        elif len(service) == 0:
            print ('Create service.')
            #create service
            new_service = PagerDutyAPISession.rpost(
                '/services',
                json={
                    'name': SERVICE_NAME,
                    'type': 'service',
                    'description': 'hey',
                    "escalation_policy": {
                        "id": escalation_policy_id,
                        "type": "escalation_policy_reference"
                    },
                    "alert_creation": "create_alerts_and_incidents"
                })
            return new_service['id']
    except PDClientError as e:
        print(e.msg)

def get_default_escalation_policy_id():
    print("Get default Escalation Policy")
    try:
        escalation_policy = PagerDutyAPISession.rget(
            '/escalation_policies',
            params={'query': 'Default'})
        if len(escalation_policy) == 1:
            return escalation_policy[0]['id']
        else:
            raise Exception
    except PDClientError as e:
        return e.msg
