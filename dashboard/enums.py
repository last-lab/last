from enum import IntEnum

from last.services.enums import Method


class ProductType(IntEnum):
    article = 1
    page = 2


class Status(IntEnum):
    on = 1
    off = 0


class GenderType(IntEnum):
    female = 0
    male = 1


class EvalStatus(IntEnum):
    on_progress = 0
    error = 1
    un_labeled = 2
    finish = 3
