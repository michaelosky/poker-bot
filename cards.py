import random

random.seed()

card_map = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suit_map = ['c', 'd', 'h', 's']
suit_emoji_map = [':clubs:', ':diamonds:', ':hearts:', ':spades:']
position_map = ['OTB', 'SB', 'BB', 'UTG', 'UTG+1', 'UTG+2', 'UTG+3', 'UTG+4']

def card_number_to_text(card_number):
    return card_map[card_number % 13] + suit_emoji_map[card_number // 13]

def is_pair(card_one, card_two):
    return abs(card_one - card_two) % 13 == 0

def is_suited(card_one, card_two):
    return abs(card_one - card_two) < 13

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