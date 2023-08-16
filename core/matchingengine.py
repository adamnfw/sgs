from core.trade import Trade

class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book
        self.trades = []

    def match_orders(self):
        best_bid, num_bids, best_ask, num_asks = self.order_book.get_top_of_book()

        while best_bid >= best_ask:
            bid_orders = self.order_book.bids[best_bid]
            ask_orders = self.order_book.asks[best_ask]

            if len(bid_orders) == 0 or len(ask_orders) == 0:
                break

            buyer = bid_orders[0].client
            seller = ask_orders[0].client
            trade_price = best_ask if bid_orders[0].sequence > ask_orders[0].sequence else best_bid
            trade_sequence = max(bid_orders[0].sequence, ask_orders[0].sequence)

            trade = Trade(buyer, seller, trade_price, trade_sequence)
            self.trades.append(trade)

            self.order_book.remove_order(bid_orders[0].client, "bid")
            self.order_book.remove_order(ask_orders[0].client, "ask")

            best_bid, num_bids, best_ask, num_asks = self.order_book.get_top_of_book()

    def get_trades(self):
        return self.trades

