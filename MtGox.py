import base64, hashlib, hmac, time, json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

base = 'https://data.mtgox.com/api/2/'

def post_request(key, secret, path, data):
    msg = path + chr(0) + data
    hmac_obj = hmac.new(secret, msg.encode('ascii'), hashlib.sha512)
    hmac_sign = base64.b64encode(hmac_obj.digest())

    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'PPClient',
        'Rest-Key': key,
        'Rest-Sign': hmac_sign,
    }

    request = Request(base + path, data, header)
    response = urlopen(request, data.encode('ascii'))
    content = response.read()
    return json.loads(content.decode('utf8'))


def gen_tonce():
    return str(int(time.time() * 1e6))


class MtGox:

    def __init__(self, key, secret):
        self.key = key
        self.secret = base64.b64decode(secret.encode('ascii'))

    def request(self, path, params={}):
        params = dict(params)
        params['tonce'] = gen_tonce()
        # using a list of tuples preservers the order in urlencode
        #params = params.items()
        #params.append(('tonce', gen_tonce()))
        data = urlencode(params)

        result = post_request(self.key, self.secret, path, data)
        if result['result'] == 'success':
            return result['data']
        else:
            raise Exception(result['result'])

