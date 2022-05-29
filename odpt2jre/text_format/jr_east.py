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
        gen.status_main.enum = StatusEnum.NOTICE
        gen.text_raw.ja = embed_field( info_text )
        gen.text_info.ja = info_text
        if "[Line:JR-East.UenoTokyo]は、" in info_text:
            gen.line_header = LineName("JR-East.UenoTokyo")

        if re.search( r"運転再開見込は.+?に変更になりました", gen.text_raw.ja ):
            gen.status_main.enum = StatusEnum.OPERATION_WILL_RESUME
        elif re.search( r"運転再開は.+?を見込んでいます", gen.text_raw.ja ):
            gen.status_main.enum = StatusEnum.OPERATION_WILL_RESUME
        elif re.search( r"運転を再開しました", gen.text_raw.ja ):
            gen.status_main.enum = StatusEnum.OPERATION_RESUMED
        else:
            main_status_text = gen.text_raw.ja.split("。")[0]
            if main_status_text.endswith("遅れがでています"):
                gen.status_main.enum = StatusEnum.DELAY
            elif main_status_text.endswith("遅れと運休がでています"):
                gen.status_main.enum = StatusEnum.DELAY
            elif main_status_text.endswith("運休となっています"):
                gen.status_main.enum = StatusEnum.SOME_TRAIN_CANCEL
                gen.status_main.modifiers[0].some_train = True
            elif re.search(r"直通運転(（.*?）|)を中止しています", main_status_text):
                gen.status_main.enum = StatusEnum.DIRECT_STOP
            elif main_status_text.endswith("運転を見合わせています"):
                gen.status_main.enum = StatusEnum.OPERATION_STOP

        result += [gen]

    return result

