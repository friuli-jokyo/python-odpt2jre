
import odpttraininfo as odpt
from odpt2jre.intermediate_components.status import StatusEnum

from ..intermediate_components.cause import Cause, CauseName
from ..intermediate_components.direction import Direction
from ..intermediate_components.station import BetweenStations, SingleStation
from ..intermediate_components.train_information import TrainInformation
from . import common
from .field import embed_field, find_all_field


def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info)]

    result:TrainInformation = TrainInformation(info)
    result.text_raw.ja = embed_field( info.train_information_text.ja )

    info_text = result.text_raw.ja

    #if match := re.match( r"^(.+?駅で|)(.+?)のため", info.train_information_text.ja ):
    #    result.cause = Cause([match[2]])

    for field in find_all_field(info_text):
        match field[0]:
            case SingleStation.header:
                if result.cause:
                    result.cause.sections.append(SingleStation(field[1]))
            case BetweenStations.header:
                if result.cause:
                    result.cause.sections.append(BetweenStations(field[1]))
            case Direction.header:
                result.status_main.modifiers[0].direction = Direction(field[1])
            case CauseName.header:
                result.cause = Cause(field[1])

    if "遅延" in info_text:
        result.status_main.enum = StatusEnum.DELAY
    if "運転見合わせ" in info_text:
        result.status_main.enum = StatusEnum.OPERATION_STOP

    return [result]
