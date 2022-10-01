from enum import Enum


class StationType(Enum):
    A = "A", "All"  # All stations
    S = "S"  # Suburban stations
    D = "D"  # Dublin stations
    M = "M"  # Mainline stations


class LocationTypeEnum(Enum):
    O = "O"  # Origin
    T = "T"  # Timing Point
    S = "S"  # Stop
    D = "D"  # Destination


class StopTypeEnum(Enum):
    C = "C"  # Current
    N = "N"  # Next


class TrainStatus(Enum):
    N = "N"  # Not running yet
    R = "R"  # Running
