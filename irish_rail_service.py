from datetime import datetime
from typing import Dict, List

import requests
from defusedxml import ElementTree
from defusedxml.ElementTree import fromstring
from requests import Response

from enums import StationType

API_BASE_URL = "http://api.irishrail.ie/realtime/realtime.asmx"
XML_TAG_PREFIX = "{http://api.irishrail.ie/realtime/}"


def get_iterable_dom_tree(url: str) -> ElementTree:
    response: Response = requests.get(url)
    xml_string = response.text
    return fromstring(xml_string)


def get_stations(station_type: StationType) -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getAllStationsXML_WithStationType?StationType={str(station_type.value)}"
    dom_tree = get_iterable_dom_tree(url)
    stations = []
    for station_el in dom_tree:

        description = ""
        alias = ""
        latitute = ""
        longitude = ""
        code = ""
        id = ""

        for child in station_el:
            if child.tag == f"{XML_TAG_PREFIX}StationDesc":
                description = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StationAlias":
                alias = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StationLatitude":
                latitute = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StationLongitude":
                longitude = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StationCode":
                code = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StationId":
                id = child.text

        station = {
            "description": description,
            "alias": alias,
            "latitude": latitute,
            "longitude": longitude,
            "code": code,
            "id": id,
        }
        stations.append(station)
    return stations


def get_station_information(station_code: str, num_mins: int) -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getStationDataByCodeXML_WithNumMins?StationCode={station_code}&NumMins={num_mins}"
    dom_tree = get_iterable_dom_tree(url)
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
            if child.tag == f"{XML_TAG_PREFIX}Traincode":
                train_code = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Stationfullname":
                station_full_name = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Stationcode":
                station_code = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Querytime":
                query_time = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Traindate":
                train_date = datetime.strptime(child.text, "%d %b %Y")
            elif child.tag == f"{XML_TAG_PREFIX}Origin":
                origin = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Destination":
                destination = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Origintime":
                origin_time = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Destinationtime":
                destination_time = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Status":
                status = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Lastlocation":
                last_location = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Duein":
                due_in = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Late":
                late = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Exparrival":
                exp_arrival = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Expdepart":
                exp_depart = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Scharrival":
                sch_arrival = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Schdepart":
                sch_depart = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Direction":
                direction = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Traintype":
                train_type = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Locationtype":
                location_type = child.text

        station = {
            "train_code": train_code,
            "station_full_name": station_full_name,
            "station_code": station_code,
            "query_time": query_time,
            "train_date": train_date,
            "origin": origin,
            "destination": destination,
            "origin_time": origin_time,
            "destination_time": destination_time,
            "status": status,
            "last_location": last_location,
            "due_in": due_in,
            "late": late,
            "exp_arrival": exp_arrival,
            "exp_depart": exp_depart,
            "sch_arrival": sch_arrival,
            "sch_depart": sch_depart,
            "direction": direction,
            "train_type": train_type,
            "location_type": location_type,
        }
        station_data.append(station)
    return station_data


def filter_stations(text: str) -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getStationsFilterXML?StationText={text}"
    dom_tree = get_iterable_dom_tree(url)
    stations = []

    for station_el in dom_tree:
        description = ""
        description_sp = ""
        code = ""

        for child in station_el:
            if child.tag == f"{XML_TAG_PREFIX}StationDesc":
                description = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StationDesc_sp":
                description_sp = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StationCode":
                code = child.text

        station = {
            "description": description,
            "description_sp": description_sp,
            "code": code,
        }
        stations.append(station)
    return stations


def get_trains(station_type: StationType) -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getCurrentTrainsXML_WithTrainType?TrainType={str(station_type.value)}"
    dom_tree = get_iterable_dom_tree(url)
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
            if child.tag == f"{XML_TAG_PREFIX}TrainStatus":
                status = child.text
            elif child.tag == f"{XML_TAG_PREFIX}TrainLatitude":
                latitude = child.text
            elif child.tag == f"{XML_TAG_PREFIX}TrainLongitude":
                longitude = child.text
            elif child.tag == f"{XML_TAG_PREFIX}TrainCode":
                code = child.text
            elif child.tag == f"{XML_TAG_PREFIX}TrainDate":
                date = child.text
            elif child.tag == f"{XML_TAG_PREFIX}PublicMessage":
                public_message = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Direction":
                direction = child.text

        train = {
            "status": status,
            "latitude": latitude,
            "longitude": longitude,
            "code": code,
            "date": date,
            "public_message": public_message,
            "direction": direction,
        }
        trains.append(train)
    return trains


def get_train_movements(train_code: str, date: datetime) -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getTrainMovementsXML?TrainId={train_code}&TrainDate={date.strftime('%d %m %Y')}"
    dom_tree = get_iterable_dom_tree(url)
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
            if child.tag == f"{XML_TAG_PREFIX}TrainCode":
                code = child.text
            elif child.tag == f"{XML_TAG_PREFIX}TrainDate":
                date = child.text
            elif child.tag == f"{XML_TAG_PREFIX}LocationCode":
                location_code = child.text
            elif child.tag == f"{XML_TAG_PREFIX}LocationFullName":
                location_full_name = child.text
            elif child.tag == f"{XML_TAG_PREFIX}LocationOrder":
                location_order = child.text
            elif child.tag == f"{XML_TAG_PREFIX}LocationType":
                location_type = child.text
            elif child.tag == f"{XML_TAG_PREFIX}TrainOrigin":
                train_origin = child.text
            elif child.tag == f"{XML_TAG_PREFIX}TrainDestination":
                train_destination = child.text
            elif child.tag == f"{XML_TAG_PREFIX}ScheduledArrival":
                scheduled_arrival = child.text
            elif child.tag == f"{XML_TAG_PREFIX}ScheduledDeparture":
                scheduled_departure = child.text
            elif child.tag == f"{XML_TAG_PREFIX}ExpectedArrival":
                expected_arrival = child.text
            elif child.tag == f"{XML_TAG_PREFIX}ExpectedDeparture":
                expected_departure = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Arrival":
                arrival = child.text
            elif child.tag == f"{XML_TAG_PREFIX}Departure":
                departure = child.text
            elif child.tag == f"{XML_TAG_PREFIX}AutoArrival":
                auto_arrival = child.text
            elif child.tag == f"{XML_TAG_PREFIX}AutoDepart":
                auto_depart = child.text
            elif child.tag == f"{XML_TAG_PREFIX}StopType":
                stop_type = child.text

        movement = {
            "code": code,
            "date": date,
            "location_code": location_code,
            "location_full_name": location_full_name,
            "location_order": location_order,
            "location_type": location_type,
            "train_origin": train_origin,
            "train_destination": train_destination,
            "scheduled_arrival": scheduled_arrival,
            "scheduled_departure": scheduled_departure,
            "expected_arrival": expected_arrival,
            "expected_departure": expected_departure,
            "arrival": arrival,
            "departure": departure,
            "auto_arrival": auto_arrival,
            "auto_depart": auto_depart,
            "stop_type": stop_type,
        }
        movements.append(movement)
    return movements
