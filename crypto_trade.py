import sys, traceback
import json

import os
import configparser

import json

from MtGox import MtGox
from MtGoxAPI import MtGoxAPI
from CurrencyPair import CurrencyPair

# Make every endpoint represented in code, configurable in a config or ini
# file

# app configuration, will later create a store for these values 
config          = None
api_key         = None
api_secret      = None
api_base_url    = None
ticker_path     = None
money_info_path = None

mtgox           = None
mtgox_api       = None
currency_pair   = None

def parse_option(selection):
    opt = get_options()
    selection -= 1 # ugly, but removes the menu offset
    try:
        print("You chose {0}".format(opt[selection][0]))
        # watch out, magic at play
        #globals()[opt[selection][0]]()
        mtgox_api_call = getattr(mtgox_api, opt[selection][0])
        mtgox_api_call()
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        print("Couldn't find this selection")
    print("Ok\n")

# these could map to function calls
def get_options():
    options = [
        ("set_fixed_cur", "Set fixed currency"),
        ("set_variable_cur", "Set variable currency"),
        ("get_balance", "Get account balance"),
        ("get_exchange", "Get exchange rate"),
        ("get_quote", "Get quote"),
        ("add_buy_order", "Buy (Request)"),
        ("add_sell_order", "Sell (Offer)"),
        ("cancel_order", "Cancel order"),
        ("place_holder", "------------"),
        ("view_open_orders", "View open orders"),
        ("view_closed_order", "View closed order"),
        ("place_holder", "------------"),
        ("get_money_info", "Get account info!"),
    ]
    return options

def print_options(opt):
    i = 1
    for o in opt:
        print("{0}) {1}".format(i, o[1]))
        i += 1

def _read_base_config(config):
    global api_key, api_secret
    api_key = config.get('service_mtgox', 'api_key')
    api_secret = config.get('service_mtgox', 'api_secret')

def _read_url_paths(config):
    global  api_base_url, ticker_path, money_info_path
    api_base_url = config.get('service_mtgox', 'api_base_url')
    ticker_path = config.get('service_mtgox', 'ticker_path')
    money_info_path = config.get('service_mtgox', 'money_info_path')

def _read_config():
    global config
    config = configparser.ConfigParser()
    config.read('crypto_trade.cfg')
    _read_base_config(config)
    _read_url_paths(config)

def _init():
    global config
    _init_currency_pair(config)
    _init_mtgox()

def _init_mtgox():
    global mtgox
    global mtgox_api
    mtgox = MtGox(api_key, api_secret)
    mtgox_api = MtGoxAPI.get_instance(
        config=config,
        mtgox=mtgox,
        currency_pair=currency_pair
    )

def _init_currency_pair(config):
    global currency_pair
    fix_currency = config.get('service_mtgox', 'fix_currency')
    var_currency = config.get('service_mtgox', 'var_currency')
    currency_pair = CurrencyPair(fix_currency, var_currency)

def run():
    _read_config()
    _init()

    selection = None

    while True:

        #try:
        os.system('clear')
        print("Currency Pair: ({0})".format(currency_pair.to_string()))
        print("Please make a choice:")
        print_options(get_options())
        while not selection:
            selection = input()
        parse_option(int(selection))
        selection = input()
        #except Exception as e:
        #    print(e)
        #    print("Something bad happened\n\n")

        selection = None

if __name__ == '__main__':
    run()
