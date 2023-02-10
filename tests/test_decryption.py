def test_project_visibility():
    enc_data = b'\x15\x17\xCA\xF1\xD6\xF9\xD7\xF9\xD7\x06'
    data = ms_ovba_crypt.decrypt(enc_data)
    assert data == b'\xFF'
