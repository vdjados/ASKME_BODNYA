import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент для заполнения данных')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        user_names = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve', 'Frank', 'Grace', 'Hannah', 'Ivy', 'Jack']
        tag_names = ['python', 'django', 'javascript', 'html', 'css', 'react', 'nodejs', 'flask', 'sql', 'linux']

        self.stdout.write(self.style.SUCCESS(f'Создание {ratio} пользователей...'))
        for i in range(ratio):
            username = f'user_{i+1}'
            email = f'user_{i+1}@example.com'
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123'
            )

        self.stdout.write(self.style.SUCCESS(f'Создание {ratio} тегов...'))
        for i in range(ratio):
            tag_name = tag_names[i % len(tag_names)] 
            tag = Tag.objects.create(name=tag_name)

        self.stdout.write(self.style.SUCCESS(f'Создание {ratio * 10} вопросов...'))
        for i in range(ratio * 10):
            user = User.objects.order_by('?').first()  
            title = f'Question {i+1}'
            body = f'This is the body of question {i+1}.'
            question = Question.objects.create(
                title=title,
                body=body,
                user=user
            )

            tags = Tag.objects.order_by('?')[:random.randint(1, 3)]  
            question.tags.set(tags)

        self.stdout.write(self.style.SUCCESS(f'Создание {ratio * 100} ответов...'))
        for i in range(ratio * 100):
            question = Question.objects.order_by('?').first()  
            user = User.objects.order_by('?').first()  
            body = f'This is the body of answer {i+1}.'
            Answer.objects.create(
                question=question,
                body=body,
                user=user
            )

        self.stdout.write(self.style.SUCCESS(f'Создание {ratio * 200} лайков для вопросов...'))
        for i in range(ratio * 200):
            user = User.objects.order_by('?').first() 
            question = Question.objects.order_by('?').first() 
            QuestionLike.objects.get_or_create(user=user, question=question)

        self.stdout.write(self.style.SUCCESS(f'Создание {ratio * 200} лайков для ответов...'))
        for i in range(ratio * 200):
            user = User.objects.order_by('?').first()  
            answer = Answer.objects.order_by('?').first() 
            AnswerLike.objects.get_or_create(user=user, answer=answer)

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))