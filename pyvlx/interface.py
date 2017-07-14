import json
import asyncio
import aiohttp
import async_timeout

from .exception import PyVLXException, InvalidToken

class Interface:
    def __init__(self, config):
        self.config = config
        self.token = None


    # pylint: disable=too-many-arguments
    async def api_call(self, verb, action, params=None, add_authorization_token=True, retry=False):
        if add_authorization_token and not self.token:
            await self.refresh_token()

        try:
            return await self.api_call_impl(verb, action, params, add_authorization_token)
        except InvalidToken:
            if not retry and add_authorization_token:
                await self.refresh_token()
                # Recursive call of api_call
                return await self.api_call(verb, action, params, add_authorization_token, True)
            else:
                raise


    async def api_call_impl(self, verb, action, params=None, add_authorization_token=True):
        url = self.create_api_url(self.config.host, verb)
        body = self.create_body(action, params)
        headers = self.create_headers(add_authorization_token, self.token)
        return await self.do_http_request(url, body, headers)


    async def do_http_request(self, url, body, headers):
        try:
            return await self.do_http_request_impl(url, body, headers)
        except asyncio.TimeoutError:
            raise PyVLXException("Request timeout when talking to VELUX API")
        except aiohttp.ClientError:
            raise PyVLXException("HTTP error when talking to VELUX API")
        except OSError:
            raise PyVLXException("OS error when talking to VELUX API")


    async def do_http_request_impl(self, url, body, headers):
        print(url, body, headers)
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.post(url, data=json.dumps(body), headers=headers) as response:
                    response = await response.text()
                    response = self.fix_response(response)
                    print(response)
                    json_response = json.loads(response)
                    self.evaluate_response(json_response)
                    #print(json.dumps(json_response, indent=4, sort_keys=True))
                    return json_response


    async def refresh_token(self):
        json_response = await self.api_call('auth', 'login', {'password': self.config.password}, add_authorization_token=False)
        if not 'token' in json_response:
            raise PyVLXException('no element token found in response: {0}'.format(json.dumps(json_response)))
        self.token = json_response['token']


    async def disconnect(self):
        await self.api_call('auth', 'logout', {}, add_authorization_token=True)
        self.token = None


    @staticmethod
    def create_api_url(host, verb):
        return 'http://{0}/api/v1/{1}'.format(host, verb)


    @staticmethod
    def create_headers(add_authorization_token, token=None):
        headers = {}
        headers['Content-Type'] = 'application/json'
        if add_authorization_token:
            headers['Authorization'] = 'Bearer ' + token
        return headers


    @staticmethod
    def create_body(action, params):
        body = {}
        body['action'] = action
        if params is not None:
            body['params'] = params
        return body


    @staticmethod
    def evaluate_response(json_response):
        if 'errors' in json_response and json_response['errors']:
            Interface.evaluate_errors(json_response)
        elif not 'result' in json_response:
            raise PyVLXException('no element result  found in response: {0}'.format(json.dumps(json_response)))
        elif not json_response['result']:
            raise PyVLXException('Request failed {0}'.format(json.dumps(json_response)))

    @staticmethod
    def evaluate_errors(json_response):
        if not 'errors' in json_response or \
           not isinstance(json_response['errors'], list) or \
           len(json_response['errors']) == 0 or \
           not isinstance(json_response['errors'][0], int):
            raise PyVLXException('Could not evaluate errors {0}'.format(json.dumps(json_response)))

        # unclear if response may contain more errors than one. Taking the first.
        first_error = json_response['errors'][0]

        if first_error in [402, 403, 405, 406]:
            raise InvalidToken(first_error)

        raise PyVLXException('Unknown error code {0}'.format(first_error))

    @staticmethod
    def fix_response(response):
        # WTF: For whatever reason, the KLF 200 sometimes puts an ')]}',' in front of the response ...
        index = response.find('{')
        if index > 0:
            return response[index:]
        return response
