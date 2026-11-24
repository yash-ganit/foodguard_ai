
import requests
from pathlib import Path

API_URL = "https://data.cityofchicago.org/resource/4ijn-s7e5.csv"

OUTPUT_FILE = Path(
    "data-engineering/foodguard-ingestion/data/raw/"
    "food_inspections_dev.csv"
)

PARAMS = {
    "$where": "inspection_date >= '2019-01-01T00:00:00'",
    "$limit": 10000,
    "$order": "inspection_date DESC"
}

def download_data():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(
        API_URL,
        params=PARAMS,
        timeout=120
    )

    response.raise_for_status()

    OUTPUT_FILE.write_bytes(response.content)

    print("Download completed!")
    print(f"File: {OUTPUT_FILE}")
    print(f"Size: {len(response.content) / 1024:.2f} KB")

if __name__ == "__main__":
    download_data()
