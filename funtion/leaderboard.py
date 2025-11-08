import json

def get_leaderboard(limit=10):
    try:
        with open("member.json", "r", encoding="utf-8") as f:
            members = json.load(f)
    except FileNotFoundError:
        return {"success": False, "message": "member.json 파일을 찾을 수 없습니다."}

    leaderboard = []

    for player_id, data in members.items():
        money = data.get("money", 0)
        rod_level = data.get("rod_level", 1)
        fish_cnt = data.get("Fish_cnt", [])
        total_fish = sum(fish_cnt) if isinstance(fish_cnt, list) else 0

        leaderboard.append({
            "player_id": player_id,
            "nickname": data.get("nickname", "Unknown"),
            "money": money,
            "rod_level": rod_level,
            "total_fish": total_fish
        })

    leaderboard.sort(key=lambda x: (x["money"], x["rod_level"], x["total_fish"]), reverse=True)

    top_players = leaderboard[:limit]

    for i, player in enumerate(top_players, start=1):
        player["rank"] = i

    return {
        "success": True,
        "total_players": len(leaderboard),
        "leaderboard": top_players
    }
