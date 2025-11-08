import json

# def get_fish_info(player_id, fish_id):
#     members = json.load(open("member.json", "r", encoding="utf-8"))
#     fish_data = json.load(open("fish.json", "r", encoding="utf-8"))
#     player = members.get(player_id)
#     fish = fish_data.get(str(fish_id))
#     if not player or not fish:
#         return {"success": False, "message": "플레이어나 물고기 정보가 없습니다."}
#     count = player["Fish_cnt"][int(fish_id)]
#     return {"success": True, "fish": fish, "count": count}

import json 

def get_player_fish_info(player_id):

    members = json.load(open('member.json', 'r', encoding='utf-8'))
    fish_list = json.load(open('fish.json', 'r', encoding='utf-8'))

    # 2. 플레이어 찾기

    player=members.get(player_id)
    if not player:
        return {"success": False} 
    
    # 4. 도감
    encyclopedia = []  
    collected_count = 0  

    # 5. 모든 물고기 확인
    for fish_id, fish_data in fish_list.items():

        fish_id = int(fish_id)
        count = player["Fish_cnt"][fish_id - 1] if fish_id - 1 < len(player["Fish_cnt"]) else 0
        collected = count > 0
        if collected:
            collected_count+=1
        encyclopedia.append({        encyclopedia.append({
            "fish_id": fish_id,
            "name": fish_data["name"],
            "level": fish_data["level"],
            "price": fish_data["price"],
            "rate": fish_data["rate"],
            "collected": collected,
            "count": count
        })


        })

    # 6. 결과 정리
    result = {
        "success": True,
        "player_id": player_id,
        "encyclopedia": encyclopedia,  
        "total_fish_count": len(fish_list),  
        "collected_count": collected_count 
    }

    return result
