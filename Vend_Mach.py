
'''My goal for this program is to show that Python is simple enough
   for even a very beginner at programming to read and understand
   useful programs.

   Note: Floating point numbers are not used due to possible rounding 
         errors.  All monetary values are in cents.

'''

# Functions used by the machine
def sum_of_coins (coins) :
  "Returns the value of the list of coins"
  total = 0
  for coin in coins:
    if coin == "NICKEL":
      total = total + 5
    elif coin == "DIME":
      total = total + 10
    elif coin == "QUARTER":
      total = total + 25
    else:
      total = total + 100
  return total

def return_coin (coin) :
  "used by make_change to return a coin if possible"
  if coin_bank[coin] > 0:
    print "Return coin -", coin
    coin_bank[coin] -= 1           # decrement the number we have
    return True
  else:
    return False

def make_change (amount):
  "Returns change after a purchase"
  remaining_change = amount
  while remaining_change > 0:
    if remaining_change >= 100 and return_coin("DOLLAR"):
      remaining_change -= 100
      continue
    elif remaining_change >= 25 and return_coin("QUARTER"):
      remaining_change -= 25
      continue
    elif remaining_change >= 10 and return_coin("DIME"):
      remaining_change -= 10
      continue
    elif remaining_change >= 5 and return_coin("NICKEL"):
      remaining_change -= 5
      continue
    else:
      # we have no change to give, just ignore
      return
    
def get_coin (coin) :
  "used by SERVICE to prompt for number of coins"
  number = coin_bank[coin]
  while True:
    raw_value = raw_input("Enter number of "+coin+"s ["+str(number)+"]:")
    if not raw_value:
      return number
    elif raw_value.isdigit():
      return int(raw_value)
    else:
      print "You must enter a number"

def get_product (product):
  "used by SERVICE to prompt for number and price of product"
  number, price = products[product]
  while True:
    raw_value = raw_input("Enter number of " + product +
                          " products ["+str(number)+"]:") 
    if not raw_value:
      number_of_product = number
      break
    elif raw_value.isdigit():
      number_of_product = int(raw_value)
      break
    else:
      print "You must enter a number"
  while True:
    raw_value = raw_input("Enter price of product " + product + 
                          " in cents ["+str(price)+"]:") 
    if not raw_value:
      price_of_product = price
      break
    elif raw_value.isdigit():
      price_of_product = int(raw_value)
      break
    else:
      print "You must enter a number"
  return number_of_product, price_of_product

# Words recognized by this vending machine
valid_words = [ "NICKEL", "DIME", "QUARTER", "DOLLAR", 
                "GET-A", "GET-B", "GET-C", 
                "COIN RETURN", "SERVICE", "QUIT" ]

# How many of each coin do we have initially (can be changed by service)
coin_bank = { "NICKEL":20, "DIME":20, "QUARTER":20, "DOLLAR":20 }

# How many of each product do we have initially (can be changed by service)
# and how much does the product cost - product:(quantity, cost)
products = { "A":(5, 65), "B":(5, 100), "C":(5, 150) }

# Start of main code
print "Lambda Lounge Vending Machine"
coins = []
while True:
  input = raw_input(">")          # accept only one word at a time
  # the ability to accecpt lower case and quit are for convenience
  input = input.upper()
  if input not in valid_words:
    print "Unrecognized word"
    continue                      # go back to top of while loop
  if input == "QUIT":
    break

  if input in [ "NICKEL", "DIME", "QUARTER", "DOLLAR" ]:
    coins.append(input)
    print "$%4.2f" % (float(sum_of_coins(coins))/100.0)

  if input == "COIN RETURN":
    for coin in coins:
      print "Return coin -", coin
    coins = []

  if input in [ "GET-A", "GET-B", "GET-C" ]:
    product = input[-1]           # the last letter is the product

    # check if we have any of this product left
    if products[product][0] == 0:
      print "Sold out"
      continue

    # check if we have enough money for this product
    collected = sum_of_coins(coins)
    if collected < products[product][1]:
      print "Deposit $%4.2f" % (float(products[product][1] - collected)/100.0) 
      continue

    # we have product and enough money, complete the transaction
    # put the coins into our coin bank
    for coin in coins:
      coin_bank[coin] += 1        # increment the quantity
    coins = []
    # dispense the product
    print "Dispense product -", product
    # decrement the quantity
    products[product] = (products[product][0]-1, products[product][1])
    # check if we owe change
    if  collected > products[product][1]:
      make_change( collected - products[product][1] )

  if input == "SERVICE":
    print "Service mode"
    for coin in [ "NICKEL", "DIME", "QUARTER", "DOLLAR" ]:
      coin_bank[coin] = get_coin(coin)
    for product in [ "A", "B", "C" ]:
      products[product] = get_product(product)
    print "Service complete"

