from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError

User = get_user_model()


class BicoAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "field", "autocomplete": "email", "placeholder": "voce@exemplo.com"}
        ),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "field", "autocomplete": "current-password", "placeholder": "Sua senha"}
        ),
    )

    def clean_username(self):
        email = self.cleaned_data["username"].strip()
        return User.objects.normalize_email(email)


class AccountCreationForm(UserCreationForm):
    name = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "field",
                "autocomplete": "name",
                "placeholder": "Como podemos chamar você?",
            }
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "field", "autocomplete": "email", "placeholder": "voce@exemplo.com"}
        ),
    )
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "field",
                "autocomplete": "new-password",
                "placeholder": "Crie uma senha",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "field",
                "autocomplete": "new-password",
                "placeholder": "Digite a senha novamente",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("name", "email")

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise ValidationError("Informe seu nome.")
        return name

    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data["email"])
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já possui uma conta. Entre ou recupere sua senha.")
        return email


class AccountProfileForm(forms.ModelForm):
    name = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "field", "autocomplete": "name"}),
    )

    class Meta:
        model = User
        fields = ("name",)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise ValidationError("Informe seu nome.")
        return name


class BicoPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha atual",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "field", "autocomplete": "current-password"}),
    )
    new_password1 = forms.CharField(
        label="Nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "field", "autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "field", "autocomplete": "new-password"}),
    )


class BicoPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="E-mail da sua conta",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "field", "autocomplete": "email", "placeholder": "voce@exemplo.com"}
        ),
    )

    def clean_email(self):
        return User.objects.normalize_email(self.cleaned_data["email"])


class BicoSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "field", "autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "field", "autocomplete": "new-password"}),
    )
