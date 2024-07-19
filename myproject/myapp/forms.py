"""Module providing all forms."""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Event, Message

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email')
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom '}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom '}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pseudo '}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email '}),
        }
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
            'username': 'Pseudo',
            'email': 'Email',
        }
        help_texts = {
            'username': None,
        }
        error_messages = {
            'username': {
                'required': "Le pseudo est obligatoire.",
                'max_length': 'Le pseudo est trop long',
                'invalid': 'Le pseudo contient des caractères invalides.',
            },
            'email': {
                'required': "L'email est obligatoire.",
                'invalid': 'Veuillez entrer un email correct',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Veuillez renseigner ce champ')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name']
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
            'username': 'Pseudo',
        }
        help_texts = {
            'username': None,
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['sport', 'name', 'date', 'time', 'city', 'price', 'participants_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'évènement'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'id': 'id_date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de l\'évènement'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix de la place'}),
            'participants_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de places'}),
        }
        labels = {
            'sport': 'Sport',
            'name': 'Nom de l\'évènement',
            'date': 'Date',
            'time': 'Heure',
            'city': 'Lieu',
            'price': 'Prix',
            'participants_number': 'Nombre de places',
        }
        error_messages = {
            'sport': {
                'required': 'Veuillez renseigner ce champ',
                'max_length': 'Ce champ ne doit pas dépasser 100 caractères',
            },
            'name': {
                'required': 'Veuillez renseigner ce champ',
                'max_length': 'Ce champ ne doit pas dépasser 100 caractères',
            },
            'date': {
                'required': 'Veuillez renseigner ce champ',
                'invalid': 'Entrez une date valide (YYYY-MM-DD)',
            },
            'time': {
                'required': 'Veuillez renseigner ce champ',
                'invalid': 'Entrez une heure valide (HH:MM)',
            },
            'participants_number': {
                'required': 'Veuillez renseigner ce champ',
                'invalid': 'Entrez un nombre valide',
            },
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Message...'}),
        }