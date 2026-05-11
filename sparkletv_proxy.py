#!/usr/bin/env python3
# ══════════════════════════════════════════════
#   SparkleTv Multi-Channel Proxy
#   Puerto: 9191
#   Uso:    python3 sparkletv_proxy.py
# ══════════════════════════════════════════════
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 9191

STREAMS = {
    "/stream/1": "https://pecdl1.streameasthd.net/espnpremium/tracks-v1a1/mono.m3u8?ip=179.37.214.240&token=028a66a0746296a2c180f9932797ef76771d8692-24-1778580446-1778526446",  # ESPN Premium
    "/stream/1778539290443": "https://o7a4799avkmu.15072669.net:8443/hls/muha9xp8lgyom64.m3u8?s=3tXcdN_5bZwZ5iQjCqGpFg&e=1778560708",  # TNT sports 
    "/stream/1778539302188": "https://doc1.streameasthd.net/dsports/tracks-v1a1/mono.m3u8?ip=179.37.214.240&token=afbb03612fcbfa46d3e2caad718b1c1c7d7cf708-28-1778583440-1778529440",  # DirecTV 
}

class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        if self.path == "/playlist.m3u8":
            lines = ["#EXTM3U"]
            for path in STREAMS:
                cid = path.split("/")[-1]
                lines.append(f"#EXTINF:-1,Canal {cid}")
                lines.append(f"http://localhost:{port}{path}")
            data = "\n".join(lines).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.apple.mpegurl")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
            return
        if self.path in STREAMS:
            try:
                req = urllib.request.Request(
                    STREAMS[self.path],
                    headers={"User-Agent": "SparkleTv/1.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = r.read()
                    ctype = r.headers.get("Content-Type","application/vnd.apple.mpegurl")
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode())
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        route = self.path.replace("/update/", "/stream/")
        if route in STREAMS:
            length = int(self.headers.get("Content-Length", 0))
            STREAMS[route] = self.rfile.read(length).decode().strip()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"URL actualizada")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    print(f"\n  Proxy corriendo en http://localhost:{port}")
    print(f"  Playlist -> http://localhost:{port}/playlist.m3u8\n")
    for path in STREAMS:
        print(f"  Canal: http://localhost:{port}{path}")
    print("\n  Actualizar token en caliente:")
    print("    curl -X POST http://localhost:9191/update/1 -d 'NUEVA_URL'")
    print("    curl -X POST http://localhost:9191/update/1778539290443 -d 'NUEVA_URL'")
    print("    curl -X POST http://localhost:9191/update/1778539302188 -d 'NUEVA_URL'")
    print()
    server.serve_forever()
📋 Copiar script
SPARKLETV PROXY  •  3