import re

import odpttraininfo as odpt

from .field_string import embed_field
from ..intermediate_components import *
from . import common

def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info)]

    result:list[TrainInformation] = []

    raw_info_text = info.train_information_text.ja
    line_name_regrex = r"(車|線|ライン|」|）)は、"
    split_count = len( re.findall(line_name_regrex, raw_info_text) )
    split_match = re.fullmatch( r"(.*?。|)" + ( r"([^。]*" + line_name_regrex + r".+。)" )*split_count ,raw_info_text )

    if split_match:
        if split_match[1]:
            info_text_list = [split_match[1]]
        else:
            info_text_list = []
        info_text_list += split_match.groups()[1::2]
    else:
        info_text_list = [raw_info_text]

    for info_text in info_text_list:

        gen = TrainInformation(info)
        gen.text_raw.ja = embed_field( info_text )
        gen.text_info.ja = info_text
        if "上野東京ラインは、" in info_text:
            gen.line_header = LineName("JR-East.UenoTokyo")



        result += [gen]

    return result

