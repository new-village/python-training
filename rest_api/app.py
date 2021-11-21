""" app.py
"""
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Sentence(BaseModel):
    text: str


@app.get('/')
def search_trades():
    return {'details': 'This site is api of real estate collection based on mlti.'}


@app.get('/{city_id}/{year}')
def get_estate_trades(city_id: str, year: str):
    return {'city_id': city_id, 'year': year}


if __name__ == '__main__':
    uvicorn.run(app)