from django import forms
from questions.models import Question, Tag, Answer
from django.contrib import auth
from django.contrib.auth.models import User

# Функция добавляющая css классы к полям формы
def css_classes(form):
    for field in form:
        if isinstance(field.field.widget, (forms.TextInput, forms.PasswordInput, forms.Textarea)):
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
        super(SignUpForm, self).__init__(*args, **kwargs)
        css_classes(self)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(u'Пользователь с таким логином уже есть.', code='username_exist')
        return self.cleaned_data['username']

    def clean_password(self):
        if len(self.cleaned_data['password']) < 3:
            raise forms.ValidationError(u'Пароль должен быть не меньше 6 символов.', code='len_password')
        return self.cleaned_data['password']

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError(u'Повторный пароль не совпал.', code='repeat_password')

    def save(self):
        user_kw = self.cleaned_data
        user = User.objects.create_user(user_kw['username'], password=user_kw['password'], email=user_kw['email'])
        user.profile.nick_name = user_kw['nick_name']
        if user_kw['avatar']:
            user.profile.avatar = user_kw['avatar']
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Пароль')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        css_classes(self)

    def clean(self):
        user = self.auth()
        if not user:
            raise forms.ValidationError(u'Неправильный логин или пароль.', code='auth')

    def auth(self):
        return auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])


class UserSettingsForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    nick_name = forms.CharField(max_length=20, label='Ник',
                                help_text='Будет отображаться в вопросахи и ответах. Ник должен быть меньше 20 символов.')
    avatar = forms.ImageField(widget=forms.FileInput, label='Аватар', required=False)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        css_classes(self)

    def save(self):
        user_kw = self.cleaned_data
        self._user.email = user_kw['email']
        self._user.profile.nick_name = user_kw['nick_name']
        if user_kw['avatar']:
            self._user.profile.avatar = user_kw['avatar']
        self._user.save()


class AskForm(forms.Form):
    title = forms.CharField(max_length=200, label='Заголовок вопроса',
                            help_text='Вопрос должен быть меньше 100 символов, и оканчиваться знаком вопроса "?".')
    text = forms.CharField(widget=forms.Textarea, label='Текст вопроса',
                           help_text='Здесь можно указать описание Вашего вопроса.')
    tags = forms.CharField(max_length=50, label='Теги к вопросу',
                           help_text='Вы можете к вопросу добавить до трёх тегов. Вводить через запятую ",".')

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)
        css_classes(self)

    def clean_tags(self):
        tags = self.cleaned_data['tags'].split(',')
        if len(tags) > 3:
            raise forms.ValidationError(u'Максимум 3 тега.', code='tags_count')
        return tags

    def save(self):
        tag_names = self.cleaned_data['tags']
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        q = Question.objects.create(title=self.cleaned_data['title'], text=self.cleaned_data['text'], user=self._user)
        for tag in tags:
            q.tags.add(tag)
        return q


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Напишите Ваш ответ здесь...', 'rows': 4}),
                           label='')

    def __init__(self, user, question, *args, **kwargs):
        self._user = user
        self._question = question
        super(AnswerForm, self).__init__(*args, **kwargs)
        css_classes(self)

    def clean(self):
        if not self._user.is_authenticated():
            raise forms.ValidationError(u'Необходимо авторизоваться.', code='auth')

    def save(self):
        ans = Answer.objects.create(text=self.cleaned_data['text'], user=self._user, question=self._question)
        return ans
