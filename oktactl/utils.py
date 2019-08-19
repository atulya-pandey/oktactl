import os

def get_creds():
    okta_dir = os.path.expanduser("~/.okta_cli")
    f = open("{}/credentials".format(okta_dir), "r")
    domain_name = f.readline().split(": ")[1].strip()
    api_token = f.readline().split(": ")[1]
    f.close()

    return domain_name, api_token

def get_api_info():
    domain_name, api_token = get_creds()
    base_url = "https://{}/api/v1".format(domain_name)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "SSWS {}".format(api_token)
    }
    return base_url, headers
