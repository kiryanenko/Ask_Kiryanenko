# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from questions.models import User, Question, Tag, Answer, QuestionLike, AnswerLike
import random
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создание пользователей
        for i in range(0, 30):
            user = User.objects.create_user(
                random.choice(
                    ["kiryanenko", "alex", "username", "sidor", "krot", "qwerty", "samsa", 'super', 'hitryy', 'grenom']
                ) + str(i) + '_' + str(time.time()),
                password="123456",
                email=str(i) + '_' + str(time.time()) + random.choice(
                    ["kiryanenkoav@mail.ru", "alex@mail.ru", "petrov@mail.ru", "qwerty@mail.ru", "krot@mail.ru"]
                )
            )
            user.profile.nick_name = random.choice(
                    ["kiryanenko", "alex", "username", "sidor", "krot", "qwerty", "samsa", 'super', 'hitryy', 'grenom']
                )
            user.save()
        users = User.objects.all()

        # Создание тегов
        for i in range(0, 30):
            try:
                Tag(name=random.choice(
                    ["XML", "JSON", "Python", "C#", "C++", "Ruby", "Ruby on Rails", "Django", "CSS", "HTML", "Perl"]
                )).save()
            except Exception:
                pass
        tags = Tag.objects.all()

        # Создание вопросов
        for i in range(0, 50):
            q = Question(
                title=str(i) + '_' + str(time.time()) + ' ' + random.choice(
                    ["Не работает регулярка в PHP в многострочном режиме",
                     "В заданном тексте в конце каждого слова добавить первый символ этого слова",
                     "Замена текста js",
                     "И опять, как всё-таки запустить приложение вне QT?",
                     "jquery и bootstrap",
                     "Плавная смена background-image",
                     "Помогите запустить проект. модуль navigator не видит модуль core. maven",
                     "Не работает функция, в чем может быть ошибка?"]
                ),
                text=random.choice(
                    ["Не работает регулярка в PHP в многострочном режиме ",
                     "В заданном тексте в конце каждого слова добавить первый символ этого слова ",
                     "Пытаюсь конвертировать python в exe с помощью pyinstaller, раньше проблем с ним не было... ",
                     "И опять, как всё-таки запустить приложение вне QT? ",
                     "Имеется проблема с получением списка файлов. Функция выполняется. Но на определенном моменте... ",
                     "Есть desktop приложение на java, делаю функцию сохранения... ",
                     "Помогите запустить проект. модуль navigator не видит модуль core. maven ",
                     "Не работает функция, в чем может быть ошибка? "]
                ) * random.randint(1, 20),
                user=random.choice(users),
            )
            q.save()
            for _ in range(0, random.randint(0, 3)):
                q.tags.add(random.choice(tags))
        questions = Question.objects.all()

        # Создание ответов
        for i in range(0, 100):
            Answer(
                text=random.choice(
                    ["Похоже здесь неправильно указано имя файла ifstream sf(Students);, а потому файл не открыт. ",
                     "В настройках проекта указать, чтобы запуск был с другой формы. ",
                     "Вы можете использовать VS для разработки приложений на C++ под андроид. ",
                     "У вас остались записи в базе Windows Installer. Первое что вам нужно это выяснить код продукта. ",
                     "Имеется проблема с получением списка файлов. Функция выполняется. Но на определенном моменте... ",
                     "Решается всё очень просто, но нудно. В реестре вбиваешь в поиск 14 и удаляешь всё, кроме офиса. ",
                     "Есть Visual Studio Tools for Apache Cordova - поддерживаются платформы Android, Windows, wp8. ",
                     "Есть ограничение на контролы андроидовские, которые можно использовать в виджете... "]
                ) * random.randint(1, 15),
                question=random.choice(questions),
                user=random.choice(users)
            ).save()
        answers = Answer.objects.all()

        # Создание лайков вопросов
        for _ in range(0, 200):
            like = QuestionLike(
                question=random.choice(questions),
                user=random.choice(users),
                is_like=bool(random.randint(0, 1))
            )
            like.save()
            if like.is_like:
                like.question.rating += 1
            else:
                like.question.rating -= 1
            like.question.save()

        # Создание лайков ответов
        for _ in range(0, 200):
            like = AnswerLike(
                answer=random.choice(answers),
                user=random.choice(users),
                is_like=bool(random.randint(0, 1))
            )
            like.save()
            if like.is_like:
                like.answer.rating += 1
            else:
                like.answer.rating -= 1
            like.answer.save()
