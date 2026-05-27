import requests
import time

BASE_URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"
LIMIT = 100

def collecter_tout(dataset_id, select=None, where=None, group_by=None, pause=0.2):
    url = f"{BASE_URL}/{dataset_id}/records"
    records = []
    offset = 0

    while True:
        params = {"limit": LIMIT, "offset": offset}

        if select:
            params["select"] = select
        if where:
            params["where"] = where
        if group_by:
            params["group_by"] = group_by

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        records.extend(data["results"])

        if len(records) >= data["total_count"]:
            break

        offset += LIMIT
        time.sleep(pause)

    return records