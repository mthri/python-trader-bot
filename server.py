from http.server import BaseHTTPRequestHandler, HTTPServer
import json 

HOST = '127.0.0.1' # or localhost
PORT = 8080

RESTful_API = True

def sell(symbol: str, amount: float) -> None:
    # write your sell logic here
    print(f'sell {symbol}, amount: {amount}')

def buy(symbol: str, amount: float) -> None:
    # write your buy logic here
    print(f'buy {symbol}, amount: {amount}')


# a minimal http server
class TraderWebServer(BaseHTTPRequestHandler):
    def do_POST(self):
        global RESTful_API
        
        # set headers
        self.send_response(200)
        self.send_header('Content-type', 'json/application' if RESTful_API else 'text/html')
        self.end_headers()

        if RESTful_API:

            status = False
            message = None

            # check have body data
            content_len = self.headers.get('Content-Length')
            if content_len is not None:
                content_len = int(self.headers.get('Content-Length'))
                body = self.rfile.read(content_len)

                # with `body_dict_data` do anything you need!(process operation)
                
                body_dict_data = json.loads(body.decode())

                # when we want open buy posstion
                if body_dict_data['operation'] == 'buy':
                    status = True
                    message = 'successfully buy'
                    buy(
                        symbol=body_dict_data['symbol'],
                        amount=body_dict_data['amount']
                    )

                # when we want open sell posstion
                elif body_dict_data['operation'] == 'sell':
                    status = True
                    message = 'successfully sell'
                    sell(
                        symbol=body_dict_data['symbol'],
                        amount=body_dict_data['amount']
                    )

                else:
                    message = 'can\'t find operation'

            else:
                message = 'no have data'
            
            response = json.dumps({
                'status': status,
                'message': message
            })

            self.wfile.write(response.encode())
        else:
            # HOST:PORT/{operation}/{symbol}/{amount}
            path = self.path.split('/')

            operation = path[1]
            symbol = path[2]
            amount = float(path[3])

            if operation == 'buy':
                buy(symbol=symbol, amount=amount)
                self.wfile.write(b'successfully buy')
            elif operation == 'sell':
                sell(symbol=symbol, amount=amount)
                self.wfile.write(b'successfully sell')
            else:
                self.wfile.write(b'can\'t find operation')
        

if __name__ == "__main__":        
    webServer = HTTPServer((HOST, PORT), TraderWebServer)
    print(f"server started http://{HOST}:{PORT}")

    try:
        #HINT: also you can run this method via thread to avoid block program here
        webServer.serve_forever()
    # when press CTRL+C
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("server stopped.")