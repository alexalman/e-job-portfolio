from fastapi import FastAPI, Query
from ...services.engine import recommend

app = FastAPI(title='Unified Recommendation & Conversion Engine')

@app.get('/')
def root():
    return {'message': 'Unified Recommendation & Conversion Engine is running.'}

@app.get('/recommend')
def rec(interest: str = Query('space adventure')):
    return recommend(interest)
