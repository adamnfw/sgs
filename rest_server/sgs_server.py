from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS

import random
from core.order import Order
from core.trade import Trade
from core.orderbook import OrderBook
from core.matchingengine import MatchingEngine

app = Flask(__name__)
CORS(app)

# Global variable for storing client tokens
client_tokens = set()

# Initialize OrderBook and MatchingEngine
order_book = OrderBook()
matching_engine = MatchingEngine(order_book)

@app.route('/join', methods=['GET'])
def join_page():
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    # Generate a unique token for the client
    while True:
        token = f"{name}{random.randint(10000, 99999)}"
        if token not in client_tokens:
            client_tokens.add(token)
            return jsonify({'token': token})

# Endpoint for posting quotes
@app.route('/quote', methods=['POST'])
def quote():
    data = request.get_json()
    token = data.get('token')
    if not token or token not in client_tokens:
        return jsonify({'error': 'Invalid token'}), 401

    bid = int(data.get('bid'))
    ask = int(data.get('ask'))

    if bid < 0 or ask <= 0 or bid >= ask:
        return jsonify({'error': 'Invalid quote'}), 400

    # Remove any previous quote from the same client token
    order_book.remove_order(token, 'bid')
    order_book.remove_order(token, 'ask')
    order_book.add_order(Order(token, 'bid', bid))
    order_book.add_order(Order(token, 'ask', ask))

    # Run the MatchingEngine to generate trades and remove crossed orders
    matching_engine.match_orders()

    return jsonify({'message': 'Quote added successfully'})

# Endpoint for getting bid and ask prices for a client
@app.route('/prices', methods=['GET'])
def get_client_prices():
    token = request.args.get('token')
    if not token or token not in client_tokens:
        return jsonify({'error': 'Invalid token'}), 401

    bid_price, ask_price = order_book.get_client_prices(token)
    return jsonify({'bid': bid_price, 'ask': ask_price})

@app.route('/joinquote', methods=['GET'])
def joinquote():
    return render_template('joinquote.html')

@app.route('/get_orderbook', methods=['GET'])
def get_orderbook():
    bids, asks = order_book.get_book_by_price()

    # Create a list to hold the data for each row
    orderbook_data = []

    # Find the highest bid and lowest ask
    max_bid = max(bids.keys()) if bids else 0
    min_ask = min(asks.keys()) if asks else 100

    # Loop through the price range from 4 below the highest bid to 4 above the lowest ask
    for price in range(max_bid - 4, min_ask + 5):
        bid_count = bids.get(price, 0)
        ask_count = asks.get(price, 0)
        orderbook_data.append({'bids': bid_count, 'price': price, 'asks': ask_count})

    # return jsonify(orderbook_data)
    return render_template('orderbook.html', orderbook_data=orderbook_data)

@app.route('/game')
def game():
    token = request.args.get('token')
    return render_template('game.html', token=token)

# Endpoint for getting top-of-book values
@app.route('/top-of-book', methods=['GET'])
def top_of_book():
    top_of_book = order_book.get_top_of_book()
    return jsonify(top_of_book)

# Endpoint for getting the list of trades
@app.route('/trades')
def get_trades():
    trades = matching_engine.get_trades()
    return render_template('trades.html', trades=trades)

@app.route('/testgrid', methods=['GET'])
def testgrid():
    return render_template('testgrid.html')

if __name__ == '__main__':
    app.run(debug=True)
