from django import forms
from .models import FoodItem
from .models import CATEGORY_CHOICES

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'expiration_date', 'price', 'quantity', 'notes']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FoodSearchForm(forms.Form):
    name = forms.CharField(label='食材名（部分一致）', required=False) #required=Falseで入力を任意にする
    category = forms.ChoiceField(label='カテゴリ', choices=[('', 'すべて')] + CATEGORY_CHOICES, required=False)
    max_days_left = forms.IntegerField(label='消費期限があと○日以内', required=False, min_value=0)
    max_price = forms.DecimalField(label='価格が○円以下', required=False, min_value=0, decimal_places=2)
