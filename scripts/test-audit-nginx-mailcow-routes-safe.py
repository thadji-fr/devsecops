#!/usr/bin/env python3
"""Only synthetic fixtures; tests never connect to the user's infrastructure."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("audit", Path(__file__).with_name("audit-nginx-mailcow-routes-safe.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

fixture = """# configuration file /config/nginx/nginx.conf:
stream { include /config/nginx/stream-confs/*.conf; }
# configuration file /config/nginx/stream-confs/mail-relay.conf:
# SECRET-ONLY-IN-FIXTURE
upstream mail_smtp { server 192.0.2.10:10025; }
upstream smtps { server 192.0.2.10:10465; }
server { listen 25; proxy_protocol on; proxy_pass mail_smtp; }
server { listen 465; proxy_protocol on; proxy_pass smtps; }
server { listen 587; proxy_pass 192.0.2.10:587; }
"""
result = module.inspect(fixture)
assert result['smtp_target_is_postfix_proxy_port'] == 'OUI'
assert result['smtp_proxy_protocol_outbound'] == 'OUI'
assert result['smtps_target_is_postfix_proxy_port'] == 'OUI'
assert result['submission_proxy_protocol_outbound'] == 'NON'
assert result['submission_target_is_postfix_proxy_port'] == 'NON'
assert '192.0.2.10' not in str(result)
assert 'SECRET-ONLY-IN-FIXTURE' not in str(result)
assert module.inspect(fixture.replace('192.0.2.10:10025', '192.0.2.10:25'))['smtp_target_is_postfix_proxy_port'] == 'NON'
assert module.inspect(fixture.replace('proxy_pass mail_smtp;', 'proxy_pass $smtp_backend;'))['smtp_target_is_postfix_proxy_port'] == 'INDÉTERMINÉ'
assert module.inspect(fixture.replace('server { listen 25; proxy_protocol on; proxy_pass mail_smtp; }', ''))['smtp_stream_block'] == 'NON'
assert module.inspect(fixture.replace('server { listen 25;', 'server { listen 0.0.0.0:25;'))['smtp_target_is_postfix_proxy_port'] == 'OUI'
print('OK: safe Nginx -> Mailcow port mapping test fixtures')