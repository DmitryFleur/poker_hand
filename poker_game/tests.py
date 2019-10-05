import json
from django.test import TestCase, Client
from poker_game.poker_logic import Game
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase


class PokerLogicTestCase(TestCase):

    def test_results(self):
        res_true_table = {
            "2 Clubs/Queen Spades/Queen Hearts/7 Diamonds/4 Spades": "One pair of Queen",
            "4 Clubs/8 Hearts/8 Spades/9 Hearts/8 Diamonds": "Three of a kind 8",
            "6 Diamonds/King Diamonds/8 Hearts/4 Hearts/Queen Diamonds": "High card of King",
            "Jack Hearts/5 Spades/10 Diamonds/2 Spades/7 Diamonds": "High card of Jack"
        }
        for data in res_true_table:
            cards = data.split("/")
            game_score = Game(cards).calculate_result()
            self.assertEqual(game_score, res_true_table["/".join(cards)])


class PokerEndpointTestCase(APITestCase):

    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()

    def test_not_list_passed(self):
        payload = {"cards": "some str text"}
        res = self.client.post("/poker/calculate-score/", payload, content_type='application/json')
        res_data = json.loads(res.content)
        self.assertEqual(res_data["error"], True)

    def test_short_list_passed(self):
        payload = {"cards": ["7 Diamonds", "4 Diamonds", "10 Hearts", "3 Clubs"]}
        res = self.client.post("/poker/calculate-score/", payload, content_type='application/json')
        res_data = json.loads(res.content)
        self.assertEqual(res_data["error"], True)
        self.assertEqual(res_data["data"], "Cards were provided in a wrong format")

    def test_no_cards_arg_passed(self):
        payload = {}
        res = self.client.post("/poker/calculate-score/", payload, content_type='application/json')
        res_data = json.loads(res.content)
        self.assertEqual(res_data["error"], True)
        self.assertEqual(res_data["data"], "Cards should be provided")

    def test_happy_flow(self):
        payload = {"cards": ["7 Diamonds", "4 Diamonds", "10 Hearts", "3 Clubs", "10 Spades"]}
        res = self.client.post("/poker/calculate-score/", payload, content_type='application/json')
        res_data = json.loads(res.content)
        self.assertEqual(res_data["error"], False)
        self.assertEqual(res_data["data"], "One pair of 10")
