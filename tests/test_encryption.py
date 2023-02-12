import pytest
import ms_ovba_crypto
import unittest.mock


encryption_data = [
    # ([0x41], b'0xFF', b'\x41\x43\x5A\x5A\x5E\x5A\x5E\x5A\x5E\x5A\x5E'),
    ([0xBC, 0x7B, 0x7B], b'\x00', b'\xBC\xBE\xA7\xA2\x59\x1C\x5A\x1C\x5A\x1C'),
    (
        [0x37, 0x7B, 0x7B, 0x7B],
        b'\xFF',
        b'\x37\x35\x2C\x2B\xDC\xDD\x56\xDE\x56\xDE\xA9'
    ),
]


class NotSoRandom():
    _rand = []
    @classmethod
    def set_seed(cls, seeds):
        cls._rand = seeds

    @classmethod
    def randint(cls):
        return cls._rand.pop(0)


@unittest.mock.patch('random.randint', NotSoRandom.randint())
@pytest.mark.parametrize("rand, data, expected", encryption_data)
def test_encryption(rand, data, expected):
    clsid = '{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'
    NotSoRandom.set_seed(rand)
    assert ms_ovba_crypto.encrypt(clsid, data) == expected
