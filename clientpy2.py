import socket
import sys

USERNAME = 'SE_Phoenix_2017'

PASSWORD = 'se2017'
def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    result = []

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            result.append(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

    return  result
'''
def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()
'''
def run_command (command):
    while True:
        try:
          return run(USERNAME, PASSWORD, command)
        except KeyboardInterrupt:
          raise
        except:
          print "Warning: Network Failed!"


my_cash = 0
my_securities = {}
my_orders = {}
securities = {}
orders = {}


# get cash
def get_my_cash():
    global my_cash
    result = run_command("MY_CASH")
    return float(result[0].split()[1])

def get_my_securities():
  global my_securities
  my_securities = {}
  result = run_command("MY_SECURITIES")[0].split()[1:]
  for index in range(len(result)/3):
      dict0 = {}
      dict0["shares"] =  int(result[3*index+1])
      dict0["dividend_ratio"] = float(result[3*index+2])
      my_securities[result[3*index]] = dict0
  return my_securities

def get_my_orders():
  global my_orders
  my_orders = {}
  result = run_command("MY_ORDERS")[0].split()[1:]
  for index in range(len(result)/4):
    dict0 = {}
    dict0[result[4*index]] = {}
    dict0[result[4*index]]["price"] =  float(result[4*index+2])
    dict0[result[4*index]]["shares"] =  float(result[4*index+3])
    my_orders[result[4*index+1]] = dict0
  return  my_orders

def get_securities():
    global securities
    securities = {}
    result = run_command("SECURITIES")[0].split()[1:]

    for index in range(len(result)/4):
        dict0 = {}
        dict0["net_worth"] = float(result[4*index+1])
        dict0["dividend_ratio"] =  float(result[4*index+2])
        dict0["volatility"] =  float(result[4*index+3])

        securities[result[4*index]] = dict0
    return  securities

def get_orders(ticker):
    global securities
    orders = {}
    result = run_command("ORDERS" + " " + ticker)[0].split()[1:]
    orders["ASK"] = []
    orders["BID"] = []
    for index in range(len(result)/4):
        if result[4*index] == "ASK" :
            orders["ASK"].append( {"price": float(result[4*index+2]), "shares": int(result[4*index+3])})
        else:
            orders["BID"].append( {"price": float(result[4*index+2]), "shares": int(result[4*index+3])})
    return  orders


def ask (ticker, price,shares):
    result = run_command("ASK" + " " +  ticker + " "+ str(price) + " " + str(shares))
    if result[0] == "ASK_OUT DONE":
        return 1
    else:
        return 0

def bid(ticker, price,shares):
    result = run_command("BID" + " " +  ticker + " "+ str(price) + " " + str(shares))

    if result[0] == "BID_OUT DONE":
        return 1
    else:
        return 0

def clear_bid(ticker):
    result = run_command("CLEAR_BID" + " " +  ticker)
    if result[0] == "CLEAR_BID_OUT DONE":
        return 1
    else:
        return 0


def clear_ask(ticker):
    result = run_command("CLEAR_ASK" + " " +  ticker)
    if result[0] == "CLEAR_ASK_OUT DONE":
        return 1
    else:
        return 0

def subscribe():
    return run_command("SUBSCRIBE")

def unsubscribe():
    return run_command("UNSUBSCRIBE")

def close_connection():
    return run_command("CLOSE_CONNECTION")



if __name__ == "__main__":
  #print get_my_cash()
  #print get_my_securities()
  print bid("AAPL", 10,10)
  #print bid("AAPL", 2,10)
  bid("CAKE", 1,10)

  #print get_my_orders()
  #print get_securities()
  #print get_orders("AAPL")
  print clear_bid("AAPL")
  print clear_ask("AAPL")
  print bid("AAPL", 5,100000000)
  print get_orders("AAPL")
  print subscribe()
  print unsubscribe()
  print close_connection()
