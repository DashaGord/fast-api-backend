import os
from datetime import date

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import AvailableRoomsResponse
from service import getAvailableRooms
from sqlalchemy import create_engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/available_rooms/", response_model=AvailableRoomsResponse)
def available_rooms(
        date_in: date,
        date_out: date,
        price_from: int,
        price_to: int,
        bedrooms: int = None,
        beds: int = None,
        bathrooms: int = None,

        breakfast: bool = None,
        desk: bool = None,
        baby_chair: bool = None,
        crib: bool = None,
        tv: bool = None,
        shampoo: bool = None,
        corridor: bool = None,
        disabled: bool = None,
        smoke: bool = None,
        pet: bool = None,
        guest: bool = None,

        skip: int = 0):
    availableRooms = getAvailableRooms(date_in, date_out, price_from, price_to, bedrooms, beds, bathrooms,
                                       breakfast, desk, baby_chair, crib, tv, shampoo, corridor, disabled,
                                       smoke, pet, guest, skip)
    return availableRooms


def dbConnectCheck(count_connect, ip):
    print(count_connect)
    count_connect += 1
    if count_connect == 8:
        raise Exception('Unable to connect to Database')

    db_user = os.environ['DATABASE_USER']
    db_pass = os.environ['DATABASE_PASS']
    db_host = f"172.18.0.{ip}"
    db_port = os.environ['DATABASE_PORT']
    db_name = os.environ['DATABASE_NAME']

    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(f"try to connect: {db_url}")

    try:
        create_engine(db_url).connect().close()
        os.environ['DATABASE_HOST'] = db_host
    except Exception as error:
        print('Caught this error: ' + repr(error))
        dbConnectCheck(count_connect, ip + 1)


if __name__ == "__main__":
    dbConnectCheck(0, 1)

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="localhost", port=8000)
