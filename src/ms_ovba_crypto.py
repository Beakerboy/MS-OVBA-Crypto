import hashlib
import os
import struct

def hash_password(password, key):
    bytes_to_hash = password + key
    return hashlib.sha1(bytes_to_hash)

def validate_password(password, key, hash):
    return hash_password(password, key) == hash

class MsOvbaCrypto():

    def encrypt(self, clsid, data, length):
        """
        Seed 1 byte
        clsid string "{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"
        data variable
        length 4 bytes (calculate from data?)
        """
        seed = MsOvbaCrypto._make_seed()

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
            temp_value = 0
            byte_enc = temp_value ^ (encrypted_byte_1 + encrypted_byte_2)
            ignored_enc += byte_enc
            encrypted_byte_2 = encrypted_byte_1
            encrypted_byte_1 = byte_enc
            unencrypted_byte_1 = temp_value

        data_length_enc = b''
        for i in range(4):
            # for each byte in length in little-Endian order
            byte = ((255 << (8 * (4 - i))) & length) >> (3 - i)
            byte_enc = byte ^ (encrypted_byte_1 + encrypted_byte_2)
            data_length_enc += byte_enc
            encrypted_byte_2 = encrypted_byte_1
            encrypted_byte_1 = byte_enc
            unencrypted_byte_1 = byte

        data_enc = b''
        for i in range(len(data)):
            data_byte = data[i]
            byte_enc = data_byte ^ (encrypted_byte_1 + encrypted_byte_2)
            data_enc += byte_enc
            encrypted_byte_2 = encrypted_byte_1
            encrypted_byte_1 = byte_enc
            unencrypted_byte_1 = data_byte

        output = struct.pack(
            "<CCC",
            seed,
            version_enc,
            proj_key_enc
        ) + ignored_enc + data_length_enc + data_enc
        return output

    def decrypt(self, data):
        """
        Decrypt bytes of data
        """
        seed = data[0]
        version_enc = data[1]
        version = version_enc ^ seed
        if version != 2:
            raise Exception("Improper version value.")
        proj_key_enc = data[2]
        proj_key = proj_key_enc ^ seed

        unencrypted_byte_1 = proj_key
        encrypted_byte_1 = proj_key_enc
        encrypted_byte_2 = version_enc

        ignored_length = (seed & 6) // 2
        for i in range(ignored_length):
            byte_enc = data[3 + i]
            byte = byte_enc ^ (encrypted_byte_1 + encrypted_byte_2)
            encrypted_byte_2 = encrypted_byte_1
            encrypted_byte_1 = byte_enc
            unencrypted_byte_1 = byte

    def encode_nulls(self, data):
        """
        Replace null bytes in data with 0x01.
        The grbit variable indicates which bytes were replaced.
        """
        # return grbit, data_no_nulls
        pass

    def decode_nulls(self, grbit, data_no_nulls):
        """
        Restore null values in the data using grbit.
        """
        data = b''
        return data

    @staticmethod
    def _make_seed():
        return os.urandom(1)
