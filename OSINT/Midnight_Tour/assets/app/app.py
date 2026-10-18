#!/usr/bin/env python3
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

PASSWORD, FLAG = 'sleepy_hollow_11', 'flame{s33_y0u_at_m1dn1ght}'


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):  # the gate: only server-side check so the flag never ships to the browser
        form = parse_qs(self.rfile.read(int(self.headers.get('Content-Length', 0))).decode())
        reply = (FLAG if form.get('password', [''])[0].strip().lower() == PASSWORD else 'The gate stays shut.').encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)


ThreadingHTTPServer(('', 8000), partial(Handler, directory=str(Path(__file__).parent / 'site'))).serve_forever()
