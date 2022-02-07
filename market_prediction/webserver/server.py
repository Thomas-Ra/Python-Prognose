import http.server
import socketserver

PORT = 8080
DIRECTORY = "../finance/html"

class handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()