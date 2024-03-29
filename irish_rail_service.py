from datetime import datetime, time
from typing import Dict, List, Union, Optional

import requests
from defusedxml import ElementTree
from defusedxml.ElementTree import fromstring
from requests import Response

API_BASE_URL = "http://api.irishrail.ie/realtime/realtime.asmx"
XML_TAG_PREFIX = "{http://api.irishrail.ie/realtime/}"


def get_iterable_dom_tree(url: str) -> ElementTree:
    response: Response = requests.get(url)
    xml_string = response.text
    return fromstring(xml_string)


def convert_date_format(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%d %b %Y")


def parse_time_hh_mm(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M").time()


def parse_time_hh_mm_ss(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M:%S").time()


def map_xml_to_dict(
    key_value_mappings: List[Dict[str, str]], dom_element: ElementTree
) -> Dict[str, str]:
    mapped_dict = {}
    for key_value_mapping in key_value_mappings:
        for child in dom_element:
            if child.tag == f"{XML_TAG_PREFIX}{key_value_mapping['xml_tag']}":
                mapped_dict[key_value_mapping["dict_key"]] = (
                    child.text.strip() if child.text else None
                )
    return mapped_dict


def list_stations(station_type: Optional[str] = "A") -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getAllStationsXML_WithStationType?StationType={station_type}"
    dom_tree = get_iterable_dom_tree(url)
    stations = []
    for station_el in dom_tree:
        station = map_xml_to_dict(
            [
                {"xml_tag": "StationDesc", "dict_key": "name"},
                {"xml_tag": "StationAlias", "dict_key": "alias"},
                {"xml_tag": "StationLatitude", "dict_key": "latitude"},
                {"xml_tag": "StationLongitude", "dict_key": "longitude"},
                {"xml_tag": "StationCode", "dict_key": "code"},
                {"xml_tag": "StationId", "dict_key": "id"},
            ],
            station_el,
        )
        stations.append(station)
    return sorted(stations, key=lambda k: k["name"])


def get_station_timetable(
    station_code: str, num_mins: int
) -> List[Dict[str, Union[str, datetime, time]]]:
    url = f"{API_BASE_URL}/getStationDataByCodeXML_WithNumMins?StationCode={station_code}&NumMins={num_mins}"
    dom_tree = get_iterable_dom_tree(url)
    station_timetable_items = []
    for station_el in dom_tree:
        station_timetable_item = map_xml_to_dict(
            [
                {"xml_tag": "Traincode", "dict_key": "train_code"},
                {"xml_tag": "Stationfullname", "dict_key": "station_full_name"},
                {"xml_tag": "Stationcode", "dict_key": "station_code"},
                {"xml_tag": "Querytime", "dict_key": "query_time"},
                {"xml_tag": "Traindate", "dict_key": "train_date"},
                {"xml_tag": "Origin", "dict_key": "origin"},
                {"xml_tag": "Destination", "dict_key": "destination"},
                {"xml_tag": "Origintime", "dict_key": "origin_time"},
                {"xml_tag": "Destinationtime", "dict_key": "destination_time"},
                {"xml_tag": "Status", "dict_key": "status"},
                {"xml_tag": "Lastlocation", "dict_key": "last_location"},
                {"xml_tag": "Duein", "dict_key": "due_in"},
                {"xml_tag": "Late", "dict_key": "late"},
                {"xml_tag": "Exparrival", "dict_key": "exp_arrival"},
                {"xml_tag": "Expdepart", "dict_key": "exp_depart"},
                {"xml_tag": "Scharrival", "dict_key": "sch_arrival"},
                {"xml_tag": "Schdepart", "dict_key": "sch_depart"},
                {"xml_tag": "Direction", "dict_key": "direction"},
                {"xml_tag": "Traintype", "dict_key": "train_type"},
                {"xml_tag": "Locationtype", "dict_key": "location_type"},
            ],
            station_el,
        )
        station_timetable_item["query_time"] = datetime.strptime(
            station_timetable_item["query_time"], "%H:%M:%S"
        ).time()
        station_timetable_item["train_date"] = convert_date_format(
            station_timetable_item["train_date"]
        )
        station_timetable_item["origin_time"] = parse_time_hh_mm(
            station_timetable_item["origin_time"]
        )
        station_timetable_item["destination_time"] = parse_time_hh_mm(
            station_timetable_item["destination_time"]
        )
        station_timetable_item["exp_arrival"] = parse_time_hh_mm(
            station_timetable_item["exp_arrival"]
        )
        station_timetable_item["exp_depart"] = parse_time_hh_mm(
            station_timetable_item["exp_depart"]
        )
        station_timetable_item["sch_arrival"] = parse_time_hh_mm(
            station_timetable_item["sch_arrival"]
        )
        station_timetable_item["sch_depart"] = parse_time_hh_mm(
            station_timetable_item["sch_depart"]
        )
        station_timetable_items.append(station_timetable_item)
    return station_timetable_items


def search_stations(text: str) -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getStationsFilterXML?StationText={text}"
    dom_tree = get_iterable_dom_tree(url)
    stations = []
    for station_el in dom_tree:
        station = map_xml_to_dict(
            [
                {"xml_tag": "StationDesc", "dict_key": "name"},
                {"xml_tag": "StationCode", "dict_key": "code"},
            ],
            station_el,
        )
        stations.append(station)
    return sorted(stations, key=lambda k: k["name"])


def list_trains(
    station_type: Optional[str] = "A",
) -> List[Dict[str, Union[str, datetime]]]:
    url = f"{API_BASE_URL}/getCurrentTrainsXML_WithTrainType?TrainType={station_type}"
    dom_tree = get_iterable_dom_tree(url)
    trains = []
    for train_el in dom_tree:
        train = map_xml_to_dict(
            [
                {"xml_tag": "TrainCode", "dict_key": "code"},
                {"xml_tag": "TrainDate", "dict_key": "date"},
                {"xml_tag": "TrainStatus", "dict_key": "status"},
                {"xml_tag": "TrainLatitude", "dict_key": "latitude"},
                {"xml_tag": "TrainLongitude", "dict_key": "longitude"},
                {"xml_tag": "PublicMessage", "dict_key": "public_message"},
                {"xml_tag": "Direction", "dict_key": "direction"},
            ],
            train_el,
        )
        train["date"] = convert_date_format(train["date"])
        trains.append(train)
    return trains


def get_train_movements(train_code: str, date: datetime) -> List[Dict[str, str]]:
    url = f"{API_BASE_URL}/getTrainMovementsXML?TrainId={train_code}&TrainDate={date.strftime('%d %m %Y')}"
    dom_tree = get_iterable_dom_tree(url)
    movements = []
    for movement_el in dom_tree:
        movement = map_xml_to_dict(
            [
                {"xml_tag": "TrainCode", "dict_key": "code"},
                {"xml_tag": "TrainDate", "dict_key": "date"},
                {"xml_tag": "LocationCode", "dict_key": "location_code"},
                {"xml_tag": "LocationFullName", "dict_key": "location_full_name"},
                {"xml_tag": "LocationOrder", "dict_key": "location_order"},
                {"xml_tag": "LocationType", "dict_key": "location_type"},
                {"xml_tag": "TrainOrigin", "dict_key": "train_origin"},
                {"xml_tag": "TrainDestination", "dict_key": "train_destination"},
                {"xml_tag": "ScheduledArrival", "dict_key": "scheduled_arrival"},
                {"xml_tag": "ScheduledDeparture", "dict_key": "scheduled_departure"},
                {"xml_tag": "ExpectedArrival", "dict_key": "expected_arrival"},
                {"xml_tag": "ExpectedDeparture", "dict_key": "expected_departure"},
                {"xml_tag": "Arrival", "dict_key": "arrival"},
                {"xml_tag": "Departure", "dict_key": "departure"},
                {"xml_tag": "AutoArrival", "dict_key": "auto_arrival"},
                {"xml_tag": "AutoDepart", "dict_key": "auto_depart"},
                {"xml_tag": "StopType", "dict_key": "stop_type"},
            ],
            movement_el,
        )
        movement["date"] = convert_date_format(movement["date"])
        movement["scheduled_arrival"] = parse_time_hh_mm_ss(
            movement["scheduled_arrival"]
        )
        movement["scheduled_departure"] = parse_time_hh_mm_ss(
            movement["scheduled_departure"]
        )
        movement["expected_arrival"] = parse_time_hh_mm_ss(movement["expected_arrival"])
        movement["expected_departure"] = parse_time_hh_mm_ss(
            movement["expected_departure"]
        )
        movements.append(movement)
    return movements
