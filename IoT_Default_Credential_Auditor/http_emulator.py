"""
Local HTTP Basic Authentication emulator.
Uses only the Python standard library and binds exclusively to localhost.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import base64
import hmac

HOST = "127.0.0.1"
PORT = 8000
LAB_USERNAME = "admin"
LAB_PASSWORD = "admin"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        expected = "Basic " + base64.b64encode(
            f"{LAB_USERNAME}:{LAB_PASSWORD}".encode()
        ).decode()
        supplied = self.headers.get("Authorization", "")
        if hmac.compare_digest(supplied, expected):
            body = b'{"status":"LOGIN_SUCCESS","service":"local-http-lab"}'
            self.send_response(200)
        else:
            body = b'{"status":"LOGIN_FAILED","service":"local-http-lab"}'
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="IoT Local Lab"')
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

def start_server():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"HTTP Basic Auth lab emulator listening on http://{HOST}:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
