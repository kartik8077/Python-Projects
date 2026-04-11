#
# MENU = {
#     "espresso": {
#         "ingredients": {
#             "water": 50,
#             "coffee": 18,
#         },
#         "cost": 1.5,
#     },
#     "latte": {
#         "ingredients": {
#             "water": 200,
#             "milk": 150,
#             "coffee": 24,
#         },
#         "cost": 2.5,
#     },
#     "cappuccino": {
#         "ingredients": {
#             "water": 250,
#             "milk": 100,
#             "coffee": 24,
#         },
#         "cost": 3.0,
#     }
# }
#
# profit = 0
# resources = {
#     "water": 300,
#     "milk": 200,
#     "coffee": 100,
# }
#
#
# def is_resource_sufficient(order_ingredients):
#     """Returns True when order can be made, False if ingredients are insufficient."""
#     for item in order_ingredients:
#         if order_ingredients[item] > resources[item]:
#             print(f"Sorry there is not enough {item}.")
#             return False
#     return True
#
#
# def process_coins():
#     """Returns the total calculated from coins inserted."""
#     print("Please insert coins.")
#     total = int(input("how many quarters?: ")) * 0.25
#     total += int(input("how many dimes?: ")) * 0.1
#     total += int(input("how many nickles?: ")) * 0.05
#     total += int(input("how many pennies?: ")) * 0.01
#     return total
#
#
# def is_transaction_successful(money_received, drink_cost):
#     """Return True when the payment is accepted, or False if money is insufficient."""
#     if money_received >= drink_cost:
#         change = round(money_received - drink_cost, 2)
#         print(f"Here is ${change} in change.")
#         global profit
#         profit += drink_cost
#         return True
#     else:
#         print("Sorry that's not enough money. Money refunded.")
#         return False
#
#
# def make_coffee(drink_name, order_ingredients):
#     """Deduct the required ingredients from the resources."""
#     for item in order_ingredients:
#         resources[item] -= order_ingredients[item]
#     print(f"Here is your {drink_name} ☕️. Enjoy!")
#
#
# is_on = True
#
# while is_on:
#     choice = input("What would you like? (espresso/latte/cappuccino): ")
#     if choice == "off":
#         is_on = False
#     elif choice == "report":
#         print(f"Water: {resources['water']}ml")
#         print(f"Milk: {resources['milk']}ml")
#         print(f"Coffee: {resources['coffee']}g")
#         print(f"Money: ${profit}")
#     else:
#         drink = MENU[choice]
#         if is_resource_sufficient(drink["ingredients"]):
#             payment = process_coins()
#             if is_transaction_successful(payment, drink["cost"]):
#                 make_coffee(choice, drink["ingredients"])
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import time
import sys

# Optional: Using simple ANSI escape codes for colors
# \033[92m = Green, \033[93m = Yellow, \033[91m = Red, \033[0m = Reset
G = "\033[92m"
Y = "\033[93m"
R = "\033[91m"
C = "\033[96m"
RES = "\033[0m"

MENU = {
    "espresso": {"ingredients": {"water": 50, "coffee": 18}, "cost": 1.5},
    "latte": {"ingredients": {"water": 200, "milk": 150, "coffee": 24}, "cost": 2.5},
    "cappuccino": {"ingredients": {"water": 250, "milk": 100, "coffee": 24}, "cost": 3.0}
}

profit = 0
resources = {"water": 300, "milk": 200, "coffee": 100}


def loading_bar(action):
    """Adds a cool animated progress bar."""
    print(f"{Y}{action}{RES}", end="")
    for _ in range(10):
        time.sleep(0.2)
        print(f"{G}█{RES}", end="", flush=True)
    print("\n")


def is_resource_sufficient(order_ingredients):
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"{R}❌ Sorry, there is not enough {item}.{RES}")
            return False
    return True


def process_coins():
    print(f"{C}💳 Please insert coins.{RES}")
    try:
        total = int(input("  Quarters: ")) * 0.25
        total += int(input("  Dimes:    ")) * 0.10
        total += int(input("  Nickels:  ")) * 0.05
        total += int(input("  Pennies:  ")) * 0.01
        return total
    except ValueError:
        print(f"{R}Invalid input. Refunding...{RES}")
        return 0


def is_transaction_successful(money_received, drink_cost):
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        if change > 0:
            print(f"{G}💰 Here is ${change} in change.{RES}")
        global profit
        profit += drink_cost
        return True
    else:
        print(f"{R}⚠️  Not enough money. ${money_received} refunded.{RES}")
        return False


def make_coffee(drink_name, order_ingredients):
    loading_bar(f"Grinding beans for {drink_name}... ")
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"✨ {G}Here is your {drink_name.title()} ☕. Enjoy!{RES}\n")


# --- UI Header ---
print(f"""{C}
  ____________________________
 (                            )
  )  WELCOME TO PYTHON CAFE  (
 (____________________________)
{RES}""")

is_on = True

while is_on:
    choice = input(f"{Y}What would you like? (espresso/latte/cappuccino/report/off): {RES}").lower()

    if choice == "off":
        print(f"{R}Shutting down... Goodbye!{RES}")
        is_on = False
    elif choice == "report":
        print(f"\n{C}--- MACHINE STATUS ---")
        print(f"💧 Water:  {resources['water']}ml")
        print(f"🥛 Milk:   {resources['milk']}ml")
        print(f"🫘 Coffee: {resources['coffee']}g")
        print(f"💵 Profit: ${profit}{RES}\n")
    elif choice in MENU:
        drink = MENU[choice]
        if is_resource_sufficient(drink["ingredients"]):
            payment = process_coins()
            if is_transaction_successful(payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])
    else:
        print(f"{R}Invalid selection. Please try again.{RES}")