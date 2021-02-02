from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'study'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(),
         name='user_create_done'),
    path('user_create/complete/<token>/',
         views.UserCreateComplete.as_view(), name='user_create_complete'),
]
