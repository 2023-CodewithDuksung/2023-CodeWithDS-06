from .models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_id', 'nickname', 'email', 'department',)

