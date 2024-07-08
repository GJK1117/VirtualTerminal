from django.db import models

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100)    # 제한된 문자열 필드 타입
    content = models.TextField()                # 대용량 문자열 필드 타입
    created_at = models.DateTimeField(auto_now_add=True)    # 날짜와 시간을 저장하는 필드 타입
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title