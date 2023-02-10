from ms_ovba_crypto import MsOvbaCrypto


def test_project_visibility():
    enc_data = b'\x15\x17\xCA\xF1\xD6\xF9\xD7\xF9\xD7\x06'
    ms_ovba_crypto = MsOvbaCrypto()
    assert ms_ovba_crypto.decrypt(enc_data) == b'\xFF'
