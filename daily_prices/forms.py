from django import forms
from .models import Price

class PriceFilterForm(forms.Form):
    commodity = forms.ModelChoiceField(queryset=Price.objects.values_list('commodity', flat=True).distinct(), empty_label="Select Commodity", required=False)
    district = forms.ModelChoiceField(queryset=Price.objects.values_list('district', flat=True).distinct(), empty_label="Select District", required=False)
    market = forms.ModelChoiceField(queryset=Price.objects.values_list('market', flat=True).distinct(), empty_label="Select Market", required=False)
    date = forms.DateField(widget=forms.SelectDateWidget, label="Select Date", required=False)