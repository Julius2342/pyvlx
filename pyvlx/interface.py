import json
import aiohttp
import async_timeout


class Interface:
    def __init__(self, config):
        self.config = config
        self.token = None


    async def api_call(self, verb, action, params=None, add_authorization_token=True):
        if add_authorization_token and not self.token:
            await self.refresh_token()

        url = self.create_api_url(self.config.host, verb)
        body = self.create_body(action, params)
        headers = self.create_headers(add_authorization_token, self.token)

        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.post(url, data=json.dumps(body), headers=headers) as response:
                    response = await response.text()
                    response = self.fix_response(response)
                    json_response = json.loads(response)
                    self.evaluate_response(json_response)
                    #print(json.dumps(json_response, indent=4, sort_keys=True))
                    return json_response


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
        if not 'result' in json_response:
            raise Exception('no element result  found in response: {0}'.format(json.dumps(json_response)))
        if not json_response['result']:
            raise Exception('Request failed {0}'.format(json.dumps(json_response)))


    @staticmethod
    def fix_response(response):
        # WTF: For whatever reason, the KLF 200 sometimes puts an ')]}',' in front of the response ...
        index = response.find('{')
        if index > 0:
            return response[index:]
        return response


    async def refresh_token(self):
        json_response = await self.api_call('auth', 'login', {'password': self.config.password}, add_authorization_token=False)
        if not 'token' in json_response:
            raise Exception('no element token found in response: {0}'.format(json.dumps(json_response)))
        self.token = json_response['token']
