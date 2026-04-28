from fastapi import FastAPI, Query
from ...services.engine import simulate_plan

app = FastAPI(title='Live Ads Personalization Engine')

@app.get('/')
def root():
    return {'message': 'Live Ads Personalization Engine is running.'}

@app.get('/simulate')
def simulate(segment: str = Query('sports fans'), context: str = Query('live sports'), slots: int = Query(5)):
    return simulate_plan(segment, context, slots)
