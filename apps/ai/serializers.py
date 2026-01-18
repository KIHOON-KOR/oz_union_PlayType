from rest_framework import serializers
from apps.ai.models import GameReviewSummary

class GameReviewSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameReviewSummary
        fields = [
            "id",
            "game_id",
            "text",
            "created_at"
        ]

