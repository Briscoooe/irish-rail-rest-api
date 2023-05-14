from apiflask import Schema
from apiflask.fields import Integer, String
from marshmallow.fields import Boolean, Date, Float


class Station(Schema):
    description = String()
    alias = String()
    latitude = Float()
    longitude = Float()
    code = String()
    id = String()


class StationInformation(Schema):
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
    station_code = String(
        metadata={"description": "4 to 5 letter station abbreviation"}
    )
    query_time = String(metadata={"description": "Time the query was made"})
    train_date = Date(
        metadata={
            "description": "The date the service started its journey ( some trains run over midnight)"
        }
    )
    origin = String()
    destination = String()
    origin_time = String(
        metadata={"description": "The time the train left (or will leave) its origin"}
    )
    destination_time = String(
        metadata={"description": "The scheduled time at its destination"}
    )
    status = String(metadata={"description": "Latest information on this service"})
    last_location = String(metadata={"description": "(Arrived|Departed $station_name)"})
    due_in = Integer(
        metadata={"description": "Num of minutes till the train will arrive here"}
    )
    late = Integer(metadata={"description": "Num of minutes the train is late"})
    exp_arrival = String(
        metadata={
            "description": "The trains expected arrival time at the query station updated as the train progresses ( note will show 00:00 for trains starting from query station"
        }
    )
    exp_depart = String(
        metadata={
            "description": "The trains expected departure time at the query station updated as the train progresses ( note will show 00:00 for trains terminating at query station)"
        }
    )
    sch_arrival = String(
        metadata={
            "description": "The trains scheduled arrival time at the query station ( note will show 00:00 for trains starting from query station)"
        }
    )
    sch_depart = String(
        metadata={
            "description": "The trains scheduled departure time at the query station ( note will show 00:00 for trains terminating at query station)"
        }
    )
    direction = String(
        metadata={"description": "Northbound, Southbound or To Destination"}
    )
    train_type = String(
        metadata={"description": "DART, Commuter, Intercity, Enterprise or None"}
    )
    location_type = String(
        metadata={"description": "O for Origin, D for Destination or S for Stop"}
    )


class Train(Schema):
    status = String(metadata={"description": "N for not yet running or R for running"})
    latitude = Float()
    longitude = Float()
    code = String(
        metadata={
            "description": "Irish Rail's unique code for an individual train service on a date"
        }
    )
    date = String()
    public_message = String(
        metadata={
            "description": "Public Message is the latest information on the train uses"
        }
    )
    direction = String(
        metadata={
            "description": "Direction is either Northbound or Southbound for trains between Dundalk and Rosslare and between Sligo and Dublin.  for all other trains the direction is to the destination eg. To Limerick"
        }
    )


class TrainMovement(Schema):
    code = String()
    date = String()
    location_code = String()
    location_full_name = String()
    location_order = Integer()
    location_type = String()
    train_origin = String()
    train_destination = String()
    scheduled_arrival = String()
    scheduled_departure = String()
    expected_arrival = String()
    expected_departure = String()
    arrival = String(metadata={"description": "Actual arrival time"})
    departure = String(metadata={"description": "Actual departure time"})
    auto_arrival = Boolean(
        metadata={"description": "Was information automatically generated"}
    )
    auto_depart = Boolean()
    stop_type = String(metadata={"description": "C= Current N = Next"})


class StationFilterResult(Schema):
    description = String()
    description_sp = String()
    code = String()
