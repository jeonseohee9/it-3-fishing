import json
from pathlib import Path

def json_file_to_dict(filename="member.json"):
    """JSON 파일을 딕셔너리로 변환"""
    path = Path(filename)
    if not path.exists():
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def dict_to_json_file(data, filename="member.json"):
    """딕셔너리를 JSON 파일로 저장"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
