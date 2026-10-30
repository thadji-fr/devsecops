#!/usr/bin/env python3
"""Contrôles statiques des modèles techniques publics, sans Docker ni secrets."""
from pathlib import Path
import re
import yaml

root = Path(__file__).resolve().parents[1]
base = root / "examples"

def read(name):
    return yaml.safe_load((base / "compose" / name).read_text(encoding="utf-8"))

edge, crowd, guac, arcane = [read(name) for name in (
    "edge.compose.yaml", "crowdsec.compose.yaml", "guacamole.compose.yaml", "arcane.compose.yaml")]
assert set(edge["services"]) == {"swag"}
assert set(crowd["services"]) == {"crowdsec", "crowdsec-web-ui"}
assert set(guac["services"]) == {"guacamole", "guacamole_db", "guacd"}
assert set(arcane["services"]) == {"arcane"}
for data in (edge, crowd, guac, arcane):
    assert data["networks"]["edge"]["name"] == "example-edge"
    assert data["networks"]["edge"]["external"] is True
    assert all("edge" in service["networks"] for service in data["services"].values())

mounts = lambda service: {v["target"]: v for v in service["volumes"]}
swag_config = mounts(edge["services"]["swag"])["/config"]["source"]
crowd_logs = mounts(crowd["services"]["crowdsec"])["/var/log/nginx"]
assert crowd_logs["read_only"] is True
assert crowd_logs["source"] == swag_config + "/log/nginx", "Log source Nginx != CrowdSec"
assert mounts(crowd["services"]["crowdsec"])["/etc/crowdsec"]
assert mounts(crowd["services"]["crowdsec"])["/var/lib/crowdsec/data"]
assert mounts(guac["services"]["guacamole"])["/var/lib/guacamole/recordings"]["read_only"]
assert mounts(guac["services"]["guacd"])["/var/lib/guacamole/recordings"]["source"] == mounts(guac["services"]["guacamole"])["/var/lib/guacamole/recordings"]["source"]
assert mounts(arcane["services"]["arcane"])["/var/run/docker.sock"]["source"] == "/var/run/docker.sock"

for s in ("crowdsec", "crowdsec-web-ui"):
    assert crowd["services"][s]["ports"][0]["host_ip"].startswith("${WG_BIND_IP")
assert arcane["services"]["arcane"]["ports"][0]["host_ip"].startswith("${WG_BIND_IP")
for s in guac["services"].values():
    assert all(port.startswith("127.0.0.1:") for port in s["ports"])

# Conteneur:port/proto et listen de Nginx Stream doivent correspondre.
nginx_stream = "\n".join(p.read_text(encoding="utf-8") for p in (base/"nginx"/"stream-confs").glob("*.conf"))
listen = {(int(port), "udp" if proto else "tcp") for port, proto in re.findall(r"\blisten\s+(\d+)(\s+udp)?\s*;", nginx_stream)}
published = {(int(p.split(":")[-1].split("/")[0]),p.split("/")[-1]) for p in edge["services"]["swag"]["ports"] if p.rsplit("/", 1)[-1] in ("tcp", "udp")}
assert listen == published - {(80,"tcp"),(443,"tcp")}, (listen,published)
assert (9987,"udp") in listen and (30033,"tcp") in listen
assert "stream {" in (base/"nginx"/"stream.conf").read_text()

# Le relevé sur le VPS a confirmé PROXY protocol émis par Nginx sur
# l'upstream SMTP ; il n'est PAS attendu du client entrant. On exige cette
# directive dans l'exemple sans l'activer par erreur sur les autres relais.
mail_stream = (base / "nginx" / "stream-confs" / "mail-relay.conf").read_text(encoding="utf-8")
blocks = re.findall(r"\bserver\s*\{[^{}]*\}", mail_stream)
smtp = [b for b in blocks if re.search(r"\blisten\s+25\s*;", b)]
assert len(smtp) == 1, "SMTP stream block missing or duplicated"
assert re.search(r"\bproxy_protocol\s+on\s*;", smtp[0]), "SMTP must emit PROXY protocol"
assert not re.search(r"\blisten\s+25\s+proxy_protocol\b", smtp[0]), "SMTP must not expect incoming PROXY protocol"
assert not any(re.search(r"\bproxy_protocol\s+on\s*;", b) for b in blocks if b not in smtp), "PROXY protocol not verified on other mail streams"
print("OK : réseau externe, bind mounts, WireGuard/localhost, montages Nginx/CrowdSec, ports HTTP/Stream")
