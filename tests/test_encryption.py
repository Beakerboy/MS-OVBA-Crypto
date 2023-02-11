from ms_ovba_crypto import MsOvbaCrypto

@pytest.mark.parametrize("rand, data, expected", encryption_data)
def test_encryption(rand, data, expected):

    clsid = '{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'

    class OverrideRand(MsOvbaCrypto):
        def set_rand(cls, rand):
            self._rand_list = rand
        @classmethod
        def _make_seed(cls):
            return self._rand_list.pop(0)

    ms_ovba_crypto = OverrideRand()
    ms_ovba_crypto.set_rand(rand)
    assert ms_ovba_crypto.encrypt(clsid, data) == expected
    # project.setProtectionState("41435A5A5E5A5E5A5E5A5E")
    # project.setPassword("BCBEA7A2591C5A1C5A1C")
    # project.setVisibilityState("37352C2BDCDD56DE56DEA9")


encryption_data = [
    ([0x41], b'0xFF', b'\x41\x43\x5A\x5A\x5E\x5A\x5E\x5A\x5E\x5A\x5E'),
    ([0xBC, 0x7B, 0x7B], b'0xFF', b'\xBC\xBE\xA7\xA2\x59\x1C\x5A\x1C\x5A\x1C'),
]


@pytest.mark.parametrize("input, expected", ceilLog2Data)
def test_cielLog2(input, expected):
    assert MsOvba.ceilLog2(input) == expected
