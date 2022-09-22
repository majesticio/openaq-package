import pandas as pd, requests


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
