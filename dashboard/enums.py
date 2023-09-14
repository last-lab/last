from enum import IntEnum, Enum

from tortoise.fields.data import CharEnumType


class ProductType(IntEnum):
    article = 1
    page = 2


class Status(IntEnum):
    on = 1
    off = 0


class GenderType(IntEnum):
    female = 0
    male = 1


# datamanager
class ScoreWayType(IntEnum):
    system = 0
    human = 1


class EvaluationType(IntEnum):
    auto_ai_critique = 0,  # "auto_ai_critique"  # 系统评分
    human_scoring = 1,  # "human_scoring"  # 人工评分
    auto_exact_match = 2  # "auto_exact_match"
    auto_similarity_match = 3  # "auto_similarity_match"
    human_a_b_testing = 4  # "human_a_b_testing"
    human_ranking = 5  # "human_ranking"
    human_boxing = 6  # "human_boxing"


# datamanager end


class EvalStatus(IntEnum):
    on_progress = 0
    error = 1
    un_labeled = 2
    finish = 3
