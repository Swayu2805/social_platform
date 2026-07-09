from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('bio', 'profile_pic', 'cover_photo', 'location', 'date_of_birth', 'is_private')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'maxlength': 500}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
