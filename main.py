from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from json_util.json_io import dict_to_json_data, json_data_to_dict
import funtion.account as account
import funtion.day as day
import funtion.stock as stock
import funtion.work as work


class WebRequestHandler(BaseHTTPRequestHandler):

    def make_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def divide_path(self) -> tuple:
        service_with_query_params = urlparse(self.path)
        servie_name = service_with_query_params.path
        query_params = service_with_query_params.query

        return servie_name, query_params

    # CORS 방지
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        self.make_header()
        service_name, _ = self.divide_path()
        print(service_name, _)
        print(type(service_name))
    
        json_data = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        body = json_data_to_dict(json_data)
        result = {}

        # 서비스에 따라, 적절한 메소드를 호출한다.
        if service_name == '/signup':
            result = account.signup(body)

        if service_name == '/login':
            result = account.login(body)

        if service_name == '/sleep':
            result = day.sleep(body["userId"])

        if service_name == '/change':
            result = stock.change_stock(body["userId"])

        if service_name == '/buy_stocks':
            result = stock.buy_stock(body["userId"], body["stockName"], body["count"])
            
        if service_name == '/sell_stocks':
            result = stock.sell_stock(body["userId"], body["stockName"], body["count"])
                  
        if service_name == '/work':
            result = work.work(body["userId"], body["workId"])

        if result:
            result_data = dict_to_json_data(result)
            self.wfile.write(result_data.encode('utf-8'))

server = HTTPServer(("0.0.0.0", 8081), WebRequestHandler)
server.serve_forever()