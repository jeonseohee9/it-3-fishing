import json

def buy_bait(player_id, bait_id, quantity):
    members = json.load(open("member.json", "r", encoding="utf-8"))
    bait_data = json.load(open("bait.json", "r", encoding="utf-8"))

    player = members.get(player_id)
    bait = bait_data[str(bait_id)]
    cost = bait["price"] * quantity

    if player["money"] < cost:
        return {"success": False, "message": "돈이 부족합니다."}

    player["money"] -= cost
    player["bait_inventory"][str(bait_id)] = player["bait_inventory"].get(str(bait_id), 0) + quantity
    members[player_id] = player
    json.dump(members, open("member.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    return {"success": True, "message": f"{bait['name']} {quantity}개 구매 완료"}
