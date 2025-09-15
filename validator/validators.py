import dns.resolver
import smtplib
import socket
from email_validator import validate_email, EmailNotValidError
import time

DNS_TIMEOUT = 5.0

def is_valid_format(email: str):
    try:
        r = validate_email(email)
        normalized = r['email']
        return True, normalized
    except EmailNotValidError as e:
        return False, str(e)

def get_mx_records(domain: str):
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=DNS_TIMEOUT)
        mx = sorted([(r.preference, str(r.exchange).rstrip('.')) for r in answers], key=lambda x: x[0])
        return [host for pref, host in mx]
    except Exception:
        return []

def check_spf(domain: str):
    try:
        answers = dns.resolver.resolve(domain, 'TXT', lifetime=DNS_TIMEOUT)
        for r in answers:
            txt = ''.join(r.strings) if hasattr(r, 'strings') else str(r)
            if 'v=spf1' in txt:
                return {'found': True, 'record': txt}
        return {'found': False, 'record': None}
    except Exception:
        return {'found': False, 'record': None}

def check_dmarc(domain: str):
    try:
        dname = f'_dmarc.{domain}'
        answers = dns.resolver.resolve(dname, 'TXT', lifetime=DNS_TIMEOUT)
        for r in answers:
            txt = ''.join(r.strings) if hasattr(r, 'strings') else str(r)
            if 'v=DMARC1' in txt.upper():
                return {'found': True, 'record': txt}
        return {'found': False, 'record': None}
    except Exception:
        return {'found': False, 'record': None}

def check_dkim(domain: str):
    selectors = ['default', 'selector1', 'google']
    found = []
    for sel in selectors:
        sub = f'{sel}._domainkey.{domain}'
        try:
            answers = dns.resolver.resolve(sub, 'TXT', lifetime=DNS_TIMEOUT)
            for r in answers:
                txt = ''.join(r.strings) if hasattr(r, 'strings') else str(r)
                if 'v=DKIM1' in txt.upper():
                    found.append({'selector': sel, 'record': txt})
        except Exception:
            continue
    return {'found': bool(found), 'records': found}

def smtp_check(email: str, mx_hosts: list, from_address='validator@example.com', timeout=8):
    if not mx_hosts:
        return {'ok': False, 'reason': 'no_mx'}
    last_error = None
    for mx in mx_hosts:
        try:
            server = smtplib.SMTP(timeout=timeout)
            server.connect(mx)
            server.helo(socket.gethostname())
            server.mail(from_address)
            code, message = server.rcpt(email)
            server.quit()
            if 200 <= code < 300:
                return {'ok': True, 'mx': mx, 'code': code, 'message': message.decode() if isinstance(message, bytes) else str(message)}
            else:
                return {'ok': False, 'mx': mx, 'code': code, 'message': message.decode() if isinstance(message, bytes) else str(message)}
        except Exception as e:
            last_error = str(e)
            continue
    return {'ok': False, 'reason': 'all_mx_failed', 'error': last_error}
