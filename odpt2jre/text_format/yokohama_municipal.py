
import odpttraininfo as odpt
from ..intermediate_components import *
from . import common
from .field_string import embed_field, find_all_field


def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info)]

    result:TrainInformation = TrainInformation(info)
    result.text_raw.ja = embed_field( info.train_information_text.ja )

    info_text = result.text_raw.ja

    if _match := re.fullmatch( r"(.+?)のため(.+?)", info_text ):
        cause_text = _match[1]
        info_text = _match[2]

        for field in find_all_field(cause_text):
            match field[0]:
                case CauseName.header:
                    result.cause = Cause(field[1])

        for field in find_all_field(cause_text):
            match field[0]:
                case SingleStation.header:
                    if result.cause:
                        result.cause.sections.append(SingleStation(field[1]))
                case BetweenStations.header:
                    if result.cause:
                        result.cause.sections.append(BetweenStations(field[1]))


    field_list = find_all_field(info_text)

    for field in field_list:
        match field[0]:
            case Direction.header:
                result.status_main.modifiers[0].direction = Direction(field[1])

    for field in field_list:
        match field[0]:
            case BetweenStations.header:
                if result.cause:
                    result.status_main.modifiers[0].sections.append(BetweenStations(field[1]))

    if "[Cause:47]" in info_text:
        result.status_main.enum = StatusEnum.DELAY
    if "運転見合わせ" in info_text:
        result.status_main.enum = StatusEnum.OPERATION_STOP

    return [result]
