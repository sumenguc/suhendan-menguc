# -*- coding: utf-8 -*-
"""
İçerik seçim galerisi için yerel sunucu.

Sıradan `python -m http.server`'dan farkı: `POST /save-selection` isteğini
karşılayıp gövdeyi `_secim/secim_sonuc.json` dosyasına yazar. Böylece sayfadaki
"Seçimleri Kaydet" düğmesi doğrudan bu dosyayı üretir; indirilenler klasörü
aramaya gerek kalmaz.

Kullanım:  python select_server.py
Sonra:     http://127.0.0.1:8765/_secim/ adresini tarayıcıda aç.
"""

import http.server
import io
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8765
OUT_PATH = os.path.join(ROOT, "_secim", "secim_sonuc.json")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        # Varsayılan gürültülü stderr logunu sadeleştir.
        print("[%s] %s" % (self.address_string(), fmt % args))

    def do_POST(self):
        if self.path != "/save-selection":
            self.send_error(404, "Not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode("utf-8"))
            return

        out_dir = os.path.dirname(OUT_PATH)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        with io.open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Kaydedildi: %s (%d oge)" % (OUT_PATH, data.get("count", 0)))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))


if __name__ == "__main__":
    # ThreadingHTTPServer, bu ortamda eşzamanlı bağlantılarda ERR_CONNECTION_RESET
    # üretti (muhtemelen Windows/AV etkileşimi). Tek iş parçacıklı sürüm, daha önce
    # düz http.server ile kanıtlanmış olan kararlı davranışı korur.
    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print("Sunucu calisiyor: http://127.0.0.1:%d/_secim/" % PORT)
    print("Kayit dosyasi:", OUT_PATH)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
