#!/usr/bin/env python3
"""Unit test: synthetic fixture, never an infrastructure capture."""
import importlib.util
from pathlib import Path

path = Path(__file__).with_name('audit-nginx-flags-safe.py')
spec = importlib.util.spec_from_file_location('safe_nginx', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

sample = '''# configuration file /config/nginx/nginx.conf:
http { include /config/nginx/proxy-confs/*.conf; }
stream { include /config/nginx/stream-confs/*.conf; }
# configuration file /config/nginx/proxy-confs/hidden.conf:
# ip 192.0.2.50 and secret FIXTURE-ONLY-MARKER
server { auth_request /auth; real_ip_header X-Forwarded-For; set_real_ip_from 192.0.2.0/24; proxy_pass http://app:1234; }
# configuration file /config/nginx/stream-confs/hidden.conf:
upstream hidden { server 192.0.2.10:25; }
server { listen 25; proxy_pass hidden; proxy_protocol on; }
server { listen 9987 udp; proxy_pass hidden; }
'''
flags = module.inspect(sample)
assert flags['smtp_proxy_protocol_outbound'] == 'OUI', flags
assert flags['http_proxy_pass_present'] == 'OUI', flags
assert flags['smtp_proxy_protocol_inbound'] == 'NON', flags
assert flags['udp_stream_present'] == 'OUI', flags
assert flags['trusted_real_ip_sources_declared'] == 'OUI', flags
assert flags['stream_file_present'] == 'OUI', flags
assert 'FIXTURE-ONLY-MARKER' not in str(flags)
assert '192.0.2.50' not in str(flags)
fixture2 = sample.replace('proxy_protocol on;', '')
assert module.inspect(fixture2)['smtp_proxy_protocol_outbound'] == 'NON'
assert module.inspect('# not a dump')['detail'] == 'INDÉTERMINÉ'
print('OK: Nginx safe flag parser unit tests')

assert module.inspect(sample.replace('proxy_protocol on;', 'listen 25 proxy_protocol;'))['stream_proxy_protocol_inbound'] == 'OUI'