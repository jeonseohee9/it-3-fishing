import random
import json
import json_util.json_io as json_io


def simulate_stock_price(initial_price, min_change=-20, max_change=40):
    """
    주어진 초기 주식 가격에 랜덤 증감율을 적용하여 새로운 주가를 계산한다.
    
    Parameters:
    - initial_price (float): 초기 주식 가격
    - min_change (float): 최소 변동률 (%)
    - max_change (float): 최대 변동률 (%)s
    
    Returns:
    - new_price (float): 변동된 새로운 주가
    """
    # -20%에서 +40% 사이의 증감율을 랜덤으로 생성
    change_percentage = random.uniform(min_change, max_change)
    
    # 변동된 주가 계산
    new_price = initial_price * (1 + change_percentage / 100)
    
    return int(new_price)


def change_stock(id):
    userData = json_io.json_file_to_dict()
    userData[id]["stock"]["NDVA"] = simulate_stock_price(userData[id]["stock"]["NDVA"])
    userData[id]["stock"]["DSL"] = simulate_stock_price(userData[id]["stock"]["DSL"])
    json_io.dict_to_json_file(userData)

    return {"success": True, 'data': userData[id]}

def buy_stock(id, stock_name, buy_num):
    # json_file_to_dict 함수를 호출하여 userData를 가져옴
    userData = json_io.json_file_to_dict()
    if stock_name == "NDVA":
        if buy_num > userData[id]["total_shares"]["NDVA"]:
            return {'success': False}
        else:
            if userData[id]["money"] < userData[id]["stock"]["NDVA"] * buy_num:
                return {'success': False}
            else:
                userData[id]["money"] -= userData[id]["stock"]["NDVA"] * buy_num
                userData[id]["total_shares"]["NDVA"] = max(int(userData[id]["total_shares"]["NDVA"] - buy_num), 0)
                userData[id]["player_shares"]["NDVA"] += buy_num

    elif stock_name == "DSL":
        if buy_num > userData[id]["total_shares"]["DSL"]:
            return {'success': False}
        else:
            if userData[id]["money"] < userData[id]["stock"]["DSL"] * buy_num:
                return {'success': False}
            else:
                userData[id]["money"] -= userData[id]["stock"]["DSL"] * buy_num
                userData[id]["total_shares"]["DSL"] = max(int(userData[id]["total_shares"]["DSL"] - buy_num), 0)
                userData[id]["player_shares"]["DSL"] += buy_num

    # 업데이트된 데이터를 저장
    json_io.dict_to_json_file(userData)
    return {"success": True, 'data': userData[id]}

def sell_stock(id, stock_name, sell_num):
    # json_file_to_dict 함수를 호출하여 userData를 가져옴
    userData = json_io.json_file_to_dict()

    if stock_name == "NDVA":
        if sell_num > userData[id]["player_shares"]["NDVA"]:
            return {'success': False}
        else:
            userData[id]["player_shares"]["NDVA"] -= sell_num
            userData[id]["money"] += userData[id]["stock"]["NDVA"] * sell_num
            userData[id]["total_shares"]["NDVA"] += sell_num
    
    elif stock_name == "DSL":
        if sell_num > userData[id]["player_shares"]["DSL"]:
            return {"success": False}
        else:
            userData[id]["player_shares"]["DSL"] -= sell_num
            userData[id]["money"] += userData[id]["stock"]["DSL"] * sell_num
            userData[id]["total_shares"]["DSL"] += sell_num

    # 업데이트된 데이터를 저장
    json_io.dict_to_json_file(userData)
    return {"success": True, 'data': userData[id]}

def load_userData():
    with open("user_info.json", "r") as f:
        userData = json.load(f)
    return userData

def dump_userData(userData):
    with open("user_info.json", "w") as f:
        json.dump(userData, f, indent=4)
