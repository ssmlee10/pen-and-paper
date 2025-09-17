from django import forms
from .models import Pen, Ink

class PenForm(forms.ModelForm):
  class Meta:
    model = Pen
    exclude = ['user', 'inks']  # hide user & inks
    widgets = {
      'acquired_date': forms.DateInput(
        attrs={'type': 'date'}
  ),
}

class InkForm(forms.ModelForm):
  class Meta:
    model = Ink
    exclude = ['user']
    widgets = {
      'acquired_date': forms.DateInput(
        attrs={'type': 'date'}
    ),
}
