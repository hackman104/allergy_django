from django import forms

from allergies.models import Request

class RequestForm(forms.ModelForm):
    """Form for user to add request"""
    request_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter restaurant name here', 'autofocus': ''})
    )
    request_link = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter link to allergy guide here (optional)'})
    )
    class Meta:
        model = Request
        fields = ['request_name', 'request_link']