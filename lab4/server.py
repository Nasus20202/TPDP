#!/usr/bin/env python3
import http.server, urllib.request

PORT = 8080


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/routino/"):
            url = "https://ksg.eti.pg.gda.pl/routino/www/routino/" + self.path[9:]
            with urllib.request.urlopen(url) as r:
                body = r.read()
            self.send_response(200)
            self.send_header("Content-Type", r.headers["Content-Type"])
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(open("lab4.html", "rb").read())


print("Serving on port", PORT)
http.server.HTTPServer(("", PORT), Handler).serve_forever()
