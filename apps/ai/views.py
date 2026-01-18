from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema

from apps.ai.services import generate_and_save_summary
from apps.ai.serializers import GameReviewSummarySerializer


class GameReviewSummaryAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=["AI 요약"],
        summary="게임 리뷰 AI 요약 생성 및 저장",
        responses={201: GameReviewSummarySerializer},
    )
    def post(self, request, game_id):
        """
        특정 게임의 리뷰를 요약하여 저장하고 반환합니다.
        POST 요청을 사용하는 이유는 서버 상태(DB)를 변경(저장)하기 때문입니다.
        """
        summary_instance = generate_and_save_summary(game_id=game_id)

        serializer = GameReviewSummarySerializer(summary_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ------------------------------------------------------------------------------
# [코드 설명]
# 1. POST Method: 요약문을 '생성'하고 '저장'하는 작업이므로 GET보다는 POST가 적합합니다.
#    (만약 단순히 조회만 하고 저장하지 않는다면 GET을 씁니다.)
# 2. Response: 저장된 모델 객체를 시리얼라이저를 통해 JSON으로 변환하여 반환합니다.
# ------------------------------------------------------------------------------