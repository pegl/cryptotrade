""" 
   Currency

   We have to divide the integer representation by the division to 
   get the float value for display

   Later if we subclass Currency for other purposes we should move the 
   conversion into its own class

"""
class Currency:

    _config = None

    def __init__(self, config):
        self._config = config

    def _get_division(self, currency):
        return float(self._config.get('mtgox_currency_division', \
                currency))

    def float_to_int(self, floatval, currency):
        division = self._get_division(currency)
        intval = floatval
        intval = intval * division
        # multiply by division
        # cast
        intval = int(intval)
        return intval

    def int_to_float(self, intval, currency):
        division = self._get_division(currency)
        floatval = intval
        # multiply by division
        floatval = floatval * (1 / division)
        # cast
        floatval = float(floatval)
        return floatval

    
