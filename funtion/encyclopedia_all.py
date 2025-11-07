import json

def get_player_fish_data(player_id):
    members = json.load(open("member.json", "r", encoding="utf-8"))
    fish_list = json.load(open("fish.json", "r", encoding="utf-8"))
    player = members.get(player_id)
    if not player:
        return {"success": False, "message": "플레이어 없음"}

    collected = sum(1 for x in player["Fish_cnt"] if x > 0)
    return {
        "success": True,
        "player_id": player_id,
        "total_fish": len(fish_list),
        "collected": collected
    }
