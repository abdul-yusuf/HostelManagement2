from django import forms
from .models import Payment, Complaint, User as CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth import get_user_model

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_text']


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password',)

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        # cleaned_email = self.clean_email()

        # password = cleaned_data.get("password")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user