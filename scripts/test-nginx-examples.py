#!/usr/bin/env python3
"""Vérifie les exemples Nginx publics dans un répertoire temporaire.

N'utilise ni les hôtes privés ni les fichiers de configuration en production.
Les includes TLS/Authentik sont DES DOUBLURES de test, pas des protections.
`--smoke` effectue des requêtes HTTP(S), TCP et UDP entre sockets localhost.
"""
import argparse
import http.client
import os
from pathlib import Path
import re
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "examples" / "nginx"
HTTP_FILES = ("http.conf", "remote-wireguard.subdomain.conf", "arcane-authentik.subdomain.conf")
STREAM_FILES = ("mail-relay.conf", "voice-relay.conf")


def cmd(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, timeout=30, **kwargs)


def load_stream():
    details = cmd(["nginx", "-V"])
    opts = details.stdout + details.stderr
    if "--with-stream=dynamic" in opts:
        module = Path("/usr/lib/nginx/modules/ngx_stream_module.so")
        if not module.is_file():
            raise RuntimeError("Module Stream absent : installer libnginx-mod-stream pour valider TCP/UDP.")
        return f"load_module {module};\n"
    if "--with-stream" not in opts:
        raise RuntimeError("Nginx a été compilé sans ngx_stream_module.")
    return ""


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def prepare(work, smoke, http_only):
    nginx = work / "nginx"
    proxy_dir = nginx / "proxy-confs"
    stream_dir = nginx / "stream-confs"
    proxy_dir.mkdir(parents=True)
    stream_dir.mkdir(parents=True)

    cert = nginx / "test.crt"
    key = nginx / "test.key"
    generated = cmd([
        "openssl", "req", "-x509", "-nodes", "-newkey", "rsa:2048",
        "-subj", "/CN=example.org", "-days", "1",
        "-keyout", str(key), "-out", str(cert),
    ])
    if generated.returncode:
        raise RuntimeError("Génération des certificats éphémères impossible")

    # Doublures indispensables au parseur Nginx. Elles ne reproduisent PAS
    # les protections TLS, Authentik ni les en-têtes de production.
    write(nginx / "ssl.conf", f"ssl_certificate {cert};\nssl_certificate_key {key};\n")
    write(nginx / "proxy.conf", "proxy_http_version 1.1;\nproxy_set_header Host $host;\n")
    write(nginx / "resolver.conf", "resolver 127.0.0.1 valid=10s;\n")
    write(nginx / "authentik-server.conf", "location = /outpost.goauthentik.io/auth/nginx { internal; return 204; }\n")
    write(nginx / "authentik-location.conf", "auth_request /outpost.goauthentik.io/auth/nginx;\n")

    for filename in HTTP_FILES:
        original = (SAMPLES / filename).read_text(encoding="utf-8")
        staged = original.replace("/config/nginx/", f"{nginx}/")
        if smoke:
            # On teste les VRAIS fragments avec des substitutions temporaires
            # vers des backends 127.0.0.1, sans publier ni contacter de VPN.
            staged = staged.replace("listen 443 ssl;", "listen 127.0.0.1:18443 ssl;")
            staged = staged.replace("listen [::]:443 ssl;", "")
            staged = staged.replace("set $upstream_app uptime-kuma;", "set $upstream_app 127.0.0.1;")
            staged = staged.replace("set $upstream_port 3001;", "set $upstream_port 19001;")
            staged = staged.replace("set $upstream_app arcane;", "set $upstream_app 127.0.0.1;")
            staged = staged.replace("set $upstream_port 3552;", "set $upstream_port 19002;")
            staged = staged.replace("192.0.2.10:8080", "127.0.0.1:19003")
        write(proxy_dir / filename, staged)

    if not http_only:
        for filename in STREAM_FILES:
            original = (SAMPLES / "stream-confs" / filename).read_text(encoding="utf-8")
            if smoke:
                # Toutes les écoutes passent sur loopback en ports élevés.
                # Les upstreams passent aussi sur loopback, en ports distincts.
                original = re.sub(
                    r"\blisten\s+(\d+)(\s+udp)?\s*;",
                    lambda m: f"listen 127.0.0.1:{20000 + int(m[1])}{m[2] or ''};",
                    original,
                )
                original = re.sub(
                    r"192\.0\.2\.10:(\d+)",
                    lambda m: f"127.0.0.1:{21000 + int(m[1])}",
                    original,
                )
            write(stream_dir / filename, original)
        block = (SAMPLES / "stream.conf").read_text(encoding="utf-8")
        block = block.replace("/config/nginx/stream-confs/*.conf", f"{stream_dir}/*.conf")
        write(nginx / "stream.conf", block)

    conf = work / "nginx.conf"
    prefix = load_stream() if not http_only else ""
    write(conf, (
        prefix + "worker_processes 1;\n" +
        f"pid {work}/nginx.pid;\nerror_log {work}/error.log notice;\n" +
        "events { worker_connections 128; }\n" +
        f"http {{ access_log off; include {proxy_dir}/*.conf; }}\n" +
        (f"include {nginx}/stream.conf;\n" if not http_only else "")
    ))
    return conf


class HTTPBackend(BaseHTTPRequestHandler):
    def do_GET(self):
        body = self.server.response_body
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        return


def tcp_echo(stop):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", 21025))
        srv.listen(4)
        srv.settimeout(0.2)
        while not stop.is_set():
            try:
                peer, _ = srv.accept()
            except socket.timeout:
                continue
            with peer:
                peer.settimeout(2)
                peer.sendall(peer.recv(128))


def udp_echo(stop):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
        srv.bind(("127.0.0.1", 30987))
        srv.settimeout(0.2)
        while not stop.is_set():
            try:
                packet, peer = srv.recvfrom(512)
            except socket.timeout:
                continue
            srv.sendto(packet, peer)


def smoke_test(work, config):
    servers = []
    stop = threading.Event()
    nginx = None
    try:
        for port, response in ((19001, b"local-docker"), (19002, b"arcane-fixture"), (19003, b"remote-wireguard")):
            server = ThreadingHTTPServer(("127.0.0.1", port), HTTPBackend)
            server.response_body = response
            threading.Thread(target=server.serve_forever, daemon=True).start()
            servers.append(server)

        for target in (tcp_echo, udp_echo):
            thread = threading.Thread(target=target, args=(stop,), daemon=True)
            thread.start()
        time.sleep(0.2)
        nginx = subprocess.Popen(
            ["nginx", "-p", str(work), "-c", str(config), "-g", "daemon off;"],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        )
        for _ in range(50):
            if nginx.poll() is not None:
                raise RuntimeError("Démarrage du Nginx de test impossible")
            try:
                with socket.create_connection(("127.0.0.1", 18443), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.1)
        else:
            raise RuntimeError("Le Nginx de test n'écoute pas sur localhost")

        ctx = ssl._create_unverified_context()  # Certificat autosigné du TEST uniquement.
        for name, expected in (("monitoring.example.org", b"local-docker"),
                               ("remote-app.example.org", b"remote-wireguard")):
            conn = http.client.HTTPSConnection("127.0.0.1", 18443, timeout=4, context=ctx)
            try:
                conn.request("GET", "/", headers={"Host": name})
                response = conn.getresponse()
                body = response.read()
                assert response.status == 200 and body == expected, (name, response.status, body)
            finally:
                conn.close()
            print("OK : HTTP(S) proxy de laboratoire →", name)

        payload = b"demo-tcp"
        with socket.create_connection(("127.0.0.1", 20025), timeout=4) as s:
            s.settimeout(4)
            s.sendall(payload)
            assert s.recv(256) == payload
        print("OK : Stream TCP de laboratoire → backend simulé")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(4)
            s.sendto(b"demo-udp", ("127.0.0.1", 29987))
            assert s.recv(256) == b"demo-udp"
        print("OK : Stream UDP de laboratoire → backend simulé")
    finally:
        if nginx is not None:
            nginx.terminate()
            try:
                nginx.communicate(timeout=4)
            except subprocess.TimeoutExpired:
                nginx.kill()
                nginx.communicate()
        stop.set()
        for server in servers:
            server.shutdown()
            server.server_close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--smoke", action="store_true", help="Tester HTTP(S), TCP et UDP sur localhost après nginx -t")
    p.add_argument("--http-only", action="store_true", help="Validation syntaxique HTTP seule si Stream n'est pas installé")
    args = p.parse_args()
    if args.smoke and args.http_only:
        p.error("--smoke nécessite le module Stream")
    if not shutil.which("nginx") or not shutil.which("openssl"):
        p.error("nginx et openssl doivent être installés sur le poste de test")
    try:
        with tempfile.TemporaryDirectory(prefix="nginx-public-lab-") as directory:
            work = Path(directory)
            conf = prepare(work, args.smoke, args.http_only)
            result = cmd(["nginx", "-p", str(work), "-c", str(conf), "-t"])
            if result.returncode:
                print(result.stderr, file=sys.stderr)
                raise RuntimeError("nginx -t a échoué (fragments publics)")
            print("OK : nginx -t sur les fragments publics en environnement temporaire")
            if args.smoke:
                smoke_test(work, conf)
    except (OSError, RuntimeError, AssertionError, subprocess.TimeoutExpired) as e:
        print("ÉCHEC :", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()