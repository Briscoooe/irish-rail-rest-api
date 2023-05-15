from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class StationType(ExtendedEnum):
    stops = "stops"  # Stops
    dart = "dart"  # DART
    mainline = "mainline"  # Mainline


station_type_map = {
    "stops": "S",
    "dart": "D",
    "mainline": "M",
}


class LocationType(ExtendedEnum):
    O = "O"  # Origin
    T = "T"  # Timing Point
    S = "S"  # Stop
    D = "D"  # Destination


class StopType(ExtendedEnum):
    C = "C"  # Current
    N = "N"  # Next


class TrainStatus(ExtendedEnum):
    N = "N"  # Not running yet
    R = "R"  # Running
