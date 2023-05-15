from apiflask import Schema
from apiflask.fields import Integer, String, Time
from marshmallow.fields import Boolean, Date, Float
from marshmallow.validate import OneOf

from enums import StopType, TrainStatus, LocationType, StationType


class Station(Schema):
    name = String()
    alias = String()
    latitude = Float()
    longitude = Float()
    code = String()
    id = String()


class StationTimetableItem(Schema):
    train_code = String(
        metadata={
            "description": "Irish Rail's unique code for an individual train service on a date"
        }
    )
    station_full_name = String(
        metadata={
            "description": "Long version of Station Name (identical in every record)"
        }
    )
    id = String(metadata={"description": "4 to 5 letter station abbreviation"})
    query_time = Time(
        metadata={"description": "Time the query was made. Format `HH:MM:SS`"}
    )
    train_date = Date(
        metadata={
            "description": "The date the service started its journey (some trains run over midnight).\nDate in `YYYY-MM-DD` format",
        },
    )
    origin = String()
    destination = String()
    origin_time = Time(
        metadata={
            "description": "The time the train left (or will leave) its origin. Format `HH:MM`"
        }
    )
    destination_time = Time(
        metadata={
            "description": "The scheduled time at its destination. Format `HH:MM`"
        }
    )
    status = String(metadata={"description": "Latest information on this service"})
    last_location = String(metadata={"description": "(Arrived|Departed $station_name)"})
    due_in = Integer(
        metadata={"description": "Num of minutes till the train will arrive here"}
    )
    late = Integer(metadata={"description": "Num of minutes the train is late"})
    exp_arrival = String(
        metadata={
            "description": "The trains expected arrival time at the query station updated as the train progresses (note will show 00:00 for trains starting from query station. Format `HH:MM`"
        }
    )
    exp_depart = String(
        metadata={
            "description": "The trains expected departure time at the query station updated as the train progresses (note will show 00:00 for trains terminating at query station). Format `HH:MM`"
        }
    )
    sch_arrival = String(
        metadata={
            "description": "The trains scheduled arrival time at the query station (note will show 00:00 for trains starting from query station). Format `HH:MM`"
        }
    )
    sch_depart = String(
        metadata={
            "description": "The trains scheduled departure time at the query station (note will show 00:00 for trains terminating at query station). Format `HH:MM`"
        }
    )
    direction = String(
        metadata={"description": "Northbound, Southbound or To Destination"}
    )
    train_type = String(
        metadata={"description": "DART, Commuter, Intercity, Enterprise or None"}
    )
    location_type = String(
        metadata={"description": "O for Origin, D for Destination or S for Stop"},
        validate=[OneOf(LocationType.list())],
    )


class Train(Schema):
    status = String(
        validate=[OneOf(TrainStatus.list())],
        metadata={"description": "N for not yet running or R for running"},
    )
    latitude = Float()
    longitude = Float()
    code = String(
        metadata={
            "description": "Irish Rail's unique code for an individual train service on a date"
        }
    )
    date = Date()
    public_message = String(
        metadata={"description": "The latest information on the train uses"}
    )
    direction = String(
        metadata={
            "description": "Either Northbound or Southbound for trains between Dundalk and Rosslare and between Sligo and Dublin.  for all other trains the direction is to the destination eg. To Limerick"
        }
    )


class TrainMovement(Schema):
    code = String()
    date = Date(metadata={"description": "Date in `YYYY-MM-DD` format"})
    location_code = String()
    location_full_name = String()
    location_order = Integer()
    train_origin = String()
    train_destination = String()
    scheduled_arrival = Time(metadata={"description": "Format `HH:MM:SS`"})
    scheduled_departure = Time(metadata={"description": "Format `HH:MM:SS`"})
    expected_arrival = Time(metadata={"description": "Format `HH:MM:SS`"})
    expected_departure = Time(metadata={"description": "Format `HH:MM:SS`"})
    arrival = String(metadata={"description": "Actual arrival time. Format `HH:MM:SS`"})
    departure = String(metadata={"description": "Actual departure time. Format `HH:MM:SS`"})
    auto_arrival = Boolean(
        metadata={"description": "Was information automatically generated"}
    )
    auto_depart = Boolean()
    stop_type = String(
        metadata={"description": "C for Current, N for Next"},
        default=StopType.C,
        validate=[OneOf(StopType.list())],
    )


class StationSearchResult(Schema):
    name = String()
    code = String()


class StationTypeIn(Schema):
    type = String(
        required=False,
        validate=[OneOf(StationType.list())],
    )
