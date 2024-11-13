from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class QuestionManager(models.Manager):
    def search(self, query):
        return self.filter(
            Q(title__icontains=query) | 
            Q(body__icontains=query) | 
            Q(tags__name__icontains=query)
        ).distinct()

    def get_newest(self):
        return self.order_by('-created_at') 

    def get_hot(self):
        return self.order_by('-views') 

    def get_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).distinct()

    def get_question_with_answers(self, question_id):
        return self.prefetch_related('answers').get(pk=question_id)

class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name='questions')
    views = models.PositiveIntegerField(default=0)

    objects = QuestionManager()

    def get_absolute_url(self):
        return f"/question/{self.id}/"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to: {self.question.title}"

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question') 

    def __str__(self):
        return f"{self.user.username} likes {self.question.title}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user.username} likes answer to: {self.answer.question.title}"

