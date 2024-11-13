from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('hot/', views.hot, name='hot'), 
    path('tag/<str:tag_name>/', views.tag_questions, name='tag_questions'),  
    path('question/<int:question_id>/', views.question_detail, name='question_detail'), 
    path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'), 
    path('ask/', views.ask_view, name='ask'),
]
