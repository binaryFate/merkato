import time

from merkato.exchanges.tux_exchange.exchange import TuxExchange

DEBUG = True

# This class is for documentation only to show examples of what the 
# public methods should look like on exchange specific classes
class Exchange(object):
    '''Merkato Market Making Bot Exchange Interface
        This class acts as an entry point for all exchange interfaces.
        handling delegation to the proper exchange interface (tux, polo, etc), retry logic, etc.
    '''
    def __init__(self, configuration, coin, base):
        self.exchange   = configuration['exchange']
        self.DEBUG = 100 # TODO: move to configuration object

        self.interface = None
        if self.exchange == "tux":
            self.interface = TuxExchange(configuration, coin=coin, base=base)
        else:
            raise Exception("ERROR: unsupported exchange: {}".format(self.exchange))

        self.retries = 5
        self.limit_only = True

    def debug(self, level, header, *args):
        if level <= self.DEBUG:
            print("-"*10)
            print("{}---> {}:".format(level, header))
            for arg in args:
                print("\t\t" + repr(arg))
            print("-" * 10)

    def sell(self, amount, ask):
        attempt = 0
        while attempt < self.retries:
            if self.limit_only:
                # Get current highest bid on the orderbook
                # If ask price is lower than the highest bid, return.
                pass
            try:
                success = self.interface.sell(amount, ask)
                if success:
                    self.debug(2, "sell", "SELL {} {} at {} on {}".format(amount, self.interface.ticker, ask, self.exchange))
                    return success
                else:
                    self.debug(1, "sell","SELL {} {} at {} on {} FAILED - attempt {} of {}".format(amount, self.interface.ticker, ask, self.exchange, attempt, self.retries))
                    attempt += 1
                    time.sleep(5)
            except Exception as e:  # TODO - too broad exception handling
                self.debug(0, "sell", "ERROR", e)
                break


    def buy(self, amount, bid):
        attempt = 0
        while attempt < self.retries:
            if self.limit_only:
                # Get current lowest ask on the orderbook
                # If bid price is higher than the lowest ask, return.
                pass

            try:
                success = self.interface.buy(amount, bid)
                if success:
                    self.debug(2, "buy", "BUY {} {} at {} on {}".format(amount, self.interface.ticker, bid, self.exchange))
                    return success
                else:
                    self.debug(1, "buy", "BUY {} {} at {} on {} FAILED - attempt {} of {}".format(amount, self.interface.ticker, bid, self.exchange, attempt, self.retries))
                    attempt += 1
                    time.sleep(5)
            except Exception as e:  # TODO - too broad exception handling
                self.debug(0, "buy", "ERROR", e)
                return False


    def get_all_orders(self):
        return self.interface.get_all_orders()


    def get_my_open_orders(self):
        return self.interface.get_my_open_orders()


    def get_my_trade_history(self, start=0, end=0):
        return self.interface.get_my_trade_history(start, end)


    def cancel_order(self, order_id):
        return self.interface.cancel_order(order_id)

    def get_balances(self):
        return self.interface.get_balances()

    def get_last_trade_price(self):
        return self.interface.get_last_trade_price()

    def get_lowest_ask(self):
        return self.interface.get_lowest_ask()

    def get_highest_bid(self):
        return self.interface.get_highest_bid()


