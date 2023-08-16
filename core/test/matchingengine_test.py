from core.order import *
from core.orderbook import OrderBook
from core.matchingengine import MatchingEngine

import unittest

class TestMatchingEngine(unittest.TestCase):
    def test_match_orders_no_cross(self):
        order_book = OrderBook()
        matching_engine = MatchingEngine(order_book)
        order1 = Order("client1", "bid", 10)
        order_book.add_order(order1)

        order2 = Order("client2", "ask", 12)
        order_book.add_order(order2)

        matching_engine.match_orders()

        trades = matching_engine.get_trades()
        self.assertEqual(trades, [])

    def test_match_orders_single_cross(self):
        order_book = OrderBook()
        matching_engine = MatchingEngine(order_book)

        order1 = Order("client1", "bid", 10)
        order_book.add_order(order1)

        order2 = Order("client2", "ask", 10)
        order_book.add_order(order2)

        matching_engine.match_orders()

        trades = matching_engine.get_trades()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].buyer, "client1")
        self.assertEqual(trades[0].seller, "client2")
        self.assertEqual(trades[0].price, 10)

    def test_match_orders_single_over(self):
        order_book = OrderBook()
        matching_engine = MatchingEngine(order_book)

        order1 = Order("client1", "bid", 10)
        order_book.add_order(order1)

        order2 = Order("client2", "bid", 12)
        order_book.add_order(order2)

        order3 = Order("client1", "ask", 11)
        order_book.add_order(order3)

        matching_engine.match_orders()

        trades = matching_engine.get_trades()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].buyer, "client2")
        self.assertEqual(trades[0].seller, "client1")
        self.assertEqual(trades[0].price, 12)

    def test_match_large_book(self):
        order_book = OrderBook()
        matching_engine = MatchingEngine(order_book)

        order1 = Order("client1", "bid", 10)
        order_book.add_order(order1)

        order2 = Order("client2", "bid", 11)
        order_book.add_order(order2)

        order3 = Order("client3", "bid", 11)
        order_book.add_order(order3)

        order4 = Order("client4", "bid", 12)
        order_book.add_order(order4)

        order5 = Order("client5", "bid", 12)
        order_book.add_order(order5)


        order6 = Order("client6", "ask", 18)
        order_book.add_order(order6)
        order7 = Order("client7", "ask", 11)
        order_book.add_order(order7)
        order8 = Order("client8", "ask", 17)
        order_book.add_order(order8)
        order9 = Order("client9", "ask", 12)
        order_book.add_order(order9)
        order0 = Order("client0", "ask", 19)
        order_book.add_order(order0)

        matching_engine.match_orders()

        trades = matching_engine.get_trades()
        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0].buyer, "client4")
        self.assertEqual(trades[0].seller, "client7")
        self.assertEqual(trades[0].price, 12)
        self.assertEqual(trades[1].buyer, "client5")
        self.assertEqual(trades[1].seller, "client9")
        self.assertEqual(trades[1].price, 12)