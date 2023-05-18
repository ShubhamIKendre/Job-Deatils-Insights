import websocket
import json
# import mysql.connector
import time
import itertools
from collections import OrderedDict
import os
# Set up the MySQL client
# mysql_client = mysql.connector.connect(
#   host="localhost",
#   user="username",
#   password="password",
#   database="MarketData"
# )

# Define the WebSocket URL
ws_url = 'wss://ws-feed.pro.coinbase.com'

symbols = ['BTC-USD','ETH-USD','SHIB-USD','DOGE-USD']
# Define the message to subscribe to the 'ticker' channel for the BTC-USD currency pair

# cursor = mysql_client.cursor(buffered=True)
# cursor.execute("DELETE FROM Bid_data")
# cursor.execute("DELETE FROM Ask_data")

#cursor.execute("CREATE TABLE Bid_data ( price float(5,2), amount FLOAT(5,2), symbol VARCHAR );")



subscribe_message = {
    'type': 'subscribe',
    'channels': [{'name': 'level2', 'product_ids':symbols }]
}

snapshot = {}

def sortedDict(myDict,flag):
    myKeys=list(myDict.keys())
    if(flag):
        myKeys = myKeys.sort(reverse=True)
    else:
        myKeys = myKeys.sort(reverse=False)
    NewDict = {i:myDict[i] for i in myKeys }
    return NewDict

def print_bids_asks(snapshot):

    for symbol in snapshot:
        bids = snapshot[symbol]['bid']
        asks = snapshot[symbol]['ask']
        max_len = max(len(bids), len(asks))
        print(f"{'\n\nSymbol'.ljust(8)}| {'Bids'.ljust(22)} | {'Asks'}")
        print(f"{' '.ljust(10)}| {'Price'.ljust(10)} | {'Amount'.ljust(9)} | {'Price'.ljust(10)} | {'Amount'.ljust(10)}")
        print("-" * 58)
        for i in range(max_len):
            if i < len(bids):
                bid_price, bid_size = list(bids.items())[i]
                bid_price_str = str(bid_price).ljust(10)
                bid_size_str = str(bid_size).ljust(10)
            else:
                bid_price_str = " " * 10
                bid_size_str = " " * 10
            if i < len(asks):
                ask_price, ask_size = list(asks.items())[i]
                ask_price_str = str(ask_price).ljust(10)
                ask_size_str = str(ask_size).ljust(10)
            else:
                ask_price_str = " " * 10
                ask_size_str = " " * 10
        print(symbol.ljust(10), bid_price_str, bid_size_str, "|", ask_price_str, ask_size_str)

def on_message(ws, message):
    data = json.loads(message)
    #print("\n",data)
    if data['type'] == 'snapshot':
        bids = data['bids'][:10]
        bid_value = {}
        for bid in bids:
            price, amount, *rest = bid
            query = "INSERT INTO Bid_data (price, amount, symbol) VALUES (%s, %s, %s)"
            values = (float(price), float(amount), data['product_id'])
            bid_value[float(price)] = amount
            
            
        asks = data['asks'][:10]
        ask_value = {}
        for ask in asks:
            price, amount, *rest = ask
            query = "INSERT INTO Ask_data (price, amount, symbol) VALUES (%s, %s, %s)"
            values = (float(price), float(amount), data['product_id'])
            ask_value[float(price)] = float(amount)
        
        snapshot[data['product_id']] = {'bid': bid_value, 'ask': ask_value}
        
        print_bids_asks(snapshot)
        time.sleep(1/100)
        os.system('clear')
        # time.sleep(2)
        
    
    if data['type'] == 'l2update':
         change = data['changes'][0]
         price = float(change[1])
         amount = float(change[2])
         symbol = data['product_id']
         #print(data)
         
         if change[0] == 'buy':
            if price in list(snapshot[symbol]['bid'].keys()):
                # define the update query
                update_query = "UPDATE Bid_data amount=%s WHERE price=%s"
                values = (amount, symbol, price)
                cursor.execute(update_query, values)
                mysql_client.commit()
                snapshot[symbol]['bid'][price] = amount
       
            else:
                bid_value = snapshot[symbol]['bid']
                bid_value[price] = amount
                #print('\nBid:- ',bid_value)
                dict1 = OrderedDict(sorted(bid_value.items(),reverse=True))
                out = dict(itertools.islice(dict1.items(), 10))
                #print("\n",out)
                snapshot[symbol]['bid'] = out
                
                # print("\nUpdate Msg:- "),
                # print("\nBid Update:- ",snapshot[symbol]['bid'])
                # print("Length Update Bid:- ",len(snapshot[data['product_id']]['bid']))
                
                last_price = dict1.keys()[-1]
                last_amount = dict1[last_price]
                
                update_query = "UPDATE Bid_data SET price=%s, amount=%s WHERE price=%s"
                values = (price, amount, symbol, last_price)
                print("\nUpdate:-")
                
         if change[0] == 'sell':
            if price in list(snapshot[symbol]['ask'].keys()):
                update_query = "UPDATE Bid_data amount=%s WHERE symbol=%s AND price=%s"
                values = (amount, symbol, price)
                snapshot[symbol]['ask'][price] = amount
       
            else:
                ask_value = snapshot[symbol]['ask']
                ask_value[price] = amount
                dict1 = OrderedDict(sorted(ask_value.items()))
                out = dict(itertools.islice(dict1.items(), 10))
                snapshot[symbol]['ask'] = out

         print_bids_asks(snapshot)
         time.sleep(1/100)
         os.system('clear')
                             
# Connect to the WebSocket and subscribe to the level 2 channel
ws = websocket.WebSocketApp(ws_url, on_message=on_message)
ws.on_open = lambda ws: ws.send(json.dumps(subscribe_message))
ws.run_forever()
