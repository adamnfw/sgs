
class Order:
    sequence_number = 0

    def __init__(self, client, side, price):
        self.sequence = Order.sequence_number
        self.client = client
        self.side = side
        self.price = price
        Order.sequence_number += 1