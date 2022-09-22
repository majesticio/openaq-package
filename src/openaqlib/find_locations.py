import pandas as pd, requests


def find_locations(city, country):
    """
    Pass desired city, country code as args to get a df of sensor location_id's
    and their names.
    """

    queries = {"country": f"{country}", "city": f"{city}"}  # country code

    base_url = "https://api.openaq.org/v2/locations"

    response = requests.get(base_url, params=queries)  # .json()
    if response.status_code != 200:
        return print("bad request; status code: ", response.status_code)

    data = response.json()

    location_id = []

    for i in data["results"]:  # loop through the data and get the location_id and name
        location_id.append({"location_id": i["id"], "name": i["name"]})

    locations = pd.DataFrame.from_dict(location_id)
    return locations
