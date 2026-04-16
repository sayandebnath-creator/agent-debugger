from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import DebugAgent

app = FastAPI()
agent = DebugAgent()

class DebugRequest(BaseModel):
    code: str
    error: str

@app.post("/debug")
def debug(req: DebugRequest):
    result = agent.debug_code(req.code, req.error)
    return {"result": result}