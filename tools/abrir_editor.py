#!/usr/bin/env python3
"""
abrir_editor.py: levanta un servidor local y abre el editor en el navegador.

Uso:
    python tools/abrir_editor.py

El editor funciona en tu compu: no se sube nada a ningún lado. Se sirve desde
http://localhost para que el navegador permita guardar directo en la carpeta del repo
(Chrome y Edge). Para cerrarlo, apretá Ctrl+C en esta terminal.

Si querés probar también el juego, entrá a http://localhost:PUERTO/ (sin /editor/).
"""

import functools
import http.server
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


class Manejador(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Sin caché: así ves siempre los cambios más recientes
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, formato, *args):  # silencia el log de cada pedido
        pass


def main() -> int:
    handler = functools.partial(Manejador, directory=str(RAIZ))
    for puerto in range(8000, 8011):
        try:
            servidor = socketserver.ThreadingTCPServer(("127.0.0.1", puerto), handler)
            break
        except OSError:
            continue
    else:
        print("No encontré un puerto libre entre 8000 y 8010.")
        return 1

    servidor.daemon_threads = True
    url = f"http://localhost:{puerto}/editor/"
    print(f"Editor andando en {url}")
    print("Cerralo con Ctrl+C cuando termines.")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nListo, hasta la próxima.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
