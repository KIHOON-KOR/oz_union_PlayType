from rest_framework.exceptions import APIException
from rest_framework import status

class AIServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "AI 서비스 연결 상태가 좋지 않습니다. 잠시 후 다시 시도해주세요."
    default_code = "ai_service_unavailable"

class ReviewNotEnough(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "요약할 리뷰 데이터가 부족합니다."
    default_code = "review_not_enough"

class SummaryGenerationFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "리뷰내용을 요약하는 도중 오류가 발생했습니다."
    default_code = "summary_generation_failed"
