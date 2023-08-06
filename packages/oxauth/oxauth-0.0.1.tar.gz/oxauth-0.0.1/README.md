# auth-python

[![Build Status](https://travis-ci.org/openstax/auth-python.svg?branch=master)](https://travis-ci.org/openstax/auth-python)

A Python package with strategies for reading OpenStax authentication cookies.

## Usage

`pip install openstax_auth`

```python
from openstax_auth import Strategy2

strategy = Strategy2(
    signature_public_key="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
    signature_algorithm="RS256",
    encryption_private_key="encryption_private_key_here",
    encryption_algorithm="A256GCM",
    encryption_method="dir"
)

payload = strategy.decrypt(cookie) # cookie is the body of the auth cookie

payload.user_uuid # this is the user's UUID
```

Note that the part that is hidden above is the signature private key, without which
others cannot forge a cookie value.

If the cookie is bad or the keys don't work on it, the `payload` will have value `None`.

## Development

All development is done inside a docker container.  From your host running Docker, in this directory run:

```
$> docker-compose up -d
%> ./docker/bash
```

This will drop you into the running container

## Run tests

From within the container, you can run tests with:

```
$ /code> python -m pytest
```

For debugging, you can use `ipdb`, e.g.

```
import ipdb; ipdb.set_trace()
```

When running tests with the debugger make sure to use the `-s` option to prevent pytest from capturing output.

`$> python -m pytest -s tests -k 'test_decrypts'`

Note that `pytest` is also on the `PATH` so you can call it directly.

## Distributing

From within the container, build the distributions:

```
$> python setup.py sdist bdist_wheel
```

## Note on names

We started naming the package `openstax_auth` but there seems to be weirdness in how different parts of the Python tooling replace underscores with hyphens.  We want the package name to be simple and not confusing on `import` so we shortened to `oxauth`.
