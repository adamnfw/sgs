class Trade:
    def __init__(self, buyer, seller, price, sequence):
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.sequence = sequence

    def serialize(self):
        return {
            'buyer': self.buyer,
            'seller': self.seller,
            'price': self.price,
            'sequence': self.sequence,
        }