import json

def transfer_asset(sender_id, receiver_id, asset_type, amount, fish_id=None):

    with open("member.json", "r", encoding="utf-8") as f:
        members = json.load(f)

    sender = members.get(sender_id)
    receiver = members.get(receiver_id)

    if not sender or not receiver:
        return {"success": False, "message": "보내는 사람 또는 받는 사람을 찾을 수 없습니다."}

    if sender_id == receiver_id:
        return {"success": False, "message": "자기 자신에게는 보낼 수 없습니다."}

    if asset_type == "money":
        if sender["money"] < amount:
            return {"success": False, "message": "보유 금액이 부족합니다."}

        sender["money"] -= amount
        receiver["money"] += amount

        message = f"{receiver['nickname']}에게 {amount}원을 보냈습니다."

    elif asset_type == "fish":
        if fish_id is None:
            return {"success": False, "message": "물고기 전송 시 fish_id가 필요합니다."}

        fish_index = int(fish_id) - 1
        sender_fish = sender["Fish_cnt"][fish_index]

        if sender_fish < amount:
            return {"success": False, "message": "보유 물고기 수가 부족합니다."}

        sender["Fish_cnt"][fish_index] -= amount
        receiver["Fish_cnt"][fish_index] += amount

        message = f"{receiver['nickname']}에게 {fish_id}번 물고기 {amount}마리를 보냈습니다."

    else:
        return {"success": False, "message": "지원하지 않는 자산 유형입니다."}

    members[sender_id] = sender
    members[receiver_id] = receiver

    with open("member.json", "w", encoding="utf-8") as f:
        json.dump(members, f, ensure_ascii=False, indent=4)

    return {
        "success": True,
        "message": message,
        "sender": {
            "player_id": sender_id,
            "money": sender["money"],
            "Fish_cnt": sender["Fish_cnt"]
        },
        "receiver": {
            "player_id": receiver_id,
            "money": receiver["money"],
            "Fish_cnt": receiver["Fish_cnt"]
        }
    }
