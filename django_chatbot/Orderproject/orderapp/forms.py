from django import forms
from . models import OrderDetails


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        models = OrderDetails
        fields = ('Name', 'Mobile_no', 'Address')
