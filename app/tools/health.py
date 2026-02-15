from app.geotab_client import GeotabClient

async def health_check():
    client = GeotabClient()
    devices = await client.call("Get", {"typeName": "Device", "resultsLimit": 5})
    return {"ok": True, "sample_device_count": len(devices)}
