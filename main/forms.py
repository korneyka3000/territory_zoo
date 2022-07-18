from django import forms
from main.models import Consultation


class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ('name', 'phone')

