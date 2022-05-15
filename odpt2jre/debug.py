from datetime import datetime
import odpttraininfo as odpt
from .convert import from_odpt_list


def gen_odpt_info(line:str, text:str) -> odpt.TrainInformation:

    result = odpt.TrainInformation(
    {
        "@id": "urn:ucode:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "@type": "odpt:TrainInformation",
        "dc:date": "0000-00-00T00:00:00+09:00",
        "@context": "http://vocab.odpt.org/context_odpt.jsonld",
        "odpt:trainInformationText": {
            "ja": "平常通り運転しています。"
        },
        "odpt:trainInformationStatus": {
            "ja":"デバッグ"
        }
    })
    result.date = datetime.now()
    result.railway = line
    result.operator = line.split(".")[0]
    result.train_information_text.ja = text

    return result

def gen_jre_info(line:str, text:str) -> list[dict[str,object]]:

    odpt_info = gen_odpt_info(line=line,text=text)

    return [ info.to_dict() for info in from_odpt_list([odpt_info]) ]