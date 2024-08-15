from django import forms
from .models import Payment, Complaint

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_text']