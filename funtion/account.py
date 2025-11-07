# 받아온 Body에서 userId, userPW를 전달받기
from json_util.json_io import dict_to_json_file, file_open, json_file_to_dict


def signup(dict_data):

    userId = dict_data['userId']
    pw = dict_data['password']

    userData = json_file_to_dict()
    print('before:', userData)
    if userId not in userData :
        userData[userId] = {
            "pw": pw,
            "userId": userId,
            "day": 1,
            "stamina": 100, 
            "money": 500000,
            "work_count": 0, 
            "stock": {
                "NDVA": 150000, 
                "DSL": 300000
            }, 
            "player_shares": {
                "NDVA": 0, 
                "DSL": 0
            }, 
            "total_shares": {
                "NDVA": 1000000, 
                "DSL": 2000000
	        },
        }
        # 회원가입한 정보 userData.json에 업데이트
        # (함수 활용 & 함수 수정 필요)
        dict_to_json_file(userData)
        return { "success" : True}

    return { "success" : False}


def login(dict_data):

    userId = dict_data['userId']
    pw = dict_data['password']
    
    userData = json_file_to_dict()
    
    if userId in userData and userData[userId]["pw"] == pw:
        dict_to_json_file(userData)
        return { "success" : True, "data" : userData[userId]}
    else:
        return { "success" : False}
