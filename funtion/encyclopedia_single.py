import json

def get_fish_info(player_id, fish_id):
    members = json.load(open("member.json", "r", encoding="utf-8"))
    fish_data = json.load(open("fish.json", "r", encoding="utf-8"))
    player = members.get(player_id)
    fish = fish_data.get(str(fish_id))
    if not player or not fish:
        return {"success": False, "message": "플레이어나 물고기 정보가 없습니다."}
    count = player["Fish_cnt"][int(fish_id)]
    return {"success": True, "fish": fish, "count": count}
