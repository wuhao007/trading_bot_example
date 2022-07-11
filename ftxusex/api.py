# This file is part of krakenex.
#
# krakenex is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# krakenex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser
# General Public LICENSE along with krakenex. If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> and
# <http://www.gnu.org/licenses/gpl-3.0.txt>.
"""Kraken.com cryptocurrency Exchange API."""

import requests

# private query nonce
import time

# private query signing
import urllib.parse
import hashlib
import hmac
import base64

from . import version


class API(object):
    """ Maintains a single session between this machine and Kraken.

    Specifying a key/secret pair is optional. If not specified, private
    queries will not be possible.

    The :py:attr:`session` attribute is a :py:class:`requests.Session`
    object. Customise networking options by manipulating it.

    Query responses, as received by :py:mod:`requests`, are retained
    as attribute :py:attr:`response` of this object. It is overwritten
    on each query.

    .. note::
       No query rate limiting is performed.

    """

    def __init__(self, key='', secret=''):
        """ Create an object with authentication information.

        :param key: (optional) key identifier for queries to the API
        :type key: str
        :param secret: (optional) actual private key used to sign messages
        :type secret: str
        :returns: None

        """
        self.key = key
        self.secret = secret
        self.uri = 'https://ftx.us/api'
        self.apiversion = '0'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'ftxusex/0.1.0'})
        self.response = None
        self._json_options = {}
        return

    def json_options(self, **kwargs):
        """ Set keyword arguments to be passed to JSON deserialization.

        :param kwargs: passed to :py:meth:`requests.Response.json`
        :returns: this instance for chaining

        """
        self._json_options = kwargs
        return self

    def close(self):
        """ Close this session.

        :returns: None

        """
        self.session.close()
        return

    def load_key(self, path):
        """ Load key and secret from file.

        Expected file format is key and secret on separate lines.

        :param path: path to keyfile
        :type path: str
        :returns: None

        """
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()
        return

    def _query(self, urlpath, data, http_method, headers=None, timeout=None):
        """ Low-level query handling.

        .. note::
           Use :py:meth:`query_private` or :py:meth:`query_public`
           unless you have a good reason not to.

        :param urlpath: API URL path sans host
        :type urlpath: str
        :param data: API request parameters
        :type data: dict
        :param headers: (optional) HTTPS headers
        :type headers: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object
        :raises: :py:exc:`requests.HTTPError`: if response status not successful

        """
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        url = self.uri + urlpath

        self.response = getattr(self.session, http_method)(url,
                                         data=data,
                                         headers=headers,
                                         timeout=timeout)

        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()

        return self.response.json(**self._json_options)

    def query_public(self, method, http_method, data=None, timeout=None):
        """ Performs an API query that does not require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param data: (optional) API request parameters
        :type data: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object

        """
        if data is None:
            data = {}

        urlpath = f'/{method}'

        return self._query(urlpath, data, http_method, timeout=timeout)

    def query_private(self, method, http_method, data=None, timeout=None):
        """ Performs an API query that requires a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param data: (optional) API request parameters
        :type data: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object

        """
        if data is None:
            data = {}

        if not self.key or not self.secret:
            raise Exception(
                'Either key or secret is not set! (Use `load_key()`.')

        # data['nonce'] = self._nonce()

        urlpath = f'/{method}'

        # headers = {
        #     'FTXUS-KEY': self.key,
        #     'FTXUS-SIGN': self._sign(data, urlpath),
        #     'FTXUS-TS': str(self._nonce())
        #}
        headers = self._sign(data, urlpath)

        return self._query(urlpath, data, http_method, headers, timeout=timeout)

    def _nonce(self):
        """ Nonce counter.

        :returns: an always-increasing unsigned integer (up to 64 bits wide)

        """
        return int(1000 * time.time())

    def _sign(self, data, urlpath):
        """ Sign request data according to Kraken's scheme.

        :param data: API request parameters
        :type data: dict
        :param urlpath: API URL path sans host
        :type urlpath: str
        :returns: signature digest
        """
        ts = self._nonce()
        request = requests.Request('GET', self.uri + urlpath)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self.secret.encode(), signature_payload, 'sha256').hexdigest()

        headers = {
             'FTXUS-KEY': self.key,
             'FTXUS-SIGN': signature,
             'FTXUS-TS': str(ts)
        }
        prepared.headers.update(headers)


        # postdata = urllib.parse.urlencode(data)

        # Unicode-objects must be encoded before hashing
        # encoded = postdata.encode()
        # message = urlpath.encode() + hashlib.sha256(encoded).digest()

        # signature = hmac.new(base64.b64decode(self.secret), message,
        #                      hashlib.sha512)
        # sigdigest = base64.b64encode(signature.digest())

        # return sigdigest.decode()
        return headers

    def get_ask_bid(self, pair):
        """
        https://ftx.us/api/markets/BTC/USD/orderbook?depth=1
        {"success":true,"result":{"bids":[[20512.0,5.3274]],"asks":[[20514.0,0.365]]}}
        """
        ticker = self.query_public(f'markets/{pair}/orderbook', 'get', {'depth': 1})
        result = ticker['result']
        return float(result.get('asks')[0][0]), float(result.get('bids')[0][0])

    def add_order(self, pair, buyorsell, vol, price, ref, price_cell):
        return self.query_private(
            'orders', 'post', {
                'market': pair,
                'side': buyorsell,
                'price': str(price_cell % price),
                'type': 'limit',
                'size': str('%.8f' % vol),
                "reduceOnly": False,
                "ioc": False,
                "postOnly": False,
                "clientId": ref,
            }, )

    def get_cost(self, ref, result):
        """Order select.

        here we use pair and userref to distinguish between orders. 
        return txid and order information
        """
        id = result['id']
        sleep_time = 1
        while True:
            result = self.query_private(f'orders/by_client_id/{ref}', 'get').get(
                'result')
            if result['status'] == 'closed' and result['id'] == id:
                return result['filledSize'] * result['avgFillPrice']
            else:
                time.sleep(sleep_time)
                sleep_time *= 2