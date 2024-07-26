from django.shortcuts import render
from .models import *
# Create your views here.

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

global logged_user

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logged_user=user
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_view(request):
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_model = User.objects.create(username=username)
            user_model.set_password(password)
            user_model.save()
            return redirect('login')
        except:
            return render(request, 'register.html', {'error_message': 'Username already exists'})
    return render(request, 'register.html')
    
@login_required
def home(request):
    if request.method=='GET':
        get_all_users = User.objects.exclude(username=request.user.username)
        return render(request, 'home.html', {'users': get_all_users})
    
@login_required
def chat(request, username):
    other_user = get_object_or_404(User, username=username)
    chat_room = ChatRoom.get_or_create_chat_room(request.user, other_user)

    if request.method == 'POST':
        content = request.POST.get('message')
        print("----------",content)
        if content:
            Message.objects.create(
                chat_room=chat_room,
                sender=request.user,
                content=content,
                timestamp=timezone.now()
            )
        return redirect('chat', username=username)

    messages = chat_room.messages.all().order_by('timestamp')
    return render(request, 'chat.html', {
        'chat_room': chat_room,
        'other_user': other_user,
        'messages': messages
    })

# @login_required
# def chat(request, username):
#     if request.method=='GET':
#         user = User.objects.get(username=username)
#         get_all_messages = ChatRoom.objects.filter(user1=request.user,user2=user)
#         return render(request, 'chat.html', {"get_all_messages":get_all_messages,"logged_user":request.user})
#     if request.method=='POST':
#         message = request.POST['message']
#         user = User.objects.get(username=username)
#         chat = Chat.objects.create(username=user, message=message)
#         chatRoom_user = ChatRoom.objects.create(user1=request.user, user2=user)
#         chatRoom_user.message = f"{request.user.username}: {message}"
#         chatRoom_user.save()
#         chat.save()
#         return render(request, 'chat.html', {'username': user})
    # else:
        # get_all_messages = Chat.objects.filter(user=user)
        # print("------", get_all_messages)
        # return render('chat.html')
    
# @login_required
# def one_chat(request,username):


# from .models import ChatRoom

# def get_or_create_chat_room(user1, user2):
#     chat_room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2)
#     if not created:
#         # Ensure user1 is always less than user2 to avoid duplicate rooms
#         chat_room, created = ChatRoom.objects.get_or_create(user1=user2, user2=user1)
#     return chat_room

# def chat_view(request, username):
#     user1 = request.user
#     user2 = get_object_or_404(User, username=username)
#     chat_room = get_or_create_chat_room(user1, user2)
#     # Additional view logic here
#     return render(request, 'chat.html', {'chat_room': chat_room})



