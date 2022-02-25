import odpttraininfo as odpt

from ..intermediate_components.status import StatusEnum
from ..intermediate_components.train_information import TrainInformation


def normal_operation(info:odpt.TrainInformation) -> TrainInformation:
    result = TrainInformation(info)
    result.status_main.enum = StatusEnum.NORMAL

    return result
