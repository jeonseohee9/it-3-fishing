from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

import funtion.account as account
import funtion.unlock as unlock
import funtion.rod as rod
import funtion.fishing as fishing
import funtion.bait as bait
import funtion.fishSell as fishSell
import funtion.inventory as inventory
import funtion.encyclopedia_all as encyclopedia_all
import funtion.encyclopedia_single as encyclopedia_single
import funtion.trap as trap


class FishingHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        """JSON 응답 헬퍼"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def _get_body(self):
        """요청 body 파싱"""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        return json.loads(self.rfile.read(content_length).decode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._get_body()

        # 회원가입
        if path == "/signup":
            result = account.signup(body)
            self._send_json(result)

        # 로그인
        elif path == "/login":
            result = account.login(body)
            self._send_json(result)

        # 낚싯대 강화
        elif path == "/rod/upgrade":
            player_id = body.get("player_id")
            result = rod.upgrade_rod_level1to5(player_id)
            self._send_json(result)

        # 낚시 시도
        elif path == "/fishing":
            player_id = body.get("player_id")
            bait_id = body.get("bait_id")
            result = fishing.attempt_fishing(player_id, bait_id)
            self._send_json(result)

        # 미끼 구매
        elif path == "/bait/buy":
            player_id = body.get("player_id")
            bait_id = body.get("bait_id")
            quantity = body.get("quantity", 1)
            result = bait.buy_bait(player_id, bait_id, quantity)
            self._send_json(result)

        # 물고기 판매
        elif path == "/fish/sell":
            player_id = body.get("player_id")
            fish_id = body.get("fish_id")
            quantity = body.get("quantity", 1)  
            result = fishSell.sell_fish(player_id, fish_id, quantity)
            self._send_json(result)

        # 인벤토리 조회
        elif path == "/inventory":
            player_id = body.get("player_id")
            result = inventory.get_inventory(player_id)
            self._send_json(result)

        # 낚시터 해금
        elif path == "/unlock":
            player_id = body.get("player_id")
            result = unlock.unlock(player_id)
            self._send_json(result)

        # 도감 전체 조회
        elif path == "/encyclopedia":
            player_id = body.get("player_id")
            result = encyclopedia_all.get_player_fish_data(player_id)
            self._send_json(result)

        # 도감 개별 조회
        elif path == "/encyclopedia/fish":
            player_id = body.get("player_id")
            fish_id = body.get("fish_id")
            result = encyclopedia_single.get_fish_info(player_id, fish_id)
            self._send_json(result)


        else:
            self._send_json({"error": "Invalid API endpoint"}, status=404)


def run():
    server = HTTPServer(("", 8000), FishingHandler)
    print("서버 시작!")
    server.serve_forever()


if __name__ == "__main__":
    run()
