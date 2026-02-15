from datetime import datetime, timedelta, timezone
from collections import defaultdict
from app.geotab_mygeotab import get_api

def _to_dt(x):
    # mygeotab may return str or datetime
    if hasattr(x, "tzinfo"):
        return x
    return datetime.fromisoformat(str(x).replace("Z", "+00:00"))

def stopped_time_leaderboard(days=7, top_n=5, speed_threshold=1, max_gap_seconds=600):
    days = int(days)
    top_n = int(top_n)
    speed_threshold = float(speed_threshold)
    max_gap_seconds = int(max_gap_seconds)

    api = get_api()
    since = datetime.now(timezone.utc) - timedelta(days=days)

    devices = api.get("Device")
    device_name = {d["id"]: d.get("name", str(d["id"])) for d in devices}

    logs = api.get(
        "LogRecord",
        search={"fromDate": since.isoformat()},
        resultsLimit=int(50000),  # bump up; demo is fine
    )

    by_device = defaultdict(list)
    for r in logs:
        by_device[r["device"]["id"]].append(r)

    stopped_seconds = defaultdict(float)

    for dev_id, recs in by_device.items():
        recs.sort(key=lambda x: x["dateTime"])
        for i in range(1, len(recs)):
            prev = recs[i - 1]
            cur = recs[i]

            prev_t = _to_dt(prev["dateTime"])
            cur_t = _to_dt(cur["dateTime"])
            dt = (cur_t - prev_t).total_seconds()

            # ignore huge gaps
            if dt <= 0 or dt > max_gap_seconds:
                continue

            prev_speed = prev.get("speed")
            if isinstance(prev_speed, (int, float)) and prev_speed <= speed_threshold:
                stopped_seconds[dev_id] += dt

    ranked = sorted(stopped_seconds.items(), key=lambda x: x[1], reverse=True)

    leaders = [{
        "deviceId": d,
        "deviceName": device_name.get(d, str(d)),
        "stoppedSeconds": int(s),
        "stoppedMinutes": round(s / 60, 1),
    } for d, s in ranked[:top_n]]

    return {
        "days": days,
        "log_records_used": len(logs),
        "speed_threshold": speed_threshold,
        "leaders": leaders,
        "note": "Stopped-time proxy computed from LogRecord speed <= threshold. Demo DB does not expose ignition in LogRecord."
    }
