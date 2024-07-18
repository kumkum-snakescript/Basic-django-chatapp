from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_view, name='login'),
    path('home/logout/', views.logout_view, name='logout'),
    path('home/<str:username>/chat/',views.chat, name='chat'),
    path('register/', views.register_view, name='register'),
    # add other URLs here
]
