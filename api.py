import datetime

from apiflask import APIFlask
from marshmallow.fields import Integer, String, DateTime
from marshmallow.validate import Range

import irish_rail_service
from enums import StationType
from schemas import (
    Station,
    StationFilterResult,
    StationInformation,
    Train,
    TrainMovement,
    StationTypeIn,
)

app = APIFlask(
    __name__,
    title="Irish Rail REST API (Unofficial)",
    version="1.0.0",
    docs_ui="redoc",
)
app.config[
    "DESCRIPTION"
] = """
A REST API wrapper around the SOAP API provided by Irish Rail. All documentation for the underlying SOAP API can be found [here](http://api.irishrail.ie/realtime/). Some property descriptions are missing as they are not provided by the orginal API. 

View on [GitHub](https://github.com/Briscoooe/irish-rail-rest-api)
"""

app.config["REDOC_CONFIG"] = {"expandResponses": "200"}


@app.get("/stations")
@app.input(
    schema=StationTypeIn,
    location="query",
)
@app.output(Station(many=True))
@app.doc(
    operation_id="get_stations",
    description="Returns a list of stations.",
    tags=["stations"],
    summary="Get stations",
)
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
@app.doc(
    summary="Filter stations",
    operation_id="filter_stations",
    description="Returns a list of stations that match the given text.",
    tags=["stations"],
)
def filter_stations(query):
    return irish_rail_service.filter_stations(text=query["text"])


@app.get("/stations/<station_code>/")
@app.input(
    schema={
        "num_mins": Integer(
            required=False,
            default=90,
            validate=[Range(min=5, max=90)],
            metadata={"default": 90},
        ),
    },
    location="query",
)
@app.output(StationInformation(many=True))
@app.doc(
    summary="Get station information",
    operation_id="get_station_information",
    description="Returns all trains due to serve the named station in the next `num_mins` minutes.",
    tags=["stations"],
)
def get_station_information(station_code, query):
    if not query:
        query = {"num_mins": 90}
    return irish_rail_service.get_station_information(
        station_code=station_code, num_mins=query
    )


@app.get("/trains")
@app.input(
    schema=StationTypeIn,
    location="query",
)
@app.output(Train(many=True))
@app.doc(
    summary="Get trains",
    operation_id="get_trains",
    description="Returns a list of of 'running trains' i.e. trains that are between origin and destination or are due to start within 10 minutes of the query time",
    tags=["trains"],
)
def get_trains(query):
    if not query:
        query = {"station_type": StationType.A}
    return irish_rail_service.get_trains(station_type=query["station_type"])


@app.get("/trains/<train_code>/movements")
@app.input(
    schema={
        "date": DateTime(
            required=False,
            default=datetime.datetime.now().strftime("%Y-%m-%d"),
            metadata={
                "default": datetime.datetime.now().strftime("%Y-%m-%d"),
                "description": "Date in `YYYY-MM-DD` format",
            },
        ),
    },
    location="query",
)
@app.output(TrainMovement(many=True))
@app.doc(
    summary="Get train movements",
    operation_id="get_train_movements",
    description="Returns all stop information for the given train.",
    tags=["trains"],
)
def get_train_movements(train_code: str, query):
    if not query:
        query = {"date": datetime.date.today()}
    return irish_rail_service.get_train_movements(
        train_code=train_code, date=query["date"]
    )
