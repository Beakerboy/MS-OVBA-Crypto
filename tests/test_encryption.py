from ms_ovba_crypto import MsOvbaCrypto


def test_encryption():

    clsid = '{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'

    class OverrideRand(MsOvbaCrypto):
        _rand_list = [0x41, 0xBC, 0x7B, 0x7B, 0x37, 0x7B, 0x7B, 0x7B]
        @staticmethod
        def _make_seed():
            return OverrideRand._rand_list(0)

    ms_ovba_crypto = OverrideRand()
    assert ms_ovba_crypto.encrypt(clsid, b'\xFF') == b'\x41\x43\x5A\x5A\x5E\x5A\x5E\x5A\x5E\x5A\x5E'
    # project.setProtectionState("41435A5A5E5A5E5A5E5A5E")
    # project.setPassword("BCBEA7A2591C5A1C5A1C")
    # project.setVisibilityState("37352C2BDCDD56DE56DEA9")
