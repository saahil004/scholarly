import random
import string

def generate_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 10))
    return otp               