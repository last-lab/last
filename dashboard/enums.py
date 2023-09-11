from enum import IntEnum


class ProductType(IntEnum):
    article = 1
    page = 2


class Status(IntEnum):
    on = 1
    off = 0


class GenderType(IntEnum):
    female = 0
    male = 1


class RiskTypes(IntEnum):
    safe = 0
    unsafe = 1


class RiskSubTypes(IntEnum):
    regime = 0

# datamanager
class ScoreWayType(IntEnum):
    system = 0
    human = 1


# datamanager end


class EvalStatus(IntEnum):
    on_progress = 0
    error = 1
    un_labeled = 2
    finish = 3

