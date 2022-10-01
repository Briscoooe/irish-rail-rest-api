from datetime import datetime
from enum import Enum as NativeEnum

import requests
from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from defusedxml.ElementTree import fromstring
from marshmallow.fields import Float, Enum as MarshmallowEnum, Date, Boolean
from requests import Response

API_BASE_URL = 'http://api.irishrail.ie/realtime/realtime.asmx'
XML_TAG_PREFIX = '{http://api.irishrail.ie/realtime/}'

app = APIFlask(__name__)

pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'}
]


class Station(Schema):
    description = String()
    alias = String()
    latitude = Float()
    longitude = Float()
    code = String()
    id = String()

class StationInformation(Schema):
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

class StationType(NativeEnum):
    A = 'A'
    S = 'S'
    D = 'D'
    M = 'M'

class LocationTypeEnum(NativeEnum):
    O = 'O'
    T = 'T'
    S = 'S'
    D = 'D'

class StopTypeEnum(NativeEnum):
    C = 'C'
    N = 'N'

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


class StationQuery(Schema):
    type = MarshmallowEnum(required=False, enum=StationType, default=StationType.A)


@app.get('/stations')
@app.input(StationQuery, location='query')  # query string
@app.output(Station(many=True))
def get_stations(query):
    if not query:
        query = {
            'type': StationType.A
        }
    stations_url = (
        f"{API_BASE_URL}/getAllStationsXML_WithStationType?StationType={str(query['type'].value)}"
    )
    response: Response = requests.get(stations_url)
    xml_string = response.text
    dom_tree = fromstring(xml_string)
    stations = []
    for station_el in dom_tree:

        description =""
        alias = ""
        latitute = ""
        longitude =""
        code = ""
        id = ""

        for child in station_el:
            if child.tag == f'{XML_TAG_PREFIX}StationDesc':
                description = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StationAlias':
                alias = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StationLatitude':
                latitute = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StationLongitude':
                longitude = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StationCode':
                code = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StationId':
                id = child.text

        station = {
            'description': description,
            'alias': alias,
            'latitude': latitute,
            'longitude': longitude,
            'code': code,
            'id': id,
        }
        stations.append(station)
    return stations

class StationDetailQuery(Schema):
    num_mins = Integer(required=False, default=90)

@app.get('/stations/<station_code>/')
@app.input(StationDetailQuery, location='query')
@app.output(StationInformation(many=True))
def get_station_information(station_code, query):
    if not query:
        query = {
            'num_mins': 90
        }
    url = f"{API_BASE_URL}/getStationDataByCodeXML_WithNumMins?StationCode={station_code}&NumMins={query['num_mins']}"
    response: Response = requests.get(url)
    xml_string = response.text
    dom_tree = fromstring(xml_string)
    station_data = []
    for station_el in dom_tree:
        train_code = ""
        station_full_name = ""
        station_code = ""
        query_time = ""
        train_date = ""
        origin = ""
        destination = ""
        origin_time = ""
        destination_time = ""
        status = ""
        last_location = ""
        due_in = ""
        late = ""
        exp_arrival = ""
        exp_depart = ""
        sch_arrival = ""
        sch_depart = ""
        direction = ""
        train_type = ""
        location_type = ""

        for child in station_el:
            if child.tag == f'{XML_TAG_PREFIX}Traincode':
                train_code = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Stationfullname':
                station_full_name = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Stationcode':
                station_code = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Querytime':
                query_time = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Traindate':
                train_date = datetime.strptime(child.text, '%d %b %Y')
            elif child.tag == f'{XML_TAG_PREFIX}Origin':
                origin = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Destination':
                destination = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Origintime':
                origin_time = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Destinationtime':
                destination_time = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Status':
                status = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Lastlocation':
                last_location = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Duein':
                due_in = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Late':
                late = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Exparrival':
                exp_arrival = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Expdepart':
                exp_depart = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Scharrival':
                sch_arrival = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Schdepart':
                sch_depart = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Direction':
                direction = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Traintype':
                train_type = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Locationtype':
                location_type = child.text

        station = {

            'train_code': train_code,
            'station_full_name': station_full_name,
            'station_code': station_code,
            'query_time': query_time,
            'train_date': train_date,
            'origin': origin,
            'destination': destination,
            'origin_time': origin_time,
            'destination_time': destination_time,
            'status': status,
            'last_location': last_location,
            'due_in': due_in,
            'late': late,
            'exp_arrival': exp_arrival,
            'exp_depart': exp_depart,
            'sch_arrival': sch_arrival,
            'sch_depart': sch_depart,
            'direction': direction,
            'train_type': train_type,
            'location_type': location_type,
        }
        station_data.append(station)
    return station_data


class StationFilterQuery(Schema):
    text = String(required=True)

class StationFilterResult(Schema):
    description = String()
    description_sp = String()
    code = String()

@app.get('/stations/filter')
@app.input(StationFilterQuery, location='query')  # query string
@app.output(StationFilterResult(many=True))
def filter_stations(query):
    url = f"{API_BASE_URL}/getStationsFilterXML?StationText={query['text']}"
    response: Response = requests.get(url)
    xml_string = response.text
    dom_tree = fromstring(xml_string)
    stations = []

    for station_el in dom_tree:
        description =""
        description_sp = ""
        code = ""

        for child in station_el:
            if child.tag == f'{XML_TAG_PREFIX}StationDesc':
                description = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StationDesc_sp':
                description_sp = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StationCode':
                code = child.text

        station = {
            'description': description,
            'description_sp': description_sp,
            'code': code,
        }
        stations.append(station)
    print(stations)
    return stations




class TrainStatus(NativeEnum):
    N = 'N'
    R = 'R'

class TrainQuery(Schema):
    status = MarshmallowEnum(required=False, enum=TrainStatus)
    type = MarshmallowEnum(required=False, enum=StationType, default=StationType.A)

@app.get('/trains')
@app.input(TrainQuery, location='query')
@app.output(Train(many=True))
def get_trains(query):
    if not query:
        query = {
            'status': TrainStatus.N,
            'type': StationType.A
        }
    trains_url = f"{API_BASE_URL}/getCurrentTrainsXML_WithTrainType?TrainType={str(query['type'].value)}"

    print(trains_url)
    response: Response = requests.get(trains_url)
    xml_string = response.text
    dom_tree = fromstring(xml_string)
    trains = []
    for train_el in dom_tree:
        status = ""
        latitude = ""
        longitude = ""
        code = ""
        date = ""
        public_message = ""
        direction = ""

        for child in train_el:
            if child.tag == f'{XML_TAG_PREFIX}TrainStatus':
                status = child.text
            elif child.tag == f'{XML_TAG_PREFIX}TrainLatitude':
                latitude = child.text
            elif child.tag == f'{XML_TAG_PREFIX}TrainLongitude':
                longitude = child.text
            elif child.tag == f'{XML_TAG_PREFIX}TrainCode':
                code = child.text
            elif child.tag == f'{XML_TAG_PREFIX}TrainDate':
                date = child.text
            elif child.tag == f'{XML_TAG_PREFIX}PublicMessage':
                public_message = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Direction':
                direction = child.text

        train = {
            'status': status,
            'latitude': latitude,
            'longitude': longitude,
            'code': code,
            'date': date,
            'public_message': public_message,
            'direction': direction,
        }
        trains.append(train)
    return trains

class TrainMovementQuery(Schema):
    date = Date(required=True)

@app.get('/trains/<train_code>/movements')
@app.input(TrainMovementQuery, location='query')
@app.output(TrainMovement(many=True))
def get_train_movements(train_code, query):
    movements_url = f"{API_BASE_URL}/getTrainMovementsXML?TrainId={train_code}&TrainDate={query['date'].strftime('%d %m %Y')}"
    print(movements_url)
    print(movements_url)
    response: Response = requests.get(movements_url)
    xml_string = response.text
    dom_tree = fromstring(xml_string)
    movements = []
    for movement_el in dom_tree:
        code = ""
        date = ""
        location_code = ""
        location_full_name = ""
        location_order = ""
        location_type = ""
        train_origin = ""
        train_destination = ""
        scheduled_arrival = ""
        scheduled_departure = ""
        expected_arrival = ""
        expected_departure = ""
        arrival = ""
        departure = ""
        auto_arrival = ""
        auto_depart = ""
        stop_type = ""

        for child in movement_el:
            if child.tag == f'{XML_TAG_PREFIX}TrainCode':
                code = child.text
            elif child.tag == f'{XML_TAG_PREFIX}TrainDate':
                date = child.text
            elif child.tag == f'{XML_TAG_PREFIX}LocationCode':
                location_code = child.text
            elif child.tag == f'{XML_TAG_PREFIX}LocationFullName':
                location_full_name = child.text
            elif child.tag == f'{XML_TAG_PREFIX}LocationOrder':
                location_order = child.text
            elif child.tag == f'{XML_TAG_PREFIX}LocationType':
                location_type = child.text
            elif child.tag == f'{XML_TAG_PREFIX}TrainOrigin':
                train_origin = child.text
            elif child.tag == f'{XML_TAG_PREFIX}TrainDestination':
                train_destination = child.text
            elif child.tag == f'{XML_TAG_PREFIX}ScheduledArrival':
                scheduled_arrival = child.text
            elif child.tag == f'{XML_TAG_PREFIX}ScheduledDeparture':
                scheduled_departure = child.text
            elif child.tag == f'{XML_TAG_PREFIX}ExpectedArrival':
                expected_arrival = child.text
            elif child.tag == f'{XML_TAG_PREFIX}ExpectedDeparture':
                expected_departure = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Arrival':
                arrival = child.text
            elif child.tag == f'{XML_TAG_PREFIX}Departure':
                departure = child.text
            elif child.tag == f'{XML_TAG_PREFIX}AutoArrival':
                auto_arrival = child.text
            elif child.tag == f'{XML_TAG_PREFIX}AutoDepart':
                auto_depart = child.text
            elif child.tag == f'{XML_TAG_PREFIX}StopType':
                stop_type = child.text

        movement = {
            'code': code,
            'date': date,
            'location_code': location_code,
            'location_full_name': location_full_name,
            'location_order': location_order,
            'location_type': location_type,
            'train_origin': train_origin,
            'train_destination': train_destination,
            'scheduled_arrival': scheduled_arrival,
            'scheduled_departure': scheduled_departure,
            'expected_arrival': expected_arrival,
            'expected_departure': expected_departure,
            'arrival': arrival,
            'departure': departure,
            'auto_arrival': auto_arrival,
            'auto_depart': auto_depart,
            'stop_type': stop_type,
        }
        movements.append(movement)
    return movements


if __name__ == '__main__':
    app.run(debug=True, port=5001)
