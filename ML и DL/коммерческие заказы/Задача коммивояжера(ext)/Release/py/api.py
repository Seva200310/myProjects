from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from geoFind import finder

import json

class Item(BaseModel):
    listcity: list
    mode: bool

apikey='5b3ce3597851110001cf62484e7802db91ae467bb71ccb306c00424a'

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/items/")
async def create_item(item: Item):
    print('--------------------------------------------------')
    apikey='5b3ce3597851110001cf62484e7802db91ae467bb71ccb306c00424a'
    try:
        url_get=finder(apikey,dict(item)['listcity'],dict(item)['mode'])
        otvet=url_get.main()
        print(url_get.__dict__)
    except:
        otvet='somethingWrong'
    return otvet
