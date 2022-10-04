import datetime

from apiflask import APIFlask
from marshmallow.fields import Date, Enum, Integer, String
from marshmallow.validate import Range, OneOf

import irish_rail_service
from enums import StationType
from schemas import (
    Station,
    StationFilterResult,
    StationInformation,
    Train,
    TrainMovement,
)

app = APIFlask(__name__, title="Irish Rail JSON API (Unofficial)", version="1.0.0")


@app.get("/stations")
@app.input(
    {
        "station_type": Enum(required=False, enum=StationType, default=StationType.A),
    },
    location="query",
)
@app.output(Station(many=True))
@app.doc(operation_id="get_stations")
def get_stations(query):
    if not query:
        query = {"station_type": StationType.A}
    return irish_rail_service.get_stations(query["station_type"])


@app.get("/stations/<station_code>/")
@app.input(
    {
        "num_mins": Integer(
            required=False, default=90, validate=[Range(min=5, max=90)]
        ),
    },
    location="query",
)
@app.output(StationInformation(many=True))
@app.doc(operation_id="get_station_information")
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
@app.doc(operation_id="filter_stations")
def filter_stations(query):
    return irish_rail_service.filter_stations(query["text"])


@app.get("/trains")
@app.input(
    {
        "station_type": Enum(
            required=False,
            enum=StationType,
            default=StationType.A,
        ),
    },
    location="query",
)
@app.output(Train(many=True))
@app.doc(operation_id="get_trains")
def get_trains(query):
    if not query:
        query = {"station_type": StationType.A}
    return irish_rail_service.get_trains(query["station_type"])


@app.get("/trains/<train_code>/movements")
@app.input(
    {
        "date": Date(required=False),
    },
    location="query",
)
@app.output(TrainMovement(many=True))
@app.doc(operation_id="get_train_movements")
@app.doc(
    summary="Get train movements",
    description="Returns all stop information for the given train as follows",
)
def get_train_movements(train_code, query):
    if not query:
        query = {"date": datetime.date.today()}
    return irish_rail_service.get_train_movements(train_code, query["date"])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
