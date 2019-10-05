from poker_game.poker_logic import SUIT_LIST, NUMERAL_LIST


def is_deck_correct(cards):
    if not isinstance(cards, list):
        return False

    if len(cards) != 5:
        return False

    for card in cards:
        card_data = card.split(" ")
        if card_data[0] not in NUMERAL_LIST or card_data[1] not in SUIT_LIST:
            return False

    return True
