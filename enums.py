from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class StationType(ExtendedEnum):
    A = "A"  # All
    S = "S"  # Stops
    D = "D"  # DART
    M = "M"  # Mainline


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
