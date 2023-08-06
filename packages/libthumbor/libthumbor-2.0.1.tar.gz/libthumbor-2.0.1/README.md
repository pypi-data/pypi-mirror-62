[![Build Status](https://secure.travis-ci.org/thumbor/libthumbor.png)](http://travis-ci.org/thumbor/libthumbor) [![Coverage Status](https://coveralls.io/repos/github/thumbor/libthumbor/badge.svg?branch=master)](https://coveralls.io/github/thumbor/libthumbor?branch=master)

libthumbor allows easy usage of
[thumbor](http://github.com/thumbor/thumbor) in Python. Check the docs for django integration.

This version is compliant with the new URL generation schema (thumbor 3.0.0 and up).

## Using it

```python
from libthumbor import CryptoURL

crypto = CryptoURL(key='my-security-key')

encrypted_url = crypto.generate(
    width=300,
    height=200,
    smart=True,
    image_url='/path/to/my/image.jpg'
)
```

## Docs

Check the wiki for more information on using libthumbor.

## Contributions

### Bernardo Heynemann

* Generic URL encryption

### Rafael Caricio

* Django Generic View and URL

### Fábio Costa

* Django Generic View and URL
