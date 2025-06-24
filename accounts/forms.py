from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(
        choices=[('guest', 'Guest'), ('landlord', 'Landlord')],
        initial='guest',
        required=False
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.role = self.cleaned_data.get("role", "guest")
        if commit:
            user.save()
        return user
