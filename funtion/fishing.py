import json
import random

def attempt_fishing(player_id, bait_id=None):
    members = json.load(open("member.json", "r", encoding="utf-8"))
    fish_data = json.load(open("fish.json", "r", encoding="utf-8"))
    bait_data = json.load(open("bait.json", "r", encoding="utf-8"))

    player = members.get(player_id)
    if not player:
        return {"success": False, "message": "플레이어 없음"}

    rod_level = player.get("rod_level", 1)
    bait_inventory = player.get("bait_inventory", {})

    bait = None
    bait_bonus = 0.0
    bait_name = "미끼 없음"

    if bait_id:  # bait_id가 전달된 경우만 처리
        bait = bait_data.get(str(bait_id))
        if not bait:
            return {"success": False, "message": "잘못된 미끼입니다."}

        if bait_inventory.get(str(bait_id), 0) <= 0:
            return {"success": False, "message": f"{bait['name']}이(가) 없습니다."}

        # 미끼 차감
        bait_inventory[str(bait_id)] -= 1
        player["bait_inventory"] = bait_inventory
        bait_bonus = bait["catch_rate_bonus"]
        bait_name = bait["name"]

    #  낚시 확률 
    base_chance = 0.1
    rod_bonus = (rod_level - 1) * 0.05
    catch_chance = min(base_chance + bait_bonus + rod_bonus, 0.8)

    if random.random() > catch_chance:
        members[player_id] = player
        json.dump(members, open("member.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
        return {
            "success": False,
            "message": f"물고기가 도망쳤습니다. (성공 확률: {round(catch_chance*100,1)}%, 사용한 미끼: {bait_name})",
            "remaining_bait": player["bait_inventory"]
        }

    # 낚싯대 이하 레벨만 고려
    level_probs = {1: 0.5, 2: 0.3, 3: 0.15, 4: 0.05, 5: 0.0}
    for lvl in range(rod_level + 1, 6):
        level_probs[lvl] = 0.0

    possible_levels = [lvl for lvl, prob in level_probs.items() if prob > 0]
    weights = [level_probs[lvl] for lvl in possible_levels]
    caught_level = random.choices(possible_levels, weights=weights, k=1)[0]

    fishes_at_level = [fid for fid, f in fish_data.items() if f["level"] == caught_level]
    caught_id = random.choice(fishes_at_level)
    caught_fish = fish_data[caught_id]

    fish_index = int(caught_id) - 1
    fish_cnt = player.get("Fish_cnt", [0] * len(fish_data))
    fish_list = player.get("Fish_list", [0] * len(fish_data))

    fish_cnt[fish_index] += 1
    fish_list[fish_index] = 1

    player["Fish_cnt"] = fish_cnt
    player["Fish_list"] = fish_list

    members[player_id] = player
    json.dump(members, open("member.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)

    return {
        "success": True,
        "message": f"{caught_fish['name']}을(를) 잡았습니다! (성공 확률 {round(catch_chance*100,1)}%, 사용한 미끼: {bait_name})",
        "fish": caught_fish,
        "remaining_bait": player["bait_inventory"],
        "Fish_cnt": player["Fish_cnt"],
        "Fish_list": player["Fish_list"]
    }
