from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from agents.master_agent import MasterAgent
from pydantic import BaseModel
import os

app = FastAPI(title="Kano API Gateway")
master = MasterAgent()

API_KEY = os.getenv("KANO_API_KEY", "kano_default_secure_key")
api_key_header = APIKeyHeader(name="X-KANO-API-KEY")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

class TaskRequest(BaseModel):
    prompt: str
    approved: bool = False

@app.post("/execute")
async def execute_task(request: TaskRequest, api_key: str = Depends(get_api_key)):
    result = master.run(request.prompt, request.approved)
    return {"result": result}

@app.get("/status")
async def get_status(api_key: str = Depends(get_api_key)):
    return {"status": "Online", "agents": ["Master", "Coder", "Security", "Browser", "Roadmap"]}
