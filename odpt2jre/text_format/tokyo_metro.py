
import copy
import odpttraininfo as odpt
from ..intermediate_components import *
from . import common
from .field_string import embed_field, find_all_field, find_field

staList = {
        # [Line:Seibu]内は「[Line:Seibu]内～[Sta:2035]」なので無視
        "TokyoMetro.Yurakucho":[["[Line:Tobu]","[Sta:1510]","[Sta:7086]","[Sta:7087]","[Sta:7088]","[Sta:7089]","[Sta:2035]","[Sta:7090]","[Sta:7091]","[Sta:13]","[Sta:7092]","[Sta:7093]","[Sta:7094]","[Sta:33]","[Sta:34]","[Sta:7095]","[Sta:7096]","[Sta:7097]","[Sta:30]","[Sta:7098]","[Sta:7099]","[Sta:7100]","[Sta:7101]","[Sta:7102]","[Sta:473]"]],
        # 「[Line:JR-East]内」は[Sta:439]側のみという仮定
        "TokyoMetro.Tozai":[["[Line:ToyoRapidRailway.ToyoRapidRailway]","[Line:JR-East]","[Sta:439]","[Sta:7074]","[Sta:7073]","[Sta:7072]","[Sta:7071]","[Sta:7070]","[Sta:7069]","[Sta:7068]","[Sta:7067]","[Sta:7066]","[Sta:7065]","[Sta:7064]","[Sta:7054]","[Sta:7009]","[Sta:7041]","[Sta:7063]","[Sta:7062]","[Sta:33]","[Sta:7061]","[Sta:7060]","[Sta:15]","[Sta:7059]","[Sta:40]"]],
        "TokyoMetro.Fukutoshin":[["[Line:Tokyu]","[Sta:20]","[Sta:7077]","[Sta:7121]","[Sta:7037]","[Sta:7120]","[Sta:7119]","[Sta:7118]","[Sta:13]","[Sta:7091]","[Sta:7090]","[Sta:2035]","[Sta:7089]","[Sta:7088]","[Sta:7087]","[Sta:7086]","[Sta:1510]","[Line:Tobu]"]],
        "TokyoMetro.Marunouchi":[["[Sta:43]","[Sta:7031]","[Sta:7032]","[Sta:7033]","[Sta:7034]","[Sta:7035]","[Sta:7036]","[Sta:17]","[Sta:7037]","[Sta:7038]","[Sta:7039]","[Sta:35]","[Sta:7004]","[Sta:7040]","[Sta:1521]","[Sta:7007]","[Sta:1]","[Sta:7041]","[Sta:7042]","[Sta:31]","[Sta:7043]","[Sta:7044]","[Sta:7045]","[Sta:7046]","[Sta:13]"],["[Sta:7122]","[Sta:7123]","[Sta:40][Sta:29]","[Sta:7035]"]],
        "TokyoMetro.Hanzomon":[["[Line:Tokyu]","[Sta:20]","[Sta:7001]","[Sta:7003]","[Sta:7096]","[Sta:7103]","[Sta:7062]","[Sta:7104]","[Sta:7041]","[Sta:7010]","[Sta:7105]","[Sta:7106]","[Sta:7107]","[Sta:431]","[Sta:1003]","[Line:Tobu]"]],
        "TokyoMetro.Namboku":[["[Line:Tokyu]","[Sta:22]","[Sta:7108]","[Sta:7109]","[Sta:7110]","[Sta:7111]","[Sta:7005]","[Sta:7096]","[Sta:35]","[Sta:34]","[Sta:33]","[Sta:7044]","[Sta:7112]","[Sta:7113]","[Sta:10]","[Sta:7114]","[Sta:246]","[Sta:7115]","[Sta:7116]","[Sta:7117]","[Line:SaitamaRailway.SaitamaRailway]"]],
        "TokyoMetro.Hibiya":[["[Line:Tokyu]","[Sta:5002]","[Sta:21]","[Sta:7047]","[Sta:7048]","[Sta:7049]","[Sta:7050]","[Sta:1521]","[Sta:7051]","[Sta:7007]","[Sta:7052]","[Sta:7053]","[Sta:470]","[Sta:7054]","[Sta:7055]","[Sta:7056]","[Sta:3]","[Sta:7057]","[Sta:5]","[Sta:222]","[Sta:7058]","[Sta:343]","[Sta:344]","[Line:Tobu]"]],
        "TokyoMetro.Chiyoda":[["[Line:Odakyu]","[Sta:7075]","[Sta:7076]","[Sta:7077]","[Sta:7001]","[Sta:7078]","[Sta:7079]","[Sta:7040]","[Sta:1521]","[Sta:7051]","[Sta:7080]","[Sta:7041]","[Sta:7081]","[Sta:7082]","[Sta:7083]","[Sta:7084]","[Sta:8]","[Sta:3002]","[Sta:344]","[Sta:345]"],["[Sta:345]","[Sta:7085]"]],
        "TokyoMetro.Ginza":[["[Sta:20]","[Sta:7001]","[Sta:7002]","[Sta:7003]","[Sta:7004]","[Sta:7005]","[Sta:7006]","[Sta:29]","[Sta:7007]","[Sta:7008]","[Sta:7009]","[Sta:7010]","[Sta:2]","[Sta:7011]","[Sta:7012]","[Sta:5]","[Sta:7013]","[Sta:7014]","[Sta:1001]"]]
}

def to_jre(info:odpt.TrainInformation) -> list[TrainInformation]:

    if not info.train_information_status:
        return [common.normal_operation(info,remove_macrons=True)]

    result:TrainInformation = TrainInformation(info)
    result.text_raw.ja = embed_field( info.train_information_text.ja )

    if result.line_header.en:
        result.line_header.en = common.removeMacrons(result.line_header.en)

    info_text = result.text_raw.ja

    if match := re.fullmatch( r"(.+?)のため、(.+?)。(.*)", info_text ):
        cause_text = match[1]
        main_status_text = match[2]
        sub_text_list = match[3].split("。")
    elif match := re.fullmatch( r"(.+?)。(.*)", info_text ):
        cause_text = ""
        main_status_text = match[1]
        sub_text_list = match[2].split("。")
    else:
        return [common.normal_operation(info)]

    if match := re.fullmatch( r"(.*?)運転を見合わせていましたが、(.*?)運転を再開し(.+?)", main_status_text ):
        main_status_text = match[3]
        result.status_occasion.enum = StatusEnum.OPERATION_RESUMED
        if field := find_field(match[2]):
            match field[0]:
                case ClockTime.header:
                    result.time_resume = ClockTime(field[1])

    cause_field_list = find_all_field(cause_text)

    for field in cause_field_list:
        match field[0]:
            case CauseName.header:
                result.cause = Cause(field[1])
            case ClockTime.header:
                result.time_occur = ClockTime(field[1])

    if result.cause:
        for field in cause_field_list:
            match field[0]:
                case LineName.header:
                    result.cause.lines.append( LineName(field[1]) )
                case SingleStation.header:
                    result.cause.sections.append( SingleStation(field[1]) )
                case BetweenStations.header:
                    result.cause.sections.append( BetweenStations(field[1]) )

    main_field_list = find_all_field(main_status_text)

    for field in main_field_list:
        match field[0]:
            case Direction.header:
                result.status_main.modifiers[0].direction = Direction(field[1])
            case BetweenStations.header:
                result.status_main.modifiers[0].sections.append(BetweenStations(field[1]))

    if "ダイヤが乱れています" in main_status_text:
        result.status_main.enum = StatusEnum.DELAY
    elif "遅れが" in main_status_text:
        result.status_main.enum = StatusEnum.DELAY
        if "一部の" in main_status_text:
            result.status_main.modifiers[0].some_train = True
    elif "中止しています" in main_status_text:
        divide_stop_resume(result, main_status_text, True)
    elif re.fullmatch( r"直通運転を中止していましたが、.+?再開しました", main_status_text):
        pass
    elif "全線で運転を見合わせています" in main_status_text:
        result.status_main.enum = StatusEnum.OPERATION_STOP
    elif "折返し運転を行っています" in main_status_text:
        result.status_main.enum = StatusEnum.OPERATION_STOP
    elif "一部列車が運休となって" in main_status_text:
        result.status_main.enum = StatusEnum.SOME_TRAIN_CANCEL
        result.status_main.modifiers[0].some_train = True

    for i,sub_text in enumerate(sub_text_list):
        if match := re.fullmatch( r"(.+?)(只今、.+?振替輸送を実施しています)", sub_text ):
            sub_text_list[i] = match[1]
            sub_text_list.append(match[2])

    for sub_text in sub_text_list:
        if "見込" in sub_text:
            field = find_field(sub_text)
            if field and field[0]=="CLK":
                result.time_resume = ClockTime(field[1])
                if "変更" in sub_text:
                    result.time_resume_changed = True
        elif "運転本数を減らして運転" in sub_text or "一部列車が運休" in sub_text:
            sub = Status()
            result.statuses_sub.append(sub)
            for field in find_all_field(sub_text):
                if field[0] == BetweenStations.header:
                    sub.modifiers[0].sections.append(BetweenStations(field[1]))
        elif subMatch := re.search( r"()この影響で(.+)を中止しています" ,sub_text) or\
			(subMatch := re.search( r"なお、(.+)は再開しました()" ,sub_text)) or\
			(subMatch := re.search( r"なお、(.+)は再開しましたが、(.+)を中止しています" ,sub_text)):
            if subMatch[1]:
                divide_stop_resume(result, subMatch[1], False)
            if subMatch[2]:
                divide_stop_resume(result, subMatch[2], True)
        elif subMatch := re.fullmatch( r"折返し運転区間　(.+?)" ,sub_text):
            if result.status_main.enum == StatusEnum.OPERATION_STOP:
                try:
                    sections = copy.deepcopy(staList[ result.line_header.id ])
                    formatted_text = re.sub(r"\[(SingleSta|BetweenSta):(.+?\])\]",r"\2",subMatch[1]).replace("駅","").replace("間","").replace("内","")
                    stopSections = [ re.split("[〜～\\,]",x) for x in formatted_text.split("　") ]

                    for i, stopSection in enumerate(stopSections): # 方南町支線関連(方南町･中野坂上)
                        if "[Sta:7035]" not in stopSection and "[Sta:7122]" in stopSection:
                            if stopSection[0]=="[Sta:7122]":
                                stopSections[i] = ["[Sta:7035]",stopSection[-1]]
                            else:
                                stopSections[i] = [stopSection[1],"[Sta:7035]"]
                            stopSections.append(["[Sta:7035]","[Sta:7122]"])

                    for stopSection in stopSections:
                        n_sections:list[list[str]] = []
                        for section in sections:
                            if stopSection[0] in section and stopSection[-1] in section:
                                start = section.index(stopSection[0])
                                end = section.index(stopSection[-1])
                                if end<start:
                                    start, end = end, start
                                if start!=0:
                                    start+=1
                                if end==len(section)-1:
                                    end+=1
                                if start==0 or end==len(section):
                                    del section[start:end]
                                    n_sections.append(section)
                                else:
                                    n_sections.append(section[0:start])
                                    n_sections.append(section[end:])
                            else:
                                n_sections.append(section)
                        sections = n_sections

                    for section in sections:
                        section = [ s for s in section if "Line:" not in s ]
                        if len(section)>1:
                            result.status_main.modifiers[0].sections.append(BetweenStations("[BetweenSta:%s,%s]" %(section[0],section[-1])))
                except:
                    pass


    return [result]


def divide_stop_resume( info:TrainInformation, text:str ,stop:bool = True ):

    line_list:list[LineName] = []
    other_list:list[str] = []
    some_cancel:bool = False

    other_suggest_list:list[str] = ["快速運転","女性専用車","急行運転"]
    for suggest in other_suggest_list:
        if suggest in text:
            other_list.append(suggest)

    liner_list:list[str] = ["ＴＨＬＩＮＥＲ","Ｓ−ＴＲＡＩＮ"]
    for liner in liner_list:
        if re.search(liner+r"[0-9０-９・]+号の運転", text):
            some_cancel = True

    for field in find_all_field(text):
        match field[0]:
            case LineName.header:
                line_list.append(LineName(field[1]))

    if line_list or "直通運転" in text:
        if info.status_main.enum==StatusEnum.NULL:
            status = info.status_main
        else:
            status = Status(StatusPlacement.MAIN)
            info.statuses_sub.append(status)
        if stop:
            status.enum = StatusEnum.DIRECT_STOP
        else:
            status.enum = StatusEnum.DIRECT_RESUMED
        for line in line_list:
            status.modifiers[0].lines.append(line)

    if other_list:
        if info.status_main.enum==StatusEnum.NULL:
            status = info.status_main
        else:
            status = Status(StatusPlacement.MAIN)
            info.statuses_sub.append(status)
        if stop:
            status.enum = StatusEnum.STOP
        else:
            status.enum = StatusEnum.RESUMED
        for other in other_list:
            status.modifiers[0].others.append(other)

    if some_cancel and stop:
        status = Status(StatusPlacement.MAIN)
        status.enum = StatusEnum.SOME_TRAIN_CANCEL
        status.modifiers[0].some_train = True
        info.statuses_sub.append(status)
