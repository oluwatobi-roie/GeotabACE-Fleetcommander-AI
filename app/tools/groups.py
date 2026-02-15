import secrets
from app.geotab_mygeotab import get_api
from app.tools.idle import stopped_time_leaderboard

# in-memory token store (fine for hackathon demo)
_CONFIRM_STORE = {}

def plan_group_from_stopped(group_name: str, days: int, top_n: int, speed_threshold: float):
    report = stopped_time_leaderboard(days=days, top_n=top_n, speed_threshold=speed_threshold)

    leaders = report["leaders"]
    if not leaders:
        raise RuntimeError("No leaderboard results to build a group from.")

    device_ids = [x["deviceId"] for x in leaders]

    token = secrets.token_urlsafe(16)
    _CONFIRM_STORE[token] = {
        "group_name": group_name,
        "device_ids": device_ids,
        "report": report
    }

    preview = {
        "action": "create_group_and_assign_devices",
        "group_name": group_name,
        "device_count": len(device_ids),
        "devices": leaders,
        "explanation": "Selected top devices by stopped-time proxy (speed <= threshold).",
        "confirm_token": token
    }

    return preview

def confirm_group_from_stopped(confirm_token: str):
    if confirm_token not in _CONFIRM_STORE:
        raise RuntimeError("Invalid or expired confirm_token.")

    payload = _CONFIRM_STORE.pop(confirm_token)
    group_name = payload["group_name"]
    device_ids = payload["device_ids"]

    api = get_api()

    # 1) Create group
    group = api.add("Group", {"name": group_name})
    group_id = group["id"]

    # 2) Assign devices to group by setting their groups list
    # We fetch each device, append group, then set.
    updated = 0
    for dev_id in device_ids:
        device = api.get("Device", search={"id": dev_id})[0]
        groups = device.get("groups", [])

        # avoid duplicates
        if not any(g.get("id") == group_id for g in groups):
            groups.append({"id": group_id})
            api.set("Device", {"id": dev_id, "groups": groups})
            updated += 1

    return {
        "ok": True,
        "group": {"id": group_id, "name": group_name},
        "devices_assigned": updated,
        "device_ids": device_ids
    }
