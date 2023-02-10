import hashlib


def hash_password(password, key):
    bytes_to_hash = password + key
    return sha1(bytes_to_hash)


def validate_password(password, key, hash):
    return hash_password(password, key) == hash


def encrypt():
    pass


def decrypt():
    pass


def encode_nulls(data):
    """
    Replace null bytes in data with 0x01.
    The grbit variable indicates which bytes were replaced.
    """
    return grbit, data_no_nulls

def decode_nulls(grbit, data_no_nulls):
    """
    Restore null values in the data using grbit.
    """
    return data
