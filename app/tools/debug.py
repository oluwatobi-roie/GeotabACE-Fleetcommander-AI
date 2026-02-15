from datetime import datetime, timedelta, timezone
from app.geotab_mygeotab import get_api

def sample_logrecord(days: int = 2, n: int = 5):
    api = get_api()
    since = datetime.now(timezone.utc) - timedelta(days=int(days))

    logs = api.get(
        "LogRecord",
        search={"fromDate": since.isoformat()},
        resultsLimit=int(n),
    )

    # Return only keys + a few values so we can see the structure
    samples = []
    for r in logs:
        samples.append({
            "keys": sorted(list(r.keys())),
            "dateTime": r.get("dateTime"),
            "speed": r.get("speed"),
            "ignition": r.get("ignition"),
            "device": r.get("device"),
            "latitude": r.get("latitude"),
            "longitude": r.get("longitude"),
        })

    return {"sample_count": len(samples), "samples": samples}



SUPPORTED_FROMDATE = {"LogRecord", "Trip", "StatusData", "ExceptionEvent", "FaultData"}

def inspect_entity(type_name: str, n: int = 5, days: int = 7):
    api = get_api()
    type_name = str(type_name)
    n = int(n)
    days = int(days)

    search = {}
    if type_name in SUPPORTED_FROMDATE:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        search["fromDate"] = since.isoformat()

    items = api.get(type_name, search=search if search else None, resultsLimit=n)

    if not items:
        return {"type": type_name, "count": 0, "message": "No records returned."}

    # summarize keys frequency
    key_counts = {}
    for it in items:
        for k in it.keys():
            key_counts[k] = key_counts.get(k, 0) + 1

    sample = items[0]
    return {
        "type": type_name,
        "returned": len(items),
        "keys_in_sample": sorted(list(sample.keys())),
        "key_presence_in_returned": dict(sorted(key_counts.items(), key=lambda x: x[0])),
        "sample_record": sample
    }