import time

from requests.exceptions import HTTPError
from sodapy import Socrata


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofchicago.org", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofchicago.org,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.


print("Fetching NYC complaint data...", flush=True)
for attempt in range(3):
    try:
        results = client.get("4ijn-s7e5", limit=5)
        break
    except HTTPError as error:
        status = error.response.status_code if error.response is not None else None
        if status not in {500, 502, 503, 504} or attempt == 2:
            raise

        delay = 2**attempt
        print(f"Socrata returned HTTP {status}; retrying in {delay}s...", flush=True)
        time.sleep(delay)

print(results, flush=True)