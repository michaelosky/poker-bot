import random
import math

random.seed()

card_map = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suit_map = ['c', 'd', 'h', 's']
suit_emoji_map = [':clubs:', ':diamonds:', ':hearts:', ':spades:']
position_map = ['OTB', 'SB', 'BB', 'UTG', 'UTG+1', 'UTG+2', 'UTG+3', 'UTG+4']

def card_value(card_number):
    return card_number % 13

def card_suit(card_number):
    return card_number // 13

def is_pair(card_one, card_two):
    return card_value(card_one) == card_value(card_two)

def is_suited(card_one, card_two):
    return card_suit(card_one) == card_suit(card_two)

def card_number_to_text(card_number):
    return card_map[card_value(card_number)] + suit_emoji_map[card_suit(card_number)]

def deal_two_cards():
    card_one = random.randint(0, 51)
    card_two = card_one
    while card_two == card_one:
        card_two = random.randint(0, 51)

    return card_one, card_two

def deal_two_cards_text():
    card_one, card_two = deal_two_cards()
    return card_number_to_text(card_one) + ' ' + card_number_to_text(card_two)

def get_random_position():
    return random.randint(0,7)

def get_random_position_text():
    random_position = get_random_position()
    return position_map[random_position]

def card_gap(card_one, card_two):
    return abs(card_value(card_one) - card_value(card_two))

# http://www.thepokerbank.com/strategy/basic/starting-hand-selection/chen-formula/

chen_value_map = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 10]
chen_gap_map = [0, -1, -2, -4, -5]
def chen_formula(card_one, card_two):
    value_one = card_value(card_one)
    value_two = card_value(card_two)

    formula_text = ''
    # Step 1 - Base
    higher_value = max(value_one, value_two)
    chen_points = chen_value_map[higher_value]
    formula_text = str(chen_points)

    # Step 2 - Pair
    if is_pair(card_one, card_two):
        chen_points = max(chen_points*2, 5)
        formula_text += '*2'

    # Step 3 - Suited
    if is_suited(card_one, card_two):
        chen_points += 2
        formula_text += '+2'

    # Step 4 - Gap
    gap = card_gap(card_one, card_two)
    gap_penalty = chen_gap_map[min(gap, 4)]
    if gap_penalty:
        chen_points += gap_penalty
        formula_text += str(gap_penalty)

    # Step 5 - Connected Small Cards (< Q)
    if gap == 1 and higher_value < 10:
        chen_points += 1
        formula_text += '+1'

    # Step 6 - Round Up
    return math.ceil(chen_points), formula_text + ' = '
