import re

from ..intermediate_components import *

FULL_TO_HALF = str.maketrans(
    {
        "０":"0",
        "１":"1",
        "２":"2",
        "３":"3",
        "４":"4",
        "５":"5",
        "６":"6",
        "７":"7",
        "８":"8",
        "９":"9",
    }
)

CAUSE = "\\[Cause:\\d+?\\]"
COMPANY = "\\[Company:\\[\\-a-zA-Z0-9\\._]+?\\]"
CLOCK_TIME = "\\[CLK:\\d+?\\]"
STATION = "\\[Sta:\\d+?\\]"
SINGLE_STA = f"\\[SingleSta:{STATION}\\]"

def embed_field(text:str) -> str:

    # 文字列としての正規化(1/2)
    text = text.replace("ヶ","ケ")
    text = text.replace("停留場","駅")
    text = text.replace("お客様","お客さま")
    text = text.replace("ホームドア","ホーム扉")

    # テーブル付き単語
    text = LineName.embed_field(text)
    text = StationName.embed_field(text)
    text = CompanyName.embed_field(text)
    text = CauseName.embed_field(text)

    # 時刻
    text = re.sub( r"(\d+)時(\d+)分", r"[CLK:\1,\2]", text )
    text = re.sub( r"(\d+)時", r"[CLK:\1,00]", text )
    text = re.sub( r"正午", r"[CLK:12,00]", text )
    text = re.sub( r"(\d+)[:：](\d+)", r"[CLK:\1,\2]", text )

    # 駅方面
    text = re.sub( f"({STATION})駅?方面", r"[Direction:\1]", text )

    # その他方面
    text = DirectionEnum.embed_field(text)

    # 方面付き路線
    text = re.sub( f"\\[Line:(.+?)\\]（({Direction.regex})）", r"[Line:\1,\2]", text )
    text = re.sub( f"\\[Line:(.+?)\\] ({Direction.regex})", r"[Line:\1,\2]", text )

    # 駅間
    text = re.sub( f"({STATION})駅?[〜～]({STATION})駅?[〜～]({STATION})駅?間?", r"[BetweenSta:\1,\2,\3]", text )
    text = re.sub( f"({STATION})駅?[〜～]({STATION})駅?間?", r"[BetweenSta:\1,\2]", text )
    text = re.sub( f"({STATION})駅?から({STATION})駅?", r"[BetweenSta:\1,\2]", text )

    # 単駅
    text = re.sub( f"({STATION})駅", r"[SingleSta:\1]", text )

    # 以.
    text = re.sub( f"({SINGLE_STA})以(東|西|南|北)", r"[OrdinalFromSta:\1,\2]", text )

    # 文字列としての正規化(2/2)
    text = text.translate(FULL_TO_HALF) # 数字のみ

    return text

def find_all_field(text: str) -> list[list[str]]:

    brackets_count: int = 0
    start_index: int = 0
    fields: list[str] = []
    result :list[list[str]] = []

    for i, char in enumerate(text):
        if char=="[":
            if brackets_count == 0:
                start_index = i
            brackets_count += 1
        elif char=="]":
            brackets_count -= 1
            if brackets_count==0:
                fields.append( text[start_index:i+1] )
            elif brackets_count<0:
                return []

    if brackets_count!=0:
        return []

    for field in fields:
        if code := re.search(r"^\[([a-zA-Z]+):", field):
            result.append( [code[1],field] )


    return result

def find_field(text: str, header:Optional[str] = None ) -> list[str]:
    for field in find_all_field(text):
        if field[0] == header or header is None:
            return field
    return []