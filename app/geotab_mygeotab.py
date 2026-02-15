import os
from dotenv import load_dotenv, find_dotenv
from mygeotab import API

load_dotenv(find_dotenv())

def get_api() -> API:
    server = os.getenv("GEOTAB_SERVER")
    database = os.getenv("GEOTAB_DATABASE")
    username = os.getenv("GEOTAB_USERNAME")
    password = os.getenv("GEOTAB_PASSWORD")

    if not all([server, database, username, password]):
        raise RuntimeError("Missing GEOTAB_* env vars. Check your .env in the repo root.")

    api = API(username=username, password=password, database=database, server=server)
    api.authenticate()
    return api
