import google.generativeai as genai
from django.conf import settings
from django.db import transaction

from apps.ai.exceptions.ai_exceptions import ReviewNotEnough, SummaryGenerationFailed, AIServiceUnavailable
from apps.ai.models import GameReviewSummary
from apps.community.models.reviews import Review
from apps.game.models.game import Game


# Gemini 설정
genai.configure(api_key=settings.GEMINI_API_KEY)


def generate_and_save_summary(game_id: int) -> GameReviewSummary:
    """
    특정 게임의 리뷰를 모아 Gemini로 요약하고, 결과를 DB에 저장합니다.
    """
    # 1. 게임 존재 여부 확인 (Django 기본 에러 활용 또는 Custom Exception)
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        # community 앱의 예외를 재사용하거나 AI 앱용 예외를 따로 만들어도 됩니다.
        from apps.community.exceptions.review_exceptions import GameNotFound
        raise GameNotFound()

    # 2. 리뷰 데이터 조회 (최신 50개)
    reviews = Review.objects.filter(game_id=game_id, is_deleted=False).order_by("-created_at")[:50]

    if not reviews.exists():
        raise ReviewNotEnough()

    # 3. 프롬프트 구성
    review_texts = "\n".join([f"- {r.content} (평점: {r.rating})" for r in reviews])
    prompt = f"""
    다음은 '{game.name}' 게임에 대한 유저 리뷰들입니다.
    이 게임의 주요 장점과 단점을 분석하여 3줄로 명확하게 요약해 주세요.

    [리뷰 데이터]
    {review_texts}
    """

    # 4. Gemini API 호출 및 DB 저장
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if not response.text:
            raise SummaryGenerationFailed()

        # 트랜잭션으로 안전하게 저장
        with transaction.atomic():
            summary_instance = GameReviewSummary.objects.create(
                game=game,
                text=response.text
            )

        return summary_instance

    except Exception as e:
        # 구체적인 로그를 남기는 것이 좋습니다 (logging 모듈 사용 권장)
        print(f"Gemini Error: {e}")
        raise AIServiceUnavailable()
