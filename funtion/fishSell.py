import json

def sell_fish(player_id, fish_id, quantity):
    members = json.load(open("member.json", "r", encoding="utf-8"))
    fish_data = json.load(open("fish.json", "r", encoding="utf-8"))

    player = members.get(player_id)
    if not player:
        return {"success": False, "message": "플레이어 없음"}

    fish = fish_data.get(str(fish_id))
    if not fish:
        return {"success": False, "message": "잘못된 물고기 ID"}

    idx = int(fish_id) - 1  # 인덱스 보정
    owned = player["Fish_cnt"][idx]

    if owned <= 0:
        return {"success": False, "message": "판매할 물고기가 없습니다."}
    if quantity > owned:
        return {"success": False, "message": f"보유 수량({owned}마리)보다 많이 팔 수 없습니다."}

    price = fish["price"]
    total = price * quantity
    player["Fish_cnt"][idx] -= quantity
    player["money"] += total

    members[player_id] = player
    json.dump(members, open("member.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)

    return {
        "success": True,
        "message": f"{fish['name']} {quantity}마리 판매 완료! (+{total}원)",
        "earned_money": total,
        "remaining_money": player["money"],
        "remaining_fish_count": player["Fish_cnt"][idx]
    }
