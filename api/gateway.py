from fastapi import FastAPI, BackgroundTasks
from agents.master_agent import MasterAgent
from pydantic import BaseModel

app = FastAPI(title="Kano API Gateway")
master = MasterAgent()

class TaskRequest(BaseModel):
    prompt: str
    approved: bool = False

@app.post("/execute")
async def execute_task(request: TaskRequest):
    result = master.run(request.prompt, request.approved)
    return {"result": result}

@app.get("/status")
async def get_status():
    return {"status": "Online", "agents": ["Master", "Coder", "Security", "Browser", "Roadmap"]}
