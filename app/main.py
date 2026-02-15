from fastapi import FastAPI, HTTPException
from app.tools.health import health_check
from app.tools.idle import stopped_time_leaderboard
from app.tools.debug import sample_logrecord
from app.tools.debug import inspect_entity
from app.schemas import PlanGroupFromStoppedRequest, ConfirmGroupFromStoppedRequest
from app.tools.groups import plan_group_from_stopped, confirm_group_from_stopped


app = FastAPI(title="FleetCommander AI")

@app.get("/health")
async def health():
    try:
        return await health_check()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/idle-leaderboard")
def leaderboard(days: int = 7, top_n: int = 5, speed_threshold: float = 1):
    try:
        return stopped_time_leaderboard(days=days, top_n=top_n, speed_threshold=speed_threshold)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/debug/logrecord-sample")
def debug_logrecord_sample(days: int = 2, n: int = 5):
    try:
        return sample_logrecord(days=days, n=n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/debug/inspect")
def debug_inspect(type_name: str, n: int = 5, days: int = 7):
    try:
        return inspect_entity(type_name=type_name, n=n, days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/plan/group-from-stopped")
def plan(req: PlanGroupFromStoppedRequest):
    try:
        return plan_group_from_stopped(
            group_name=req.group_name,
            days=req.days,
            top_n=req.top_n,
            speed_threshold=req.speed_threshold
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/confirm/group-from-stopped")
def confirm(req: ConfirmGroupFromStoppedRequest):
    try:
        # ignore req fields, trust token
        return confirm_group_from_stopped(req.confirm_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))