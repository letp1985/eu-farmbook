import os
import requests
from dotenv import load_dotenv


# get environment variables
load_dotenv()
API_ADDRESS = os.environ.get("API_ADDRESS")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


def get_api_status():
    """
    Get the status of the API. Should return "OK"
    """
    url = f"{API_ADDRESS}/api/status/db_status"
    response = requests.get(
        url
    )
    return response.json()


def get_token():
    """
    Gets the access, refresh and user ID for the user based on the e-mail and password
    """
    url = f"{API_ADDRESS}/api/authentication/token/"
    response = requests.post(
        url,
        json={"email": EMAIL, "password": PASSWORD}
    )
    if response.status_code != 200:
        raise Exception(f"Could not get token: Status code: {response.status_code}: {response.json()}")
    else:
        return response.json()


def get_projects():
    """
    Uses the token to get the projects that the user is registered for
    """
    url = f"{API_ADDRESS}/api/authentication/projects/"

    token = get_token()
    response = requests.post(
        url,
        json=token
    )

    if response.status_code != 200:
        raise Exception(f"Could not access projects: Status code: {response.status_code}: {response.json()}")
    else:
        return response.json()

