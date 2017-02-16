from werkzeug.security import generate_password_hash, \
    check_password_hash
import os
import string
import random
import hashlib
import uuid

string_full = string.ascii_uppercase + string.digits


def generate_random_string(size=6):
    return ''.join(random.choice(string_full) for _ in range(size))


def hash_password(password, salt):
    return str(generate_password_hash(password + salt))
