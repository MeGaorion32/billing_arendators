from django.db.models import Q
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User
from apartments.models import Apartment

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
        help_text=_("""
            <ul class="text-muted">
                <li>Пароль должен содержать минимум 8 символов</li>
                <li>Не может быть полностью числовым</li>
                <li>Не должен быть слишком простым или распространенным</li>
                <li>Не должен совпадать с вашими личными данными</li>
            </ul>
        """),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
        strip=False,
    )
    role = forms.ChoiceField(
        label=_("Роль"),
        choices=User.Role.choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=User.Role.CLIENT
    )
    first_name = forms.CharField(
        label=_("Имя"),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    patronymic = forms.CharField(
        label=_("Отчество"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label=_("Телефон"),
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label=_("Адрес"),
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'role', 
                 'first_name', 'last_name', 'patronymic', 
                 'phone', 'address']
        widgets = {
            'role': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request and self.request.user.is_client:
            self.fields['role'].initial = User.Role.RENTER
            self.fields['role'].widget = forms.HiddenInput()
            
            # Добавляем поле для выбора объектов
            self.fields['apartments'] = forms.ModelMultipleChoiceField(
                queryset=Apartment.objects.filter(owner=self.request.user, renter__isnull=True),
                widget=forms.CheckboxSelectMultiple,
                required=True,
                label=_('Объекты для арендатора')
            )

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'phone', 'address', 'role']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        is_admin = kwargs.pop('is_admin', False)
        super().__init__(*args, **kwargs)
        
        if not is_admin:
            self.fields['role'].required = False
            self.fields['role'].widget = forms.HiddenInput()
        
        # Добавляем поле apartments если это арендатор
        if self.instance.is_renter:
            if is_admin:
                queryset = Apartment.objects.filter(Q(renter__isnull=True) | Q(renter=self.instance))
                required = False
            else:
                queryset = Apartment.objects.filter(
                    # owner=self.request.user,
                    # renter__isnull=True | Q(renter=self.instance)
                     Q(owner=self.request.user) &
                    (Q(renter__isnull=True) | Q(renter=self.instance))
                )
                required = True

            self.fields['apartments'] = forms.ModelMultipleChoiceField(
                queryset=queryset,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                required=required,
                label=_('Привязанные объекты'),
                initial=self.instance.rented_apartments.all()
            )

      

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # email = forms.EmailField(label=_('Email'))
    # password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)