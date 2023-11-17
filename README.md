[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/MS-OVBA-Crypto/badge.png?branch=main)](https://coveralls.io/github/Beakerboy/MS-OVBA-Crypto?branch=main) ![Build Status](https://github.com/Beakerboy/MS-OVBA-Crypto/actions/workflows/python-package.yml/badge.svg)
# MS-OVBA-Crypto
Cryptographic Functions for Office Visual Basic files.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install MS_OVBA_Compression.

```bash
pip install ms_ovba_crypto
```

## Usage
Microsoft VBA files use a custom encryption algorithm to obfuscate visibility and permission fields. The clsid is used as a seed. 

```python
import ms_ovba_crypto

data = b'\x00\x00\x00\x00',

clsid = '{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}'
# Random numbers are used in the obfuscation, so the output is not deterministic.
encrypted = ms_ovba_crypto.encrypt(clsid, data)

data = b'\x41\x43\x5A\x5A\x5E\x5A\x5E\x5A\x5E\x5A\x5E'

# returns b'\x00\x00\x00\x00'
ms_ovba_crypto.decrypt(data)

```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

