from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mistake_count = models.IntegerField(default=0)
    last_mistake_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def no_mistake_days(self):
        if not self.last_mistake_date:
            return 0
        delta = timezone.now().date() - self.last_mistake_date.date()
        return delta.days


class MistakeRecord(models.Model):
    INVESTMENT_TYPES = [
        ('crypto', '币圈'),
        ('stock', 'A股'),
        ('fund', '基金'),
        ('bond', '债券'),
        ('futures', '期货'),
        ('options', '期权'),
        ('real_estate', '房地产'),
        ('other', '其他'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mistake_records')
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPES)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_investment_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"
