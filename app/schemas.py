from pydantic import BaseModel


class AvailableRoom(BaseModel):
    id: int
    luxury: bool
    images: list[str]
    stars: int
    avg_price: int


class AvailableRoomsResponse(BaseModel):
    count: int
    available_rooms: list[AvailableRoom]
