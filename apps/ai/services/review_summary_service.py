from django.conf import settings
from apps.community.models.reviews import Review
import openai


def get_review_summary(game_id: int) -> str:
    """
    특정 게임의 리뷰들을 조회하여 AI를 통해 요약본을 생성합니다.
    """
    # 1. 요약할 리뷰 데이터 조회
    reviews = Review.objects.filter(game_id=game_id, is_deleted=False).order_by("-created_at")[:30]

    if not reviews:
        return "작성된 리뷰가 없습니다."

    # 2. 리뷰 텍스트 합치기
    reviews_text = "\n".join([f"- {r.content}" for r in reviews])

    # 3. AI 프롬프트 작성
    prompt = f"""
    아래는 특정 게임에 대한 유저들의 리뷰 모음입니다. 
    이 게임에 대한 유저들의 전반적인 평가를 3줄로 요약해주세요.

    [리뷰 목록]
    {reviews_text}
    """

    # 4. OpenAI API 호출 (예시)
    # 실제 사용 시 settings.OPENAI_API_KEY 등을 설정해야 합니다.
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 게임 리뷰 요약 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        # 로그 기록 등이 필요할 수 있습니다.
        return "요약 서비스를 일시적으로 사용할 수 없습니다."