from pdpyras import APISession, PDClientError, EventsAPISession
from os import environ as ENV

import twitter


SERVICE_NAME="PDSummit Twitter Service"
PagerDutyAPISession = APISession(ENV.get('PAGERDUTY_REST_API_KEY'))

def startup():
    print("doing startup things.")
    service_id = create_or_get_service_id()
    print (f"Service ID: {service_id}")
    integration_key = get_or_create_events_v2_integration_key(service_id)
    print (f"Integration Key: {integration_key}")
    twitter_statuses = twitter.query_twitter()
    send_twitter_statuses_to_events_API(integration_key, twitter_statuses)


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
        print(e.msg)

def get_or_create_events_v2_integration_key(service_id):
    print ("creating events integration")
    try:
        service = PagerDutyAPISession.rget(
            f'/services/{service_id}'
        )
        if len(service['integrations']) >= 1:
            integration_id = service['integrations'][0]['id']
            integration = PagerDutyAPISession.rget(
                f'/services/{service_id}/integrations/{integration_id}'
            )
        elif len(service['integrations']) == 0:
            # create a new integration
            integration = PagerDutyAPISession.rpost(
                f'/services/{service_id}/integrations',
                json={
                    "integration": {
                        "type": "events_api_v2_inbound_integration",
                        "name": "EventsV2",
                        "service": {
                            "id": service_id,
                            "type": "service_reference"
                        },
                    }
                }
            )
        return integration['integration_key']
    except PDClientError as e:
        print(e.msg)

def send_twitter_statuses_to_events_API(integration_key, statuses):
    session = EventsAPISession(integration_key)

    for status in statuses:
        print("Triggering on Events API")
        response = session.trigger(
            f"Matching tweet from user @{status['user']['screen_name']}",
            'twitter.com',
            severity='info',
            custom_details=status)
        print(response)
    ## Next
    ## Send each event with 'trigger' type
    ## Make an event rule to suppress alerts created by these events that don't contain our magic word.
    ## See: https://support.pagerduty.com/docs/event-management#section-event-rules
