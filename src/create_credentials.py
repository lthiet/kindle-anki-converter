import json
import sys

app_id = sys.argv[1]
app_key = sys.argv[2]

obj = {
    "app_id": app_id,
    "app_key": app_key
}
with open("../data/credentials.json", "w") as f:
    json.dump(obj, f, indent=4)
