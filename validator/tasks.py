from celery import shared_task
from .validators import is_valid_format, get_mx_records, check_spf, check_dmarc, check_dkim, smtp_check
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

MAX_WORKERS = 50

@shared_task
def validate_emails_task(emails):
    results = []
    start = time.time()

    def validate_one(email):
        item = {'email': email}
        fmt_ok, fmt_info = is_valid_format(email)
        item['format_valid'] = fmt_ok
        item['format_info'] = fmt_info
        if not fmt_ok:
            item.update({'mx': [], 'smtp': {'ok': False, 'reason': 'invalid_format'},
                         'spf': None, 'dmarc': None, 'dkim': None})
            return item
        domain = fmt_info.split('@')[-1]
        mx = get_mx_records(domain)
        item['mx'] = mx
        item['spf'] = check_spf(domain)
        item['dmarc'] = check_dmarc(domain)
        item['dkim'] = check_dkim(domain)
        item['smtp'] = smtp_check(email, mx)
        item['latency'] = time.time() - start
        return item

    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, max(2, len(emails)))) as exe:
        future_to_email = {exe.submit(validate_one, e): e for e in emails}
        for future in as_completed(future_to_email):
            try:
                res = future.result()
            except Exception as exc:
                res = {'email': future_to_email[future], 'error': str(exc)}
            results.append(res)

    return results
