class CurrencyPair:

    _cur1 = 'BTC'
    _cur2 = 'USD'

    _currencies = ['USD', 'AUD', 'EUR', 'PLN', 'GBP']

    def __init__(self, cur1, cur2):
        self._cur1 = cur1
        self._cur2 = cur2

    def set_fixed(self, cur):
        self._cur1 = cur

    def set_variable(self, cur):
        self._cur2 = cur

    def get_fixed(self):
        return self._cur1

    def get_variable(self):
        return self._cur2

    def to_string(self):
        return self._cur1 + self._cur2

    def get_currencies(self):
        return self._currencies

