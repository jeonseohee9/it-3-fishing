import json
from pathlib import Path

MEMBER_FILE = "member.json"

def load_json():
    if not Path(MEMBER_FILE).exists():
        return {}
    with open(MEMBER_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(data):
    with open(MEMBER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def signup(data):
    player_id = data.get("player_id")
    password = data.get("password")
    if not player_id or not password:
        return {"success": False, "message": "ID와 비밀번호를 입력하세요."}

    members = load_json()
    if player_id in members:
        return {"success": False, "message": "이미 존재하는 사용자입니다."}

    members[player_id] = {
        "password": password,
        "nickname": data.get("nickname", "New Player"),
        "email": data.get("email", ""),
        "money": 5000,
        "level": 1,
        "rod_level": 1,
        "bait_inventory": {"1": 5},
        "unlocked_sites": [1],
        "Fish_cnt": [0] * 25,
        "Fish_list": [0] * 25
    }
    save_json(members)
    return {"success": True, "player_id": player_id, "message": "회원가입 성공"}

def login(data):
    player_id = data.get("player_id")
    password = data.get("password")
    members = load_json()

    player = members.get(player_id)
    if not player or player.get("password") != password:
        return {"success": False, "message": "로그인 실패"}

    return {"success": True, "player_id": player_id, "data": player}
