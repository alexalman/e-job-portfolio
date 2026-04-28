from fastapi import FastAPI
from pydantic import BaseModel
from ...services.generator import generate_campaign

app = FastAPI(title="Streaming Ad Creative Studio")

class CampaignRequest(BaseModel):
    brand: str
    product: str
    audience: str
    goal: str
    context: str = "streaming"

@app.get("/")
def root():
    return {"message": "Streaming Ad Creative Studio is running."}

@app.post("/generate")
def generate(req: CampaignRequest):
    return generate_campaign(req.model_dump())
