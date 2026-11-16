"""
A small Telnet-style plaintext login emulator for localhost demonstrations.
This is NOT a full Telnet protocol implementation. It accepts USER and PASS
lines over TCP and is intentionally restricted to 127.0.0.1.
"""
import socketserver

HOST = "127.0.0.1"
PORT = 2323
LAB_USERNAME = "admin"
LAB_PASSWORD = "123456"

class LoginHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b"LOCAL IoT TELNET-STYLE LAB\r\n")
        self.wfile.write(b"Username:\r\n")
        username = self.rfile.readline(256).decode("utf-8", "ignore").strip()
        self.wfile.write(b"Password:\r\n")
        password = self.rfile.readline(256).decode("utf-8", "ignore").strip()
        try:
            if username == LAB_USERNAME and password == LAB_PASSWORD:
                self.wfile.write(b"LOGIN_SUCCESS\r\n")
            else:
                self.wfile.write(b"LOGIN_FAILED\r\n")
        except OSError:
            pass

class LocalTelnetServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def start_server():
    server = LocalTelnetServer((HOST, PORT), LoginHandler)
    server.serve_forever()

if __name__ == "__main__":
    print(f"Telnet-style lab emulator listening on {HOST}:{PORT}")
    start_server()
