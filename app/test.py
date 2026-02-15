from dotenv import load_dotenv
import os
from mygeotab import API

load_dotenv()
api = API(
    username=os.getenv("GEOTAB_USERNAME"),
    password=os.getenv("GEOTAB_PASSWORD"),
    database=os.getenv("GEOTAB_DATABASE"),
    server=os.getenv("GEOTAB_SERVER")
)
api.authenticate()
devices = api.get("Device")
print("AUTH OK. Devices:", len(devices))