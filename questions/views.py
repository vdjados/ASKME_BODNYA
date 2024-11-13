from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Question, Answer, Tag
from django.db.models import Count
from .utils import paginate

def index(request):
    query = request.GET.get('q', '')
    if query:
        questions = Question.objects.search(query) 
    else:
        questions = Question.objects.get_newest() 
    page_obj = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': page_obj.object_list,
        'page_obj': page_obj,  
        'query': query
    })

def hot(request):
    questions = Question.objects.get_hot() 
    page_obj = paginate(questions, request)
    return render(request, 'hot.html', {'questions': page_obj.object_list, 'page_obj': page_obj})

def tag_questions(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.get_by_tag(tag_name)
    return render(request, 'tag_questions.html', {'tag': tag, 'questions': questions})

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers.all()
    return render(request, 'question_detail.html', {'question': question, 'answers': answers})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def ask_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        tags = request.POST.getlist('tags')  
        user = request.user
        question = Question.objects.create(title=title, body=body, user=user)
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)
        return redirect('index')
    else:
        return render(request, 'ask.html')