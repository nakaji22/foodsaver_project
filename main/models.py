from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

CATEGORY_CHOICES = [
    ('MEAT', '肉類'),
    ('VEGE', '野菜'),
    ('DRINK', '飲料'),
    ('DAIRY', '乳製品'),
    ('SNACK', 'お菓子'),
    ('OTHER', 'その他'),
]

class FoodItem(models.Model):
    author= models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    category=models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    purchase_date=models.DateField(default=timezone.now)
    expiration_date=models.DateField()
    price=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #DBやフォームで値が空でもエラーが出ない！
    quantity=models.PositiveIntegerField(default=1) #正の整数
    notes=models.TextField(blank=True, null=True) #メモ欄

    def __str__(self):
        return f"{self.name} ({self.category})"

    def days_left(self):
        return (self.expiration_date - timezone.now().date()).days


