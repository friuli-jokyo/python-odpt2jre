
from typing import Optional, TypedDict
from odpttraininfo.odpt_components import MultiLanguageDict


class MultiLanguageDictWithId(MultiLanguageDict):
    id:str

class TrainInformationDict(TypedDict):

    lineName: MultiLanguageDictWithId
    cause: Optional[MultiLanguageDictWithId]
    direction: MultiLanguageDictWithId
    section: MultiLanguageDict
    infoStatus: MultiLanguageDictWithId
    infoStatusIcon: str
    infoText: MultiLanguageDict
    rawText: MultiLanguageDict
    causeTime: Optional[str]
    resumeTime: Optional[str]
    date: str
    valid: Optional[str]
