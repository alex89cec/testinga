import os
import requests
import json

tokenSfx = os.getenv("SFX_AUTH_TOKEN")
headerSfx = "X-SF-TOKEN"
baseUrl = "https://api.us1.signalfx.com/v2"
header = ['name', 'DashboardGroup', 'creator']
data = []


def get_users():
    response = requests.get(baseUrl + "/organization/member", headers={headerSfx: tokenSfx})
    return json.loads(response.text)["results"]


def get_dashboards():
    offset = 0
    limit = 100
    results = []
    while True:
        response = requests.get(f"{baseUrl}/dashboard?limit={limit}&offset={offset}", headers={headerSfx: tokenSfx})
        response.raise_for_status()
        answer = json.loads(response.text)
        results += answer["results"]
        offset += limit
        if offset >= answer["count"]:
            break

    # Remove charts that does not have charts?
    return list(filter(lambda x: len(x["charts"]) > 0, results))


def get_name(users, id):
    if "AAAAAAAAAAA" == id:
        return "SignalFx Created"

    found_user = next((u["fullName"] for u in users if u["userId"] == id), None)
    return found_user if found_user else f"User not found {id}"


users = get_users()
dashboards = get_dashboards()
print(f"We have {len(dashboards)} dashboards to migrate")
for dashboard in dashboards:
    creator_name = get_name(users, dashboard['creator'])
    directory = f"./dashboards/{creator_name}"
    print(f"{dashboard['name']},{dashboard['groupName']},{creator_name}")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{dashboard['name']}.json", 'w') as outfile:
        outfile.write(json.dumps(dashboard))
