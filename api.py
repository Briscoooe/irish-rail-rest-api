from apiflask import APIFlask, Schema
from apiflask.fields import Integer, String
from marshmallow.fields import Date, Enum

import irish_rail_service
from enums import StationType, TrainStatus
from schemas import (Station, StationFilterResult, StationInformation, Train,
                     TrainMovement)

app = APIFlask(__name__)


@app.get("/stations")
@app.input(
    {
        "type": Enum(required=False, enum=StationType, default=StationType.A),
    },
    location="query",
)
@app.output(Station(many=True))
def get_stations(query):
    if not query:
        query = {"type": StationType.A}
    return irish_rail_service.get_stations(query["type"])


@app.get("/stations/<station_code>/")
@app.input(
    {
        "num_mins": Integer(required=False, default=90),
    },
    location="query",
)
@app.output(StationInformation(many=True))
def get_station_information(station_code, query):
    if not query:
        query = {"num_mins": 90}
    return irish_rail_service.get_station_information(station_code, query)


@app.get("/stations/filter")
@app.input(
    {
        "text": String(required=True),
    },
    location="query",
)
@app.output(StationFilterResult(many=True))
def filter_stations(query):
    return irish_rail_service.filter_stations(query["text"])


@app.get("/trains")
@app.input(
    {
        "type": Enum(required=False, enum=StationType, default=StationType.A),
    },
    location="query",
)
@app.output(Train(many=True))
def get_trains(query):
    if not query:
        query = {"type": StationType.A}
    return irish_rail_service.get_trains(query["type"])


@app.get("/trains/<train_code>/movements")
@app.input(
    {
        "date": Date(required=True),
    },
    location="query",
)
@app.output(TrainMovement(many=True))
def get_train_movements(train_code, query):
    return irish_rail_service.get_train_movements(train_code, query["date"])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
