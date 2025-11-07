import json, random

def upgrade_rod_level1to5(player_id, members_file="member.json"):
    members = json.load(open(members_file, "r", encoding="utf-8"))
    player = members.get(player_id)
    if not player:
        return {"success": False, "message": "플레이어를 찾을 수 없습니다."}

    current_level = int(player.get("rod_level", 1))
    if current_level >= 5:
        return {
            "success": False,
            "player_id": player_id,
            "previous_rod_level": current_level,
            "new_rod_level": current_level,
            "remaining_money": player.get("money", 0),
            "message": "최대 강화 레벨입니다."
        }

    # 레벨별 강화 확률 및 비용
    rod_level_data = {
        1: {"success_rate": 0.9, "cost_money": 10000},
        2: {"success_rate": 0.7, "cost_money": 20000},
        3: {"success_rate": 0.5, "cost_money": 30000},
        4: {"success_rate": 0.3, "cost_money": 40000},
        5: {"success_rate": 0.1, "cost_money": 50000}
    }

    data = rod_level_data[current_level]
    success_rate = data["success_rate"]
    cost_money = data["cost_money"]

    if player["money"] < cost_money:
        return {
            "success": False,
            "player_id": player_id,
            "previous_rod_level": current_level,
            "new_rod_level": current_level,
            "remaining_money": player["money"],
            "message": "돈이 부족합니다."
        }

    player["money"] -= cost_money

    if random.random() < success_rate:
        player["rod_level"] = current_level + 1
        message = f" 낚싯대 강화 성공! 현재 레벨: {player['rod_level']}"
        success = True
    else:
        message = "강화 실패. 돈만 차감되었습니다."
        success = False

    members[player_id] = player
    json.dump(members, open(members_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

    return {
        "success": success,
        "player_id": player_id,
        "previous_rod_level": current_level,
        "new_rod_level": player["rod_level"],
        "remaining_money": player["money"],
        "message": message
    }
