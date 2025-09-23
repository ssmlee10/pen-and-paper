from django import forms
from .models import Pen, Ink, PenInkLog

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
        attrs={'type': 'date'},
    ),
      'hex_code': forms.TextInput(attrs={'type': 'color'}),
}
    
class PenInkLogForm(forms.ModelForm):
  class Meta:
    model = PenInkLog
    fields = ['ink', 'date_inked']
    widgets = {
        'date_inked': forms.DateInput(attrs={'type': 'date'})
    }