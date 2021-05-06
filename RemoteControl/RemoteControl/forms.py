from django import forms

from authentication.models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')