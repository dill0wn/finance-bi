import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from flask import Flask, jsonify

from ronin.utils.logging import getLogger

HC_PORT = int(os.environ.get("HEALTHCHECK_PORT"))

log = getLogger('ronin.model.healthcheck')

class HealthcheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthcheck':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'OK'}).encode())
        else:
            self.send_response(404)

    @classmethod
    def run(cls, server_class=HTTPServer):
        handler_class = cls
        server_address = ('', HC_PORT)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()
        log.info(f"Healthcheck server running on port {HC_PORT}")


def create_app():
    flapp = Flask(__name__)

    @flapp.route('/healthcheck', methods=['GET'])
    def healthcheck():
        return jsonify({'status': 'OK'}), 200
    
    return flapp

# if __name__ == '__main__':
#     flapp.run(port=HC_PORT, debug=True)