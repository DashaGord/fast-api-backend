import os
from os import linesep

from fastapi.encoders import jsonable_encoder
from schemas import AvailableRoomsResponse, AvailableRoom
from sqlalchemy import create_engine


def generateFilterStr(**kwargs):
    str = ""
    first = True
    for k, v in kwargs.items():
        if v is not None:
            if first:
                str += f"{linesep}WHERE h.{k} = {v}"
                first = False
            else:
                str += f"{linesep}AND h.{k} = {v}"
    return str


def getDateDiff(date1, date2):
    delta = date2 - date1
    return delta.days + 1


def getAvailableRooms(date_in, date_out, price_from, price_to, bedrooms, beds, bathrooms, breakfast, desk,
                      baby_chair, crib, tv, shampoo, corridor, disabled, smoke, pet, guest, offset):
    filter_str = generateFilterStr(bedrooms=bedrooms, beds=beds, bathrooms=bathrooms, breakfast=breakfast, desk=desk,
                                   baby_chair=baby_chair, crib=crib, tv=tv, shampoo=shampoo, corridor=corridor,
                                   disabled=disabled, smoke=smoke, pet=pet, guest=guest)

    query = f""" 
    SELECT h.id, h.luxury, h.images, h.stars, round(avg(price))::INTEGER AS avg_price, COUNT(*) OVER()
    FROM (
        SELECT hotel_room_id, price
        FROM "availability"
        WHERE date BETWEEN '{date_in}' AND '{date_out}'
    ) AS foo
    INNER JOIN "hotel-room" AS h
    ON h.id = foo.hotel_room_id {filter_str}
    GROUP BY h.id
    HAVING COUNT(h.id) = {getDateDiff(date_in, date_out)} AND round(avg(price)) BETWEEN {price_from} AND {price_to}
    ORDER BY h.id
    OFFSET {offset} ROWS FETCH NEXT 20 ROWS ONLY
    """

    count = 0
    rooms = list()

    try:
        db_user = os.environ['DATABASE_USER']
        db_pass = os.environ['DATABASE_PASS']
        db_host = os.environ['DATABASE_HOST']
        db_port = os.environ['DATABASE_PORT']
        db_name = os.environ['DATABASE_NAME']

        db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        # db_url = os.environ['DATABASE_URL']

        engine = create_engine(db_url)
        with engine.connect() as con:
            rs = con.execute(query)

            if rs.rowcount:
                for row in rs:
                    print(rs.cursor)

                    availableRoom = AvailableRoom(
                        id=row[0],
                        luxury=bool(row[1]),
                        images=str(row[2]).split("|"),
                        stars=row[3],
                        avg_price=row[4],
                    )
                    rooms.append(availableRoom)

                if count == 0:
                    count = row[5]

        con.close()

        response = AvailableRoomsResponse(
            count=count,
            available_rooms=rooms
        )

        return jsonable_encoder(response)
    except Exception as error:
        print('Caught this error: ' + repr(error))
        raise Exception('Unable to execute SQL query')
