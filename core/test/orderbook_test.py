from core.order import *
from core.orderbook import OrderBook

import unittest

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.order_book = OrderBook()

    def test_add_order(self):
        order1 = Order("client1", "bid", 10)
        self.order_book.add_order(order1)

        order2 = Order("client2", "bid", 12)
        self.order_book.add_order(order2)

        bid_orders, ask_orders = self.order_book.get_order_book()
        self.assertEqual(bid_orders, [{"price": 12, "num_orders": 1}, {"price": 10, "num_orders": 1}])
        self.assertEqual(ask_orders, [])

    def test_remove_order(self):
        order1 = Order("client1", "bid", 10)
        self.order_book.add_order(order1)

        self.order_book.remove_order("client1", "bid")

        bid_orders, ask_orders = self.order_book.get_order_book()
        self.assertEqual(bid_orders, [])
        self.assertEqual(ask_orders, [])

    def test_get_top_of_book(self):
        order1 = Order("client1", "bid", 10)
        self.order_book.add_order(order1)

        order2 = Order("client2", "ask", 12)
        self.order_book.add_order(order2)

        best_bid, num_bids, best_ask, num_asks = self.order_book.get_top_of_book()
        self.assertEqual(best_bid, 10)
        self.assertEqual(num_bids, 1)
        self.assertEqual(best_ask, 12)
        self.assertEqual(num_asks, 1)

    def test_find_client_price(self):
        order_book = OrderBook()

        order_book.add_order(Order("client1", "bid", 11))
        order_book.add_order(Order("client2", "bid", 12))
        order_book.add_order(Order("client3", "bid", 13))
        order_book.add_order(Order("client4", "bid", 13))

        order_book.add_order(Order("client4", "ask", 21))
        order_book.add_order(Order("client5", "ask", 22))
        order_book.add_order(Order("client6", "ask", 23))

        c2 = order_book.get_client_prices("client2")
        self.assertEqual(c2[0], 12)
        self.assertIsNone(c2[1])

        c4 = order_book.get_client_prices("client4")
        self.assertEqual(c4[0], 13)
        self.assertEqual(c4[1], 21)

        c6 = order_book.get_client_prices("client6")
        self.assertIsNone(c6[0])
        self.assertEqual(c6[1], 23)

        c8 = order_book.get_client_prices("client8")
        self.assertIsNone(c8[0])
        self.assertIsNone(c8[1])

    def test_book_by_price(self):
        order_book = OrderBook()

        order_book.add_order(Order("client1", "bid", 11))
        order_book.add_order(Order("client2", "bid", 12))
        order_book.add_order(Order("client3", "bid", 13))
        order_book.add_order(Order("client4", "bid", 13))

        order_book.add_order(Order("client4", "ask", 21))
        order_book.add_order(Order("client5", "ask", 23))
        order_book.add_order(Order("client6", "ask", 23))

        bid_levels, ask_levels = order_book.get_book_by_price()
        self.assertEqual(3, len(bid_levels))
        self.assertEqual(1, bid_levels[11])
        self.assertEqual(1, bid_levels[12])
        self.assertEqual(2, bid_levels[13])
        self.assertEqual(2, len(ask_levels))
        self.assertEqual(1, ask_levels[21])
        self.assertEqual(2, ask_levels[23])

if __name__ == "__main__":
    unittest.main()

