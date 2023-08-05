# BrightHive Auth Library

Authlib is a library built specifically for simplifying the task of adding authentication and authorization features to RESTful web services that reside within BrightHive Data Trusts. With this library, developers simply need to provision an OAuth 2.0 provider and inject it into a simple decorator to protect specific URLs.

## Quick Links

- [Read the docs](https://brighthive-authlib.readthedocs.io/en/latest/)

## Features

- Built-in Support for Auth0.
- Simple decorator for injecting auth capabilities into applications.
- Purpose-built for use with [Flask](http://flask.pocoo.org/) applications, however can be extended to other frameworks.

## Installation

### PyPi

[Pypi](https://pypi.org) is the fastest method for installing this library. Simply install the `brighthive-authlib` package via the Pip installer. This library is intended for use with Python 3.5+.

```bash
pip install brighthive-authlib
```

### Pipenv

Installing the library via [Pipenv](https://pipenv.readthedocs.io/en/latest/) is straightforward.

```bash
pipenv install brighthive-authlib
```

### Dependencies

- flask >= 1.0.2
- pycryptodome >= 3.8.0
- python-jose[pycryptodome] >= 3.0.1
- requests >= 2.21.0

## Usage

### Auth0 Example

The code snippet shown below is a simple Flask application configured to use [Auth0](https://auth0.com) as the default OAuth 2.0 provider. Three steps are required to configure the library for use with a Flask application:

1. Instantiate the OAuth 2.0 provider object.
2. Decorate the route(s) to protect with the `token_required` decorator (passing the OAuth 2.0 provider object and optionally a dictionary of scopes).
3. Configure the custom error handler to deal with `OAuth2ProviderError` exceptions (in this example, a 401 status is returned).
4. Sit back and marvel at how painless the entire process is.

```python
import json
from flask import Flask, request
from brighthive_authlib import OAuth2ProviderError, OAuth2ProviderFactory, AuthLibConfiguration, token_required


# Warning: Testing purposes only. These attributes need to be protected.
PROVIDER = 'AUTH0'
OAUTH2_URL = 'https://brighthive-test.auth0.com'
JSON_URL = '{}/.well-known/jwks.json'.format(OAUTH2_URL)
AUDIENCE = 'http://localhost:8000'
ALGORITHMS = ['RS256']

# Build the Auth Service Configuration Object
auth_config = AuthLibConfiguration(
    provider=PROVIDER, base_url=OAUTH2_URL, jwks_url=JSON_URL, algorithms=ALGORITHMS, audience=AUDIENCE)
oauth2_provider = OAuth2ProviderFactory.get_provider(PROVIDER, auth_config)


# Builed the Flask App
app = Flask(__name__)

# Add a Public Route
@app.route('/public')
def public_resource():
    return json.dumps({'message': 'You can see me because I am public!'}), 200

# Add a Private Route
@app.route('/private')
@token_required(oauth2_provider, ['get:users'])
def private_resource():
    return json.dumps({'message': 'If you can see me, you have a valid token.'}), 200

# Error Handler for Invalid or Expired Tokens
@app.errorhandler(OAuth2ProviderError)
def handle_auth_error(e):
    return json.dumps({'message': 'Access Denied'}), 401


if __name__ == '__main__':
    app.run(debug=True)
```

## Contributing

To contribute code to this project, simply:

1. Fork the repository from [here](https://github.com/brighthive/authlib).
2. Write some code and associated unit tests.
3. Create a pull request.

## Setting up for Development

To set up a development environment, clone the repository and create a virtual environmemt with [Pipenv](https://docs.pipenv.org/).

```bash
git clone git@github.com:brighthive/tpot-abacus-api.git
cd tpot-abacus-api
```

Install Python project and development dependencies.

```bash
pipenv install --dev
```

## Testing

This project uses the excellent [pytest](https://docs.pytest.org/en/latest/) and [expects](https://github.com/jaimegildesagredo/expects) libraries for unit testing. All unit tests are housed in the `tests` module. To run unit tests, invoke `pytest` at the command prompt.

```bash
$ pytest

======= test session starts =======
platform darwin -- Python 3.7.2, pytest-4.3.1, py-1.8.0, pluggy-0.9.0
rootdir: /Users/gmundy/Work/brighthive-data-trusts/authlib, inifile: pytest.ini
plugins: cov-2.6.1
collected 2 items

tests/test_provider_factory.py ..      [100%]

=========== 2 passed in 0.60 seconds ===========
```

## License

### The MIT License (MIT)

Copyright © `2019` `BrightHive`

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
