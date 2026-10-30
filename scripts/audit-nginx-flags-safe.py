#!/usr/bin/env python3
"""Audit Nginx read-only: output fixed feature names and booleans only.

Never prints raw nginx -T, paths, names, IPs, counts, certs, directive values
or stderr. Results are structural observations, not security guarantees.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

HEADER = re.compile(r"(?m)^# configuration file [^\n]+:\s*$")
PORT25 = re.compile(r"(?m)\blisten\s+(?:[^;\s]*:)?25(?:\s|;)")


def strip_comments(s: str) -> str:
    # nginx -T headers are parsed *before* stripping comments.
    return re.sub(r"(?m)#.*$", "", s)


def find_blocks(s: str, kind: str) -> list[str]:
    """Extract non-nested named blocks in a config fragment, without logging it."""
    out = []
    for match in re.finditer(r"\b" + re.escape(kind) + r"\s*\{", s):
        start = match.end()
        depth = 1
        pos = start
        while pos < len(s) and depth:
            if s[pos] == "{":
                depth += 1
            elif s[pos] == "}":
                depth -= 1
            pos += 1
        if depth == 0:
            out.append(s[start : pos - 1])
    return out


def inspect(config: str) -> dict[str, str]:
    sections = []
    markers = list(HEADER.finditer(config))
    for i, marker in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(config)
        header, _, body = config[marker.start() : end].partition("\n")
        sections.append((header, strip_comments(body)))
    if not sections:
        return {"config_sections_detected": "NON", "detail": "INDÉTERMINÉ"}

    all_text = "\n".join(body for _, body in sections)
    stream_files = [body for header, body in sections if "/stream-confs/" in header]
    stream_text = "\n".join(stream_files)
    smtp_blocks = [block for block in find_blocks(stream_text, "server") if PORT25.search(block)]
    outbound = re.compile(r"\bproxy_protocol\s+on\s*;")
    incoming = re.compile(r"\blisten\s+[^;]*\bproxy_protocol\b")
    http_text = "\n".join(body for header, body in sections if "/proxy-confs/" in header)
    proxy_values = re.findall(r"\bproxy_pass\s+([^;]+);", http_text)
    flags = {
        "config_sections_detected": "OUI",
        "stream_config_present": "OUI" if re.search(r"\bstream\s*\{", all_text) else "NON",
        "stream_file_present": "OUI" if stream_files else "NON",
        "http_proxy_pass_present": "OUI" if any(v.strip().startswith(("http://", "https://", "$")) for v in proxy_values) else "NON",
        "tcp_stream_present": "OUI" if re.search(r"\blisten\s+\d+\s*;", stream_text) else "NON",
        "udp_stream_present": "OUI" if re.search(r"\blisten\s+[^;]+\budp\b", stream_text) else "NON",
        "auth_request_declared": "OUI" if re.search(r"\bauth_request\s+", all_text) else "NON",
        "real_ip_header_declared": "OUI" if re.search(r"\breal_ip_header\s+", all_text) else "NON",
        "trusted_real_ip_sources_declared": "OUI" if re.search(r"\bset_real_ip_from\s+", all_text) else "NON",
        "crowdsec_reference_in_directives": "OUI" if re.search(r"crowdsec", all_text, re.I) else "NON",
        "stream_proxy_protocol_outbound": "OUI" if outbound.search(stream_text) else "NON",
        "stream_proxy_protocol_inbound": "OUI" if incoming.search(stream_text) else "NON",
        "smtp_stream_block_located": "OUI" if smtp_blocks else "NON",
        "smtp_proxy_protocol_outbound": (
            "INDÉTERMINÉ" if not smtp_blocks else
            "OUI" if any(outbound.search(block) for block in smtp_blocks) else "NON"
        ),
        "smtp_proxy_protocol_inbound": (
            "INDÉTERMINÉ" if not smtp_blocks else
            "OUI" if any(incoming.search(block) for block in smtp_blocks) else "NON"
        ),
    }
    return flags


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Nginx structurel, résultats uniquement OUI/NON/INDÉTERMINÉ")
    parser.add_argument("--container", default="swag", help="Identifiant local du conteneur, jamais affiché")
    args = parser.parse_args()
    try:
        command = subprocess.run(
            ["docker", "exec", args.container, "nginx", "-T"],
            capture_output=True, text=True, timeout=45, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        print("audit_status: ERREUR", "detail: COMMANDE_INDISPONIBLE", sep="\n")
        return 1
    if command.returncode != 0:
        print("audit_status: ERREUR", "detail: CONFIGURATION_NON_VALIDEE", sep="\n")
        return 1
    result = inspect(command.stdout)
    print("audit_status: OK")
    for key, value in result.items():
        print(f"{key}: {value}")
    print("note: indicateurs structurels; ni secrets ni configurations brutes affichés")
    return 0


if __name__ == "__main__":
    sys.exit(main())