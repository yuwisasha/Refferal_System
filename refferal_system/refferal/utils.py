import time
import random
import string

from django.utils.crypto import get_random_string


def send_sms_code(phone_number: str) -> int:
    code = get_random_string(4, string.digits)
    time.sleep(random.choice([1, 2]))
    return code
