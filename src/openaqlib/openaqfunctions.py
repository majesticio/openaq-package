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


def get_latest_data(id):
    """
    Get the latest data by passing a location_id (sensor ID) as
    the argument.
    """

    url = f"https://api.openaq.org/v2/latest/{id}"
    response = requests.get(url)

    if response.status_code != 200:
        return print("bad request; status code: ", response.status_code)

    data = response.json()["results"]

    df = pd.DataFrame(data)
    df = pd.concat(
        [df.drop(["coordinates"], axis=1), df["coordinates"].apply(pd.Series)], axis=1
    )
    df_measurements = pd.json_normalize(df["measurements"].explode())
    df = pd.concat([df.drop(["measurements"], axis=1), df_measurements], axis=1)
    df.fillna(method="ffill", inplace=True)

    return df


def location_data_from_dates(location_id, start, end):
    """
    Pass the function the location_id, starting date, ending date.
    Returns a dataframe.Dates must be in the ISO-8601 date time + offset format
    e.g.2000-01-01T00:00:00+00:00, which is January 1 2000 12:00 AM at UTC.
    Will default to UTC if passed e.g. YYYY-MM-DD. If too much data is returned
    it will time out or throw an error code.
    """
    q = {
        "location_id": f"{location_id}",
        "date_from": f"{start}",
        "date_to": f"{end}",
        "limit": 10000,  # max is 10000
    }
    base_url = "https://api.openaq.org/v2/measurements"
    response = requests.get(base_url, params=q)

    if response.status_code != 200:
        return print("bad request; status code: ", response.status_code)

    data = response.json()["results"]

    neat = [
        {
            "Date": row["date"]["local"],
            "Parameter": row["parameter"],
            "Value": row["value"],
            "Unit": row["unit"],
        }
        for row in data
    ]

    df = pd.DataFrame.from_dict(neat)
    # df['Datetime'] = pd.to_datetime(df['Date']) #uncomment for datetime object column
    # df.drop(['Date'], axis=1,inplace=True)

    return df
