from fastapi import FastAPI, Query, Body
import uvicorn

from fastapi.openapi.docs import get_swagger_ui_html


app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/hotels")
def get_hotels(
    hotel_id: int | None = Query(default=None, description="ID"),
    title: str | None = Query(default=None, description="Навзвание отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True), name: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title, "name": name})
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int, title: str = Body(embed=True), name: str = Body(embed=True)
):
    global hotels
    # Поиск отеля по ID
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            # Обновление отеля
            if title is not None:
                hotels[i]["title"] = title
            if name is not None:
                hotels[i]["name"] = name
            return {"status": "OK", "updated_hotel": hotels[i]}

    # Если отель не найден
    return {"status": "ERROR", "message": "Hotel not found"}


@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    title: str | None = Body(default=None, embed=True),
    name: str | None = Body(default=None, embed=True),
):
    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            if title is not None:
                hotels[i]["title"] = title
            if name is not None:
                hotels[i]["name"] = name
            return {"status": "OK", "updated_hotel": hotels[i]}
    return {"status": "ERROR", "message": "Hotel not found"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
