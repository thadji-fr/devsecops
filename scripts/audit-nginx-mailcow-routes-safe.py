#!/usr/bin/env python3
"""Passive audit of Nginx Stream -> Postfix port numbers.

No raw Nginx configuration, names, IPs, counts or errors are printed. This
checks only the declared upstream PORTS, not Docker NAT, WireGuard routing,
intermediate proxies, whether a service is listening, or actual connectivity.
"""
from __future__ import annotations

import re
import subprocess
import sys

HEADER = re.compile(r"(?m)^# configuration file ([^\n]+):[^\n]*\n")
PORT_MAP = ((25, 10025, "smtp"), (465, 10465, "smtps"), (587, 10587, "submission"))


def blocks(text: str, kind: str):
    pattern = (r"\bupstream\s+(?P<name>[A-Za-z_][\w-]*)\s*\{" if kind == "upstream"
               else r"\bserver\s*\{")
    for match in re.finditer(pattern, text):
        begin, pos, depth = match.end(), match.end(), 1
        while pos < len(text) and depth:
            depth += (text[pos] == "{") - (text[pos] == "}")
            pos += 1
        if depth == 0:
            yield match.groupdict().get("name"), text[begin:pos - 1]


def address_port(value: str):
    # Supports literal IPv4/IPv6/hostname:port, but never exposes the host.
    if "$" in value or not re.search(r":\d+$", value):
        return None
    return int(value.rsplit(":", 1)[1])


def inspect(config: str) -> dict[str, str]:
    markers = list(HEADER.finditer(config))
    pieces = []
    for idx, match in enumerate(markers):
        end = markers[idx + 1].start() if idx + 1 < len(markers) else len(config)
        filename = match.group(1)
        if "/stream-confs/" in filename:
            text = config[match.end():end]
            # We don't parse or output comments; strip them before matching.
            pieces.append(re.sub(r"(?m)#.*$", "", text))
    stream = "\n".join(pieces)
    upstreams = {}
    for name, body in blocks(stream, "upstream"):
        upstreams[name] = [address_port(endpoint) for endpoint in re.findall(
            r"\bserver\s+([^\s;]+)", body)]

    servers = [body for _, body in blocks(stream, "server")]
    result = {}
    for external, expected, label in PORT_MAP:
        listen = re.compile(r"\blisten\s+(?:[^;\s]*:)?" + str(external) + r"(?:\s|;)")
        matches = [block for block in servers if listen.search(block)]
        if len(matches) != 1:
            result[label + "_stream_block"] = "NON" if not matches else "INDÉTERMINÉ"
            result[label + "_proxy_protocol_outbound"] = "INDÉTERMINÉ"
            result[label + "_target_is_postfix_proxy_port"] = "INDÉTERMINÉ"
            continue
        body = matches[0]
        result[label + "_stream_block"] = "OUI"
        result[label + "_proxy_protocol_outbound"] = (
            "OUI" if re.search(r"\bproxy_protocol\s+on\s*;", body) else "NON"
        )
        direct = re.search(r"\bproxy_pass\s+([^\s;]+)\s*;", body)
        ports = []
        if direct:
            target = direct.group(1)
            if target in upstreams:
                ports = upstreams[target]
            else:
                ports = [address_port(target)]
        if not ports or None in ports:
            result[label + "_target_is_postfix_proxy_port"] = "INDÉTERMINÉ"
        else:
            result[label + "_target_is_postfix_proxy_port"] = (
                "OUI" if all(port == expected for port in ports) else "NON"
            )
    return result


def main() -> int:
    try:
        cmd = subprocess.run(["docker", "exec", "swag", "nginx", "-T"],
                             capture_output=True, text=True, timeout=45)
    except (OSError, subprocess.TimeoutExpired):
        print("audit_status: ERREUR")
        return 1
    if cmd.returncode != 0:
        print("audit_status: ERREUR")
        return 1
    print("audit_status: OK")
    for key, value in inspect(cmd.stdout).items():
        print(f"{key}: {value}")
    print("note: ports declared in Nginx only; not Docker mappings or reachability")
    return 0


if __name__ == "__main__":
    sys.exit(main())