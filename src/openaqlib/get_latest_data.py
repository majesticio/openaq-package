import pandas as pd, requests


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
