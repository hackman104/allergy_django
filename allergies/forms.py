from django import forms

from .models import Request

class RequestForm(forms.ModelForm):
    """Form for user to add request"""
    class Meta:
        model = Request
        fields = ['request_name', 'request_link']