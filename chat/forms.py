from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=100)
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )