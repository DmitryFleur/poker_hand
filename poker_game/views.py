from rest_framework.views import APIView
from rest_framework.response import Response
from poker_game.utils import is_deck_correct
from poker_game.poker_logic import Game


class CalculateScoreView(APIView):

    def post(self, request):
        cards = request.data.get('cards', None)

        if not cards:
            return Response({'error': True, 'data': 'Cards should be provided'})
        if not is_deck_correct(cards):
            return Response({'error': True, 'data': 'Cards were provided in a wrong format'})

        cards_score = Game(cards).calculate_result()
        return Response({'error': False, 'data': cards_score})
