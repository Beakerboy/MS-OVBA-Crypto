import pytest
import ms_ovba_crypto


decryption_data = [
    (b'\x15\x17\xCA\xF1\xD6\xF9\xD7\xF9\xD7\x06', b'\xFF'),
    (b'\x41\x43\x5A\x5A\x5E\x5A\x5E\x5A\x5E\x5A\x5E', b'\x00\x00\x00\x00'),
    (b'\xBC\xBE\xA7\xA2\x59\x1C\x5A\x1C\x5A\x1C', b'\x00'),
    (b'\x37\x35\x2C\x2B\xDC\xDD\x56\xDE\x56\xDE\xA9', b'\xFF'),
]


@pytest.mark.parametrize("data, expected", decryption_data)
def test_project_visibility(data, expected):
    assert ms_ovba_crypto.decrypt(data) == expected


def test_version_exception() -> None:
    data = b'\x15\x16\xCA\xF1\xD6\xF9\xD7\xF9\xD7\x06'
    with pytest.raises(Exception):
        ms_ovba_crypto.decrypt(data)
