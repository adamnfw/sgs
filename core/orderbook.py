class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}

    def add_order(self, order):
        if order.side == "bid":
            self._add_to_side(self.bids, order)
        elif order.side == "ask":
            self._add_to_side(self.asks, order)

    def _add_to_side(self, side_dict, order):
        price = order.price
        if price not in side_dict:
            side_dict[price] = [order]
        else:
            side_dict[price] = [o for o in side_dict[price] if o.client != order.client]
            side_dict[price].append(order)

    def remove_order(self, client, side):
        if side == "bid":
            price = self._find_bid_price(client)
            if price:
                self.remove_from_price(client, price, self.bids)
        elif side == "ask":
            price = self._find_ask_price(client)
            if price:
                self.remove_from_price(client, price, self.asks)

    # find the best price offered by a client
    def _find_bid_price(self, client):
        for price in sorted(self.bids.keys(), reverse=True):
            if any([o.client == client for o in self.bids[price]]):
                return price
        return None

    def _find_ask_price(self, client):
        for price in sorted(self.asks.keys()):
            if any([o.client == client for o in self.asks[price]]):
                return price
        return None

    def get_client_prices(self, client):
        return (self._find_bid_price(client), self._find_ask_price(client))


    def _remove_from_side(self, side_dict, client):
        for price in list(side_dict.keys()):
            self.remove_from_price(client, price, side_dict)

    def remove_from_price(self, client, price, side_dict):
        side_dict[price] = [o for o in side_dict[price] if o.client != client]
        if not side_dict[price]:
            del side_dict[price]

    def get_order_book(self):
        bid_orders = self._format_orders(self.bids)
        ask_orders = self._format_orders(self.asks)
        return bid_orders, ask_orders

    def num_orders_at_price(self, book):
        return {price:len(book[price]) for price in book.keys()}

    def get_book_by_price(self):
        return (self.num_orders_at_price(self.bids), self.num_orders_at_price(self.asks))

    def _format_orders(self, side_dict):
        orders = []
        for price, orders_at_price in sorted(side_dict.items(), reverse=(side_dict == self.bids)):
            num_orders = len(orders_at_price)
            orders.append({"price": price, "num_orders": num_orders})
        return orders

    def get_top_of_book(self):
        best_bid = max(self.bids.keys()) if self.bids else 0
        best_ask = min(self.asks.keys()) if self.asks else float("inf")
        num_bids = len(self.bids[best_bid]) if best_bid in self.bids else 0
        num_asks = len(self.asks[best_ask]) if best_ask in self.asks else 0
        return best_bid, num_bids, best_ask, num_asks
