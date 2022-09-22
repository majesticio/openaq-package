import pandas as pd, requests


def locations_by_coordinates(lat, lon, rad):
    """
    latitude, longitude, radius as args. radius is in meters.
    If data is not returned check coordinates or increase radius!
    If too much data is returned, lower the radius!
    """

    url = f"https://api.openaq.org/v2/locations?coordinates={lat},{lon}&radius={rad}"

    response = requests.get(url)

    if response.status_code != 200:
        return print("bad request; status code: ", response.status_code)

    data = response.json()

    location_id = []

    for i in data["results"]:  # loop through the data and get the location_id and name
        location_id.append({"location_id": i["id"], "name": i["name"]})

    locations = pd.DataFrame.from_dict(location_id)
    return locations
