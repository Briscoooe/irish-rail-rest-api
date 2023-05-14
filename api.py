import datetime

from apiflask import APIFlask, Schema
from marshmallow.fields import List, Integer, String, DateTime, Enum
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

app = APIFlask(__name__, title="Irish Rail REST API (Unofficial)", version="1.0.0", docs_ui='redoc')

class StationTypeIn(Schema):
    station_type = String(required=False, default=StationType.A, validate=[OneOf(StationType.list())], metadata={'description': 'A for All, M for Mainline, S for suburban and D for DART', 'default': 'A'})

@app.get("/stations")
@app.input(
    schema=StationTypeIn,
    location="query",
)
@app.output(Station(many=True))
@app.doc(operation_id="get_stations", description="Returns a list of stations.")
def get_stations(query):
    if not query:
        query = {"station_type": StationType.A}
    return irish_rail_service.get_stations(station_type=query["station_type"])



@app.get("/stations/filter")
@app.input(
    schema={
        "text": String(required=True),
    },
    location="query",
)
@app.output(StationFilterResult(many=True))
@app.doc(operation_id="filter_stations", description="Returns a list of stations that match the given text.")
def filter_stations(query):
    return irish_rail_service.filter_stations(text=query["text"])

@app.get("/stations/<station_code>/")
@app.input(
    schema={
        "num_mins": Integer(
            required=False, default=90, validate=[Range(min=5, max=90)], metadata={'default': 90}
        ),
    },
    location="query",
)
@app.output(StationInformation(many=True))
@app.doc(operation_id="get_station_information", description="Returns all trains due to serve the named station in the next `num_mins` minutes.")
def get_station_information(station_code, query):
    if not query:
        query = {"num_mins": 90}
    return irish_rail_service.get_station_information(station_code=station_code, num_mins=query)


@app.get("/trains")
@app.input(
    schema=StationTypeIn,
    location="query",
)
@app.output(Train(many=True))
@app.doc(operation_id="get_trains", description="Returns a list of of 'running trains' i.e. trains that are between origin and destination or are due to start within 10 minutes of the query time")
def get_trains(query):
    if not query:
        query = {"station_type": StationType.A}
    return irish_rail_service.get_trains(station_type=query["station_type"])


@app.get("/trains/<train_code>/movements")
@app.input(
    schema={
        "date": DateTime(required=False),
    },
    location="query",
)
@app.output(TrainMovement(many=True))
@app.doc(operation_id="get_train_movements")
@app.doc(
    summary="Get train movements",
    description="Returns all stop information for the given train.",
)
def get_train_movements(train_code: str, query):
    if not query:
        query = {"date": datetime.date.today()}
    return irish_rail_service.get_train_movements(train_code=train_code, date=query["date"])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
