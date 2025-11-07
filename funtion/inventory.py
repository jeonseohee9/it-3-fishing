import json

def get_inventory(player_id):
    members = json.load(open("member.json", "r", encoding="utf-8"))
    fish_data = json.load(open("fish.json", "r", encoding="utf-8"))

    player = members.get(player_id)
    if not player:
        return {"success": False, "message": "플레이어 없음"}

    caught_fish = []
    fish_cnt_list = player.get("Fish_cnt", [])

    for idx, count in enumerate(fish_cnt_list, start=1):
        if count > 0 and str(idx) in fish_data:
            fish_info = fish_data[str(idx)]
            caught_fish.append({
                "fish_id": idx,
                "name": fish_info["name"],
                "count": count,
                "price": fish_info["price"],
                "total_value": fish_info["price"] * count
            })

    return {
        "success": True,
        "inventory": {
            "money": player["money"],
            "rod_level": player["rod_level"],
            "bait_inventory": player["bait_inventory"],
            "caught_fish": caught_fish  
        }
    }
