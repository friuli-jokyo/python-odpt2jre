import odpttraininfo as odpt

from ..intermediate_components.status import StatusEnum
from ..intermediate_components.train_information import TrainInformation

_trans_macron = str.maketrans({
    "Ā":"A",
    "Ī":"I",
    "Ū":"U",
    "Ē":"E",
    "Ō":"O",
    "ā":"a",
    "ī":"i",
    "ū":"u",
    "ē":"e",
    "ō":"o",
})

def removeMacrons(text:str):
    return text.translate(_trans_macron)

def normal_operation(info:odpt.TrainInformation, remove_macrons:bool = False) -> TrainInformation:
    result = TrainInformation(info)
    result.status_main.enum = StatusEnum.NORMAL

    if remove_macrons and result.line_header.en:
        result.line_header.en = removeMacrons(result.line_header.en)

    return result
