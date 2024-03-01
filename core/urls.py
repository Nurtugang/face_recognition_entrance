from django.urls import path,include
from .views import *


urlpatterns = [
    path('',mainpage, name = 'mainpage'),
    path('index/', index, name= 'index'),
    path('ajax/', ajax, name= 'ajax'),
    path('scan/',scan,name='scan'),
 

    path('register/', register, name='register'),
    path('login/', login, name = 'login'),


]
