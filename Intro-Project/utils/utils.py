from werkzeug.security import generate_password_hash, \
    check_password_hash
import os
import string
import random
import hashlib
import uuid
import urllib

string_full = string.ascii_uppercase + string.digits

def create_gravatar(email,size = 64):
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d': 'wavatar', 's': str(size)})
    return gravatar_url


def generate_random_string(size=6):
    return ''.join(random.choice(string_full) for _ in range(size))


def hash_password(password, salt):
    return str(generate_password_hash(password + salt))


def check_password(hash_password, password, password_salt):
    return check_password_hash(hash_password, password + password_salt)


def hash_password_sha256(password, password_salt):
    return hashlib.sha256(password_salt.encode() + password.encode()).hexdigest()


def check_password_sha256(hashed_password, password, password_salt):
    return hashed_password == hashlib.sha256(password_salt.encode() + password.encode()).hexdigest()
