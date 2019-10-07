import requests
def create_session(config):
    r = requests.post("https://%s/oauth/token" % config["domain"], data = {
            "client_id": config["client_id"],
            "client_secret" : config["client_secret"],
            "audience": "https://%s/api/v2/" % config["domain"],
            "grant_type": "client_credentials"
    })

    token = r.json()["access_token"]
    print("Token is %s" % token)

    s = requests.Session()
    s.headers.update({"Authorization": "Bearer %s" % token})
    return s