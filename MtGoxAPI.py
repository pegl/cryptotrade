from Currency import Currency

import json

class MtGoxAPI:

    _instance = None
    _config = None
    _mtgox = None
    _currency_pair = None
    _currency = None

    @classmethod
    def get_instance(cls, **kwargs):
        # try:
        if not 'config' in kwargs\
            or not 'mtgox' in kwargs\
            or not 'currency_pair' in kwargs:
            raise Exception('Dependencies missing')

        if cls._instance is None:
            cls._instance = MtGoxAPI()
            cls._instance._config = kwargs['config']
            cls._instance._mtgox = kwargs['mtgox']
            cls._instance._currency_pair = kwargs['currency_pair']
            cls._instance._init_currency()
        # except Exception, e:
        # MtGoxAPI couldn't be initialised
        return cls._instance

    def _init_currency(self):
        self._currency = Currency(self._config)

    def _get_url(self, path, **kwargs):
        exchange = ""
        if 'exchange' in kwargs:
            exchange = kwargs['exchange'] + "/"
        #return api_base_url + exchange + path
        return exchange + path

    def get_balance(self):
        def _parse(resp):
            balance = resp["Wallets"]["AUD"]["Balance"]["display"]
            btc_balance = resp["Wallets"]["BTC"]["Balance"]["display"]
    
            return {
                "balance": balance,
                "btc_balance": btc_balance,
            }
    
        res = self._mtgox.request(self._get_url(self._config.get('service_mtgox', 'money_info_path')))
        #print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))
        print(json.dumps(_parse(res)))
    
        return

    def get_money_info(self):
        res = self._mtgox.request(self._get_url(self._config.get('service_mtgox', 'money_info_path')))
        print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))

    
    def get_exchange(self):
        exchange_string = self._currency_pair.to_string()
        res = self._mtgox.request(
            self._get_url(self._config.get('service_mtgox', 'ticker_path'), 
            exchange=exchange_string)
        )
        print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))
        return
    
    def get_quote(self):
        fixed_cur = self._currency_pair.get_fixed()
        aux_cur = self._currency_pair.get_variable()
        exchange_string = self._currency_pair.to_string()

        def convert_to_int_amount(amount_float):
            amount_int = self._currency.float_to_int(amount_float, fixed_cur)
            return int(amount_int)

        def convert_to_float_amount(amount_int):
            amount_float = self._currency.int_to_float(amount_int, aux_cur)
            return float(amount_float)

        def get_params():
            print("Quote type? (bid, ask)")
            quote_type = input()
            print("Amount? (1.0 = 1.0BTC, 1.0 = 1.0AUD)")
            amount = float(input())
            params = {
                'type': quote_type,
                'amount': convert_to_int_amount(amount)
            }
            return params

        path = self._config.get('service_mtgox', 'money_quote_path')
        res = self._mtgox.request(
            self._get_url(path,exchange=exchange_string),
            params=get_params()
        )
        print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))
        if 'amount' in res:
            quote = res["amount"]
            amount_float = convert_to_float_amount(quote)
            print("Quoted: {0} {1}".format(amount_float, self._currency_pair.get_variable()))
        return

    def add_buy_order(self):
        self.add_order('bid')

    def add_sell_order(self):
        self.add_order('ask')

    # merge with add_sell_order
    def add_order(self, order_type):
        fixed_cur = self._currency_pair.get_fixed()
        aux_cur = self._currency_pair.get_variable()
        exchange_string = self._currency_pair.to_string()

        def convert_to_int_amount(amount_float):
            amount_int = self._currency.float_to_int(amount_float, fixed_cur)
            return int(amount_int)

        def convert_to_float_amount(amount_int):
            amount_float = self._currency.int_to_float(amount_int, aux_cur)
            return float(amount_float)

        def get_params():
            print("Amount? (1.0 = 1.0BTC, 1.0 = 1.0AUD)")
            amount = float(input())
            print("Price (per bitcoin)? (optional for non market rate)")
            price = input()
            params = {
                'type': order_type,
                'amount_int': convert_to_int_amount(amount),
            }
            # if a limit rate is given, add the parameter
            if price:
                params['price_int'] = convert_to_int_amount(float(price))
            return params

        path = self._config.get('service_mtgox', 'money_order_add_path')
        res = self._mtgox.request(
            self._get_url(path,exchange=exchange_string),
            params=get_params()
        )
        print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))
        return

    def view_open_orders(self):
        exchange_string = self._currency_pair.to_string()
        def get_params():
            params = {}
            return params
        def get_orders(res):
            if 'success' in res:
                return res['data']
        path = self._config.get('service_mtgox', 'money_order_info_path')
        res = self._mtgox.request(
            self._get_url(path,exchange=exchange_string),
            params=get_params()
        )
        print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))

    def view_closed_order(self):
        exchange_string = self._currency_pair.to_string()
        def get_params():
            print("Quote type? (bid, ask)")
            order_type = input()
            print("Order id (oid)?")
            oid = str(input())
            params = {
                'type': order_type,
                'order': oid
            }
            return params
        path = self._config.get('service_mtgox', 'money_order_result_path')
        res = self._mtgox.request(
            self._get_url(path,exchange=exchange_string),
            params=get_params()
        )
        print(res)
        print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


    def cancel_order(self):
        exchange_string = self._currency_pair.to_string()
        def get_params():
            print("Order id (oid)?")
            oid = input()
            params = {
                'oid': str(oid)
            }
            return params
        path = self._config.get('service_mtgox', 'money_order_cancel_path')
        res = self._mtgox.request(
            self._get_url(path,exchange=exchange_string),
            params=get_params()
        )
        print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))
    
    def _set_currency(self):
        currencies = self._currency_pair.get_currencies()
        print("Choose a currency: ")
        for i in range(len(currencies) - 1):
            print(str(i + 1) + ") " + currencies[i])
        cur = int(input())
        return currencies[cur - 1]
    
    def set_fixed_cur(self):
        #cur = _set_currency()
        #currency_pair.set_fixed(cur)
        print("Fixed at BTC currently")
        return
    
    def set_variable_cur(self):
        cur = self._set_currency()
        self._currency_pair.set_variable(cur)
        self._currency = Currency(self._config)

