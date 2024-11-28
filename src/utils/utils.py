import string
import random

def generate_random_name(length=8):
    chrs = string.ascii_letters + string.digits
    alphnmr_id = ''.join(random.choice(chrs) for _ in range(length))
    return alphnmr_id