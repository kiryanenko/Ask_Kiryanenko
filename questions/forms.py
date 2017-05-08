from django import forms
from questions.models import Profile, Question, Tag


# Функция добавляющая css классы к полям формы
def css_classes(form):
    for field in form:
        if isinstance(field.field.widget, (forms.TextInput, forms.PasswordInput)):
            field.field.widget.attrs['class'] = 'form-control'


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логин',
                            help_text='Логин должен быть меньше 20 символов, и состоять только из латинских смиволов.')
    email = forms.EmailField(label='E-mail')
    nick_name = forms.CharField(max_length=20, label='Ник',
                                help_text='Будет отображаться в вопросахи и ответах. Ник должен быть меньше 20 символов.')
    password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Пароль',
                               help_text='Пароль должен быть не меньше 6 символов.')
    repeat_password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Повтор пароля')
    avatar = forms.ImageField(label='Аватар', required=False)

    def __init__(self, *args, **kwargs):
        print(kwargs)
        super(SignUpForm, self).__init__(*args, **kwargs)
        css_classes(self)

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            raise forms.ValidationError(
                u'Повторный пароль не совпал'
            )

    def save(self):
        user_kwargs = self.cleaned_data
        del user_kwargs['repeat_password']
        user = Profile(**user_kwargs)
        user.save()
        return user
