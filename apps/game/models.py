
from django.db import models

class Game(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="게임명"
    )

    intro = models.TextField(
        verbose_name="게임 소개"
    )

    release_datetime = models.DateTimeField(
        verbose_name="출시일"
    )

    developer = models.CharField(
        max_length=255,
        verbose_name="개발자"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성일시"
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name="삭제여부"
    )

    avg_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name="별점 평균"
    )

    class Meta:
        db_table = 'games'
        verbose_name = '게임'
        verbose_name_plural = '게임 목록'

    def __str__(self):
        return self.name