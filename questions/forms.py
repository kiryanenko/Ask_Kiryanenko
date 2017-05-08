from django import forms


class SignUp(forms.Form):
    login = forms.CharField(max_length=20, label='Логин',
                            help_text='Логин должен быть меньше 20 символов, и состоять только из латинских смиволов')
    email = forms.EmailField(label='E-mail')
    nick_name = forms.CharField(max_length=20, label='Ник')
    password = forms.CharField(max_length=50, label='Пароль')
    repeat_password = forms.CharField(max_length=50, label='Повтор пароля')
    avatar = forms.ImageField(label='Аватар', required=False)

    def clean(self):
        if self.password != self.repeat_password:
            raise forms.ValidationError(
                u'Повторный пароля не совпал'
            )
