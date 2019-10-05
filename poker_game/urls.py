from django.urls import path
from poker_game.views import CalculateScoreView

urlpatterns = [
    path('calculate-score/', CalculateScoreView.as_view())
]
