from django import forms
from .models import FoodItem

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'expiration_date', 'price', 'quantity', 'notes']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
