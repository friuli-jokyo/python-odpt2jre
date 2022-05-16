
import copy
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

def remove_unimportant(dic:TrainInformationDict) -> dict[str,object]:

    result = dict(copy.deepcopy(dic))

    for key, value in list(result.items()):
        if key in ["rawText","date","valid"]:
            result.pop(key, None)
        if value is None:
            result.pop(key, None)

    return result

def list_diff(new: list[TrainInformationDict], old: list[TrainInformationDict]) -> tuple[list[TrainInformationDict], list[TrainInformationDict]]:

    new_essence = [ remove_unimportant(n) for n in new ]
    old_essence = [ remove_unimportant(o) for o in old ]

    added:list[TrainInformationDict] = []
    for i in range(len(new)):
        for j in range(len(old)):
            if new_essence[i] == old_essence[j]:
                break
        else:
            added.append(new[i])

    removed:list[TrainInformationDict] = []
    for i in range(len(old)):
        for j in range(len(new)):
            if old_essence[i] == new_essence[j]:
                break
        else:
            removed.append(old[i])

    return added, removed