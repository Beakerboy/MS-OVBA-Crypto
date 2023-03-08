import random
import struct


def encrypt(clsid: string, data: bytes) -> bytes:
    """
    clsid string "{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"
    data variable
    """
    length = len(data)
    seed = random.randint(0, 255)

    version = 2
    version_enc = version ^ seed

    proj_key = 0
    # sum character bytes in clsid
    for i in range(38):
        proj_key += ord(clsid[i])
    proj_key = proj_key & 255
    proj_key_enc = proj_key ^ seed

    unencrypted_byte_1 = proj_key
    encrypted_byte_1 = proj_key_enc
    encrypted_byte_2 = version_enc

    ignored_length = (seed & 6) // 2
    ignored_enc = b''
    for i in range(ignored_length):
        # set temp to anything(?)
        temp_value = random.randint(0, 255)
        sum = (unencrypted_byte_1 + encrypted_byte_2) & 255
        byte_enc = temp_value ^ sum
        ignored_enc += byte_enc.to_bytes(1, "little")
        encrypted_byte_2 = encrypted_byte_1
        encrypted_byte_1 = byte_enc
        unencrypted_byte_1 = temp_value

    data_length_enc = b''
    length_bytes = length.to_bytes(4, "little")
    for i in range(4):
        byte = length_bytes[i]
        # for each byte in length in little-Endian order.
        byte_enc = byte ^ ((unencrypted_byte_1 + encrypted_byte_2) & 255)
        data_length_enc += byte_enc.to_bytes(1, "little")
        encrypted_byte_2 = encrypted_byte_1
        encrypted_byte_1 = byte_enc
        unencrypted_byte_1 = byte

    data_enc = b''
    for i in range(len(data)):
        data_byte = data[i]
        sum = (unencrypted_byte_1 + encrypted_byte_2) & 255
        byte_enc = data_byte ^ sum
        data_enc += byte_enc.to_bytes(1, "little")
        encrypted_byte_2 = encrypted_byte_1
        encrypted_byte_1 = byte_enc
        unencrypted_byte_1 = data_byte

    output = struct.pack(
        "<BBB",
        seed,
        version_enc,
        proj_key_enc
    ) + ignored_enc + data_length_enc + data_enc
    return output


def decrypt(data_enc: bytes) -> bytes:
    """
    Decrypt bytes of data
    """
    data_enc = bytearray(data_enc)
    seed = data_enc.pop(0)
    version_enc = data_enc.pop(0)
    version = version_enc ^ seed
    if version != 2:
        raise Exception("Improper version value.")
    proj_key_enc = data_enc.pop(0)
    proj_key = proj_key_enc ^ seed

    unencrypted_byte_1 = proj_key
    encrypted_byte_1 = proj_key_enc
    encrypted_byte_2 = version_enc

    ignored_length = (seed & 6) // 2
    ignored = b''
    for i in range(ignored_length):
        byte_enc = data_enc.pop(0)
        byte = byte_enc ^ ((unencrypted_byte_1 + encrypted_byte_2) & 255)
        ignored += byte.to_bytes(1, "little")
        encrypted_byte_2 = encrypted_byte_1
        encrypted_byte_1 = byte_enc
        unencrypted_byte_1 = byte

    byte_index = 0
    length = 0
    for i in range(4):
        byte_enc = data_enc.pop(0)
        byte = byte_enc ^ ((unencrypted_byte_1 + encrypted_byte_2) & 255)
        temp_value = 256 ** byte_index
        temp_value *= byte
        length += temp_value
        encrypted_byte_2 = encrypted_byte_1
        encrypted_byte_1 = byte_enc
        unencrypted_byte_1 = byte
        byte_index += 1
    data = b''
    for i in range(length):
        byte_enc = data_enc.pop(0)
        byte = byte_enc ^ ((unencrypted_byte_1 + encrypted_byte_2) & 255)
        data += byte.to_bytes(1, "little")
        encrypted_byte_2 = encrypted_byte_1
        encrypted_byte_1 = byte_enc
        unencrypted_byte_1 = byte
    return data
