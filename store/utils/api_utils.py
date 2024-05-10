import requests


def get_client_gender(client_name: str) -> str:
    data = requests.get(f"https://api.genderize.io/?name={client_name}")
    client_gender = data.json()["gender"]
    return client_gender


def get_client_nationality(client_name: str) -> str:
    data = requests.get(f"https://api.nationalize.io/?name={client_name}")
    max_potential_country = -1

    for d in data.json()["country"]:
        if max_potential_country < d["probability"]:
            max_potential_country = d["probability"]
            client_nationality = d["country_id"]
    return client_nationality
