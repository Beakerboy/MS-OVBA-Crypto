import hashlib


class MsOvbaCrypto():

    def hash_password(password, key):
        bytes_to_hash = password + key
        return sha1(bytes_to_hash)


    def validate_password(password, key, hash):
        return hash_password(password, key) == hash


    def encrypt(seed, clsid, data, length):
        """
        Seed 1 byte
        clsid ?
        data variable
        length 4 bytes (calculate from data?)
        """

        version = 2
        version_enc = version ^ seed

        proj_key = 0
        # add each character byte from clsid to proj_key
        # if clsid = 1234-56, do we add chr('1') + chr('2') + ... or
        # 0x12 + 0x34 + 0x56. Do we include the dashes?
        proj_key_enc = proj_key ^ seed

        unencrypted_byte_1 = proj_key
        encrypted_byte_1 = proj_key_enc
        encrypted_byte_2 = version_enc

        ignored_length = (seed & 6) / 2
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

    def decrypt(data):
        """
        Decrypt bytes of data
        """
        seed = data[0]
        version_enc
        version = version_enc ^ seed
        if version != 2:
            raise Exception("Improper version value.")
        proj_key_enc = data[2]
        proj_key = proj_key_enc ^ seed

        unencrypted_byte_1 = proj_key
        encrypted_byte_1 = proj_key_enc
        encrypted_byte_2 = version_enc

        ignored_length = (seed & 6) / 2

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
