
import odpttraininfo as odpt
from odpt2jre.intermediate_components.line import LineName
from odpt2jre.intermediate_components.status import StatusEnum

from ..intermediate_components.cause import Cause, CauseName
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

    amari: list[list[str]] = []

    for field in find_all_field(info_text):
        match field[0]:
            case CauseName.header:
                result.cause = Cause(field[1])
            case LineName.header:
                if result.cause:
                    result.cause.lines.append(LineName(field[1]))
                else:
                    amari.append(field)

    for field in amari:
        match field[0]:
            case LineName.header:
                if result.cause:
                    result.cause.lines.append(LineName(field[1]))

    if "遅れ" in info_text:
        result.status_main.enum = StatusEnum.DELAY

    return [result]
