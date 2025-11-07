import json_util.json_io as json_io

def work(id, workId):
    userData = json_io.json_file_to_dict()
    if workId == 1:
        if userData[id]["stamina"] >= 20:
            userData[id]["money"] += 50000
            userData[id]["stamina"] -= 20
            
            json_io.dict_to_json_file(userData)
            return {"success": True, 'data': userData[id]}
        else:
            return {"success": False}
    else:
        if userData[id]["stamina"] >= 30:
            userData[id]["money"] += 80000
            userData[id]["stamina"] -= 30
            
            json_io.dict_to_json_file(userData)
            return {"success": True, 'data': userData[id]}
        else:
            return {"success": False}

