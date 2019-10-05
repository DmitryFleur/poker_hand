import collections

SUIT_LIST = ("Hearts", "Spades", "Diamonds", "Clubs")
NUMERAL_LIST = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace")


class Card:
    def __init__(self, numeral, suit):
        self.numeral = numeral
        self.suit = suit
        self.card = self.numeral, self.suit

    def __str__(self):
        return self.numeral + " " + self.suit


class Game:
    def __init__(self, cards=None):
        self.cards = cards

    @staticmethod
    def create_card(numeral, suit):
        return Card(numeral, suit)

    @staticmethod
    def get_high_card_suit(values):
        if "Ace" in values:
            return "Ace"
        if "King" in values:
            return "King"
        if "Queen" in values:
            return "Queen"
        if "Jack" in values:
            return "Jack"
        values = [int(value) for value in values]
        return str(max(values))

    def combine_deck(self):
        deck = list()
        for card in self.cards:
            card = card.split(' ')
            deck.append(Card(card[0], card[1]))
        return deck

    def calculate_result(self):
        deck = self.combine_deck()
        short_desc = "High card"
        numeral_dict = collections.defaultdict(int)
        suit_dict = collections.defaultdict(int)

        for my_card in deck:
            numeral_dict[my_card.numeral] += 1
            suit_dict[my_card.suit] += 1

        # Pair
        if len(numeral_dict) == 4:
            short_desc = "One pair of %s" % \
                         [k for k, v in numeral_dict.items() if v == max(numeral_dict.values())][0]

        # Two pair or 3-of-a-kind
        elif len(numeral_dict) == 3:
            if 3 in numeral_dict.values():
                short_desc = "Three of a kind % s" % \
                             [k for k, v in numeral_dict.items() if v == 3][0]
            else:
                short_desc = "Two pair"

        # Full house or 4-of-a-kind
        elif len(numeral_dict) == 2:
            if 2 in numeral_dict.values():
                short_desc = "Full house"
            else:
                short_desc = "Four of a kind"
        else:
            # Flushes and straights
            straight, flush = False, False
            if len(suit_dict) == 1:
                flush = True
            min_numeral = min([NUMERAL_LIST.index(x) for x in numeral_dict.keys()])
            max_numeral = max([NUMERAL_LIST.index(x) for x in numeral_dict.keys()])
            if int(max_numeral) - int(min_numeral) == 4:
                straight = True

            # Ace can be low
            low_straight = set(("Ace", "2", "3", "4", "5"))
            if not set(numeral_dict.keys()).difference(low_straight):
                straight = True
            if straight and not flush:
                short_desc = "Straight"
            elif flush and not straight:
                short_desc = "Flush"
            elif flush and straight:
                short_desc = "Straight flush"

        if short_desc == "High card":
            short_desc = "High card of " + self.get_high_card_suit(numeral_dict.keys())

        return short_desc
