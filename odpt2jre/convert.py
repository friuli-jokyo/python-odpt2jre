
import odpttraininfo as odpt

from .intermediate_components.train_information import TrainInformation
from .text_format import jr_east, rinkai, toei, tokyo_metro, yokohama_municipal


def from_odpt_list(info_list: list[odpt.TrainInformation]) -> list[TrainInformation]:

    result:list[TrainInformation] = []

    for single_info in info_list:
        match single_info.get_company():
            case "JR-East"|"MIR"|"Yurikamome":
                result += jr_east.to_jre(single_info)
            case "YokohamaMunicipal":
                result += yokohama_municipal.to_jre(single_info)
            case "TWR":
                result += rinkai.to_jre(single_info)
            case "TokyoMetro":
                result += tokyo_metro.to_jre(single_info)
            case "Toei":
                result += toei.to_jre(single_info)
            case _:
                result += jr_east.to_jre(single_info)

    return result
