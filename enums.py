from enum import Enum


class StationType(Enum):
    A = "A"
    S = "S"
    D = "D"
    M = "M"


class LocationTypeEnum(Enum):
    O = "O"
    T = "T"
    S = "S"
    D = "D"


class StopTypeEnum(Enum):
    C = "C"
    N = "N"


class TrainStatus(Enum):
    N = "N"
    R = "R"
