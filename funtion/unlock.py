import json

def unlock(player_id):
    with open("member.json", "r", encoding="utf-8") as f:
        member = json.load(f)

    with open("fishing_sites.json", "r", encoding="utf-8") as f:
        fishing_sites = json.load(f)

    player = member.get(player_id)
    if not player:
        return {"success": False, "message": "플레이어가 존재하지 않습니다."}

    level = player.get("level", 0)
    unlocked = player.get("unlocked_sites", [])

    target_site_id = None
    for site_id, site in fishing_sites.items():
        if level == site.get("required_level"):
            target_site_id = int(site_id)
            break

    if target_site_id is None:
        return {"success": False, "message": f"레벨에 맞는 낚시터가 없습니다."}

    if target_site_id not in unlocked:
        unlocked.append(target_site_id)
        player["unlocked_sites"] = unlocked

        with open("member.json", "w", encoding="utf-8") as f:
            json.dump(member, f, ensure_ascii=False, indent=4)

        site = fishing_sites[str(target_site_id)]
        return {
            "success": True,
            "message": f"{site['name']}가 해금되었습니다!",
            "player_money": player.get("money", 0),
            "unlocked_site": {
                "site_id": target_site_id,
                "name": site["name"]
            }
        }
    else:
        site = fishing_sites[str(target_site_id)]
        return {"success": False, "message": f"아직 해금할 수 없습니다."}
