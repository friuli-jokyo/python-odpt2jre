

def concat_ja( expression_list: list[str]) -> str:

    result_list: list[str] = []

    for expression in expression_list:
        if expression:
            result_list.append(expression)

    match len(result_list):
        case 0:
            return ""
        case 1:
            return result_list[0]
        case 2:
            return "および".join(result_list)
        case _:
            return "・".join(result_list)

def concat_en( expression_list: list[str]) -> str:

    result_list: list[str] = []

    for expression in expression_list:
        if expression:
            result_list.append(expression)

    match len(result_list):
        case 0:
            return ""
        case 1:
            return result_list[0]
        case 2:
            return " and ".join(result_list)
        case _:
            return ", ".join(result_list[:-1]) + ", and " + result_list[-1]