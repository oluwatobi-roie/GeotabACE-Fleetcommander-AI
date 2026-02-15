import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEOTAB_SERVER = os.getenv("GEOTAB_SERVER")
GEOTAB_DATABASE = os.getenv("GEOTAB_DATABASE")
GEOTAB_USERNAME = os.getenv("GEOTAB_USERNAME")
GEOTAB_PASSWORD = os.getenv("GEOTAB_PASSWORD")

if not all([GEOTAB_SERVER, GEOTAB_DATABASE, GEOTAB_USERNAME, GEOTAB_PASSWORD]):
    raise RuntimeError("Missing GEOTAB_* env vars. Check your .env file in repo root.")

BASE_URL = f"https://{GEOTAB_SERVER}/apiv1"


class GeotabClient:
    def __init__(self):
        self.credentials = None

    async def authenticate(self):
        payload = {
            "method": "Authenticate",
            "params": {
                "database": GEOTAB_DATABASE,
                "userName": GEOTAB_USERNAME,
                "password": GEOTAB_PASSWORD,
            },
        }

        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(BASE_URL, json=payload)
            # If auth fails, Geotab often returns 200 with an "error" field.
            data = res.json()

            if "error" in data:
                raise RuntimeError(f"Geotab auth error: {data['error']}")

            self.credentials = data["result"]["credentials"]

    async def call(self, method: str, params: dict | None = None):
        if not self.credentials:
            await self.authenticate()

        payload = {
            "method": method,
            "params": {
                "credentials": self.credentials,
            },
        }
        if params:
            payload["params"].update(params)

        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(BASE_URL, json=payload)
            data = res.json()

            if "error" in data:
                raise RuntimeError(f"Geotab API error: {data['error']}")

            return data["result"]
