from __future__ import absolute_import

import requests

from requests.exceptions import ConnectionError, Timeout

import ricloud
from ricloud import conf, __version__
from ricloud.exceptions import RequestError, ServerError
from ricloud.utils import encode, encode_json, decode_json


def get_user_agent_header():
    return "ricloud-py/{version}".format(version=__version__)


def get_auth_header():
    return "Token {token}".format(token=ricloud.token)


class RequestHandler(object):
    def __init__(self):
        self.session = requests.Session()

        self.max_retries = conf.getint("api", "max_retries")
        self.await_for = conf.get("api", "await_for")

    def set_headers(self, headers):
        headers = headers or {}

        headers.setdefault("User-Agent", get_user_agent_header())
        headers.setdefault("Authorization", get_auth_header())

        if self.await_for:
            headers.setdefault("Ricloud-Await", self.await_for)

        return headers

    def get(self, url, headers=None, params=None):
        if params:
            for param, value in params.items():
                encoded_value = encode(value)
                params[param] = encoded_value if encoded_value is not None else value

        return self.send("GET", url, headers=headers, params=params)

    def post(self, url, headers=None, data=None):
        json_data = encode_json(data)

        return self.send("POST", url, headers=headers, data=json_data)

    def delete(self, url, headers=None):
        return self.send("DELETE", url, headers=headers)

    def send(self, method, url, headers=None, data=None, params=None):
        headers = self.set_headers(headers)

        response = self._send(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            retries_remaining=self.max_retries,
        )

        if response.status_code >= 500:
            raise ServerError(response.status_code, response.content)
        elif response.status_code >= 400:
            raise RequestError(response.status_code, response.content)

        return decode_json(response.content), response.status_code

    def _send(self, method, url, headers, data, params, retries_remaining=None):
        try:
            response = self.session.request(
                method=method, url=url, headers=headers, data=data, params=params
            )
        except (ConnectionError, Timeout):
            if not retries_remaining:
                raise

            response = None

        # Explicit None comparison as bad responses are falsey.
        if response is None or (response.status_code >= 500):
            if retries_remaining:
                return self._send(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                    params=params,
                    retries_remaining=retries_remaining - 1,
                )

        return response
