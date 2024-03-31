import datetime
import http.server
import os
import signal
import socket
import ssl
import sys

# A minimal HTTP/HTTPS server that echos datetime, hostname, request IP and request
# headers on every GET. Can serve HTTP or HTTPS. If environment variable IS_HTTPS is
# not set, then serves HTTPS. If env var _is_ set, then if "True", serves HTTPS else
# serves HTTP. If environment variable SERVER_PORT is set, serves on that port.
# Else serves on 80 or 443 based on HTTP or HTTPS. If HTTPS, expects a server cert
# at "/etc/certs/server.pem". Responds promptly to SIGTERM from the container
# runtime.

class SigHandler():
    httpd = None

    def __init__(self, httpd):
        self.httpd = httpd
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, signum, frame):
        print("Received shutdown signal - stopping")
        httpd.server_close()
        sys.exit(0)

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        resp_str = str(datetime.datetime.now())
        resp_str += " -- " + socket.gethostname()
        resp_str += " -- " + str(self.client_address[0]) + "\n"
        print(resp_str)
        for key in self.headers.keys():
            print("%s: %s" % (key, self.headers.get(key)))
        self.wfile.write(bytes(resp_str, "utf8"))

is_https = os.environ.get("IS_HTTPS", "True").lower() in ["true", "t", "y", "yes", "1"]
port = int(os.environ.get("SERVER_PORT", 443 if is_https else 80))
server_address = ("0.0.0.0", port)

print("Starting server with configuration: HTTPS: %s, Port: %s" % (is_https, port))
httpd = http.server.HTTPServer(server_address, MyHandler)

if is_https:
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile="/etc/certs/server.pem", ssl_version=ssl.PROTOCOL_TLS)

sig_handler = SigHandler(httpd)
httpd.serve_forever()
