import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator
)

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Пароль должен содержать минимум %(min_length)d символов."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Пароль слишком простой и часто используется."),
                code='password_too_common',
            )

class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Пароль не может состоять только из цифр."),
                code='password_entirely_numeric',
            )

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if len(value_part) < 3:
                    continue
                if value_part.lower() in password.lower():
                    raise ValidationError(
                        _("Пароль слишком похож на ваш %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': self.get_verbose_name(attribute_name)},
                    )

    def get_verbose_name(self, attribute_name):
        return {
            'email': 'email',
            'first_name': 'имя',
            'last_name': 'фамилию',
        }.get(attribute_name, attribute_name)