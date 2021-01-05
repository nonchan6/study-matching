from django.urls import path
from . import views

app_name='study'

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('signup', views.signup, name='signup'),
    path('update/<int:num>', views.update, name='update'),
    path('delete/<int:num>', views.delete, name='delete'),
]