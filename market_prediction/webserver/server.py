import http.server
import socketserver
import threading

PORT = 8080
DIRECTORY = "./market_prediction/finance/displayResults"

class handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start():
    serverhandler = handler
    with socketserver.TCPServer(("", PORT), serverhandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def start_in_thread():
    daemon = threading.Thread(name='daemon_server',
                          target=start)
    daemon.setDaemon(True)
    daemon.start()