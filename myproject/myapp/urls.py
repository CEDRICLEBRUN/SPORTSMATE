from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('account/', views.account, name='account'),
    path('events/list', views.event_list, name='event_list'),
    path('event/detail/<int:event_id>', views.event_detail, name='event_detail'),
    path('events/create', views.create_event, name='create_event'),
    path('events/join/<int:event_id>', views.join_event, name='join_event'),
    path('myevents/', views.my_events, name='my_events'),
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversations/start/', views.start_conversation, name='start_conversation'),
]