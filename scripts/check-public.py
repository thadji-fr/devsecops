#!/usr/bin/env python3
"""Heuristic pre-publication checks. No guarantee; review files and screenshots manually."""
from pathlib import Path
import ipaddress
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC_NETS = tuple(map(ipaddress.ip_network, (
    '192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24'
)))
ALLOW_IP = {'0.0.0.0', '127.0.0.1', '255.255.255.255'}
EXTS = {'.md', '.yaml', '.yml', '.conf', '.py', '.example', '.sh', '.json', '.txt'}
IPV4 = re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])')
PRIVATE_KEY = re.compile(r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----')
SUSPECT = re.compile(r'(?i)(?:vps-[0-9a-f]{7,}|root@vps|\.internal\b|\b10\.50\.|(?:api[_-]?key|token|password)[ \t]*[:=][ \t]*["\']?[A-Za-z0-9_./+!=-]{16,})')
violations = []

for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix not in EXTS or '.git' in path.parts:
        continue
    try:
        txt = path.read_text(encoding='utf-8')
    except (UnicodeError, OSError):
        violations.append((path, 'fichier illisible'))
        continue
    for m in IPV4.finditer(txt):
        try:
            ip = ipaddress.ip_address(m.group())
        except ValueError:
            continue
        if str(ip) not in ALLOW_IP and not any(ip in n for n in DOC_NETS):
            violations.append((path, 'adresse IPv4 à examiner'))
    if PRIVATE_KEY.search(txt):
        violations.append((path, 'clé privée potentielle'))
    if SUSPECT.search(txt) and path.name != 'check-public.py':
        violations.append((path, 'motif de secret ou hôte à vérifier'))

if violations:
    for path, reason in sorted(set(violations)):
        print(f'À EXAMINER: {path.relative_to(ROOT)} — {reason}')
    sys.exit(1)
print('Contrôle heuristique OK. Relecture humaine, des images et de l’historique toujours indispensable.')
