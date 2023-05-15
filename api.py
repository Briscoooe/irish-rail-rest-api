import datetime

from apiflask import APIFlask
from marshmallow.fields import Integer, String, DateTime, Date
from marshmallow.validate import Range, Length
from werkzeug.utils import redirect

import irish_rail_service
from enums import StationType, station_type_map
from schemas import (
    Station,
    StationSearchResult,
    StationTimetableItem,
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


@app.get("/")
@app.doc(
    hide=True,
)
def index():
    return redirect("/docs")


@app.get("/stations")
@app.input(
    schema=StationTypeIn,
    location="query",
)
@app.output(
    schema=Station(many=True),
    links={
        "get_station_timetable": {
            "operationId": "get_station_timetable",
            "parameters": {"code": "$response.body#/code"},
        },
    },
)
@app.doc(
    operation_id="list_stations",
    description="Returns a list of stations.",
    tags=["stations"],
    summary="List stations",
)
def list_stations(query):
    station_type = query.get("type", None)
    if station_type:
        station_type = station_type_map[station_type]
    return irish_rail_service.list_stations(station_type=station_type)


@app.get("/stations/search")
@app.input(
    schema={
        "text": String(required=True),
    },
    location="query",
)
@app.output(schema=StationSearchResult(many=True))
@app.doc(
    summary="Search stations",
    operation_id="search_stations",
    description="Returns a list of stations that match the given text.",
    tags=["stations"],
)
def search_stations(query):
    return irish_rail_service.search_stations(text=query["text"])


@app.get("/stations/<code>/timetable")
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
# @app.input(
#     schema={
#         "code": String(
#             required=True,
#             validate=[Length(min=4, max=5)],
#             metadata={"description": "Station `code`"},
#         ),
#     },
#     location="query",
# )
@app.output(schema=StationTimetableItem(many=True))
@app.doc(
    summary="Get station timetable",
    operation_id="get_station_timetable",
    description="Returns all trains due to serve the named station in the next `num_mins` minutes.",
    tags=["stations"],
)
def get_station_timetable(code, query):
    if not query:
        query = {"num_mins": 90}
    return irish_rail_service.get_station_timetable(station_code=code, num_mins=query)


@app.get("/trains")
@app.input(
    schema=StationTypeIn,
    location="query",
)
@app.output(
    schema=Train(many=True),
    links={
        "get_train_movements": {
            "operationId": "get_train_movements",
            "parameters": {"code": "$response.body#/code"},
        },
    },
)
@app.doc(
    summary="List trains",
    operation_id="list_trains",
    description="Returns a list of of 'running trains' i.e. trains that are between origin and destination or are due to start within 10 minutes of the query time",
    tags=["trains"],
)
def list_trains(query):
    station_type = query.get("type", None)
    if station_type:
        station_type = station_type_map[station_type]
    return irish_rail_service.list_trains(station_type=station_type)


@app.get("/trains/<code>/movements")
@app.input(
    schema={
        "date": Date(
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
@app.output(schema=TrainMovement(many=True))
@app.doc(
    summary="Get train movements",
    operation_id="get_train_movements",
    description="Returns all stop information for the given train.",
    tags=["trains"],
)
def get_train_movements(code: str, query):
    if not query:
        query = {"date": datetime.date.today()}
    return irish_rail_service.get_train_movements(train_code=code, date=query["date"])
