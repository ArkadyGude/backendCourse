from fastapi import Query, APIRouter

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    hotel_id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Навзвание отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotels_


@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1, "title": hotel_data.title, "name": hotel_data.name}
    )
    return {"status": "OK"}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    # Поиск отеля по ID
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
)
def partial_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
