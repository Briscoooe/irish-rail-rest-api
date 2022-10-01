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
    # https: // apiflask.com / openapi /
    #     name = String(metadata={'description': 'The name of the pet.'})
    train_code = String()
    station_full_name = String()
    station_code = String()
    query_time = String()
    train_date = Date()
    origin = String()
    destination = String()
    origin_time = String()
    destination_time = String()
    status = String()
    last_location = String()
    due_in = Integer()
    late = Integer()
    exp_arrival = String()
    exp_depart = String()
    sch_arrival = String()
    sch_depart = String()
    direction = String()
    train_type = String()
    location_type = String()


class Train(Schema):
    status = String()
    latitude = Float()
    longitude = Float()
    code = String()
    date = String()
    public_message = String()
    direction = String()


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
    arrival = String()
    departure = String()
    auto_arrival = Boolean()
    auto_depart = Boolean()
    stop_type = String()


class StationFilterResult(Schema):
    description = String()
    description_sp = String()
    code = String()
