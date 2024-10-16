from multiprocessing import AuthenticationError
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomerUser

# Create your views here.
def showDemoPage(request):
    return render(request, "home.html" )

def showLogin(request):
    return render(request, "login_page.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            return redirect('home')
        else:
            messages.success(request, ('There was an login'))
            return redirect('login')
    return render(request, 'login.html',{})
def signup(request):
    if(request.method == "POST"):
        fist_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        gender = request.POST['gender']
        user = CustomerUser.objects.create_user(username=username, password=password,user_type = 3 )
        return redirect('login')
    return render(request,'signup.html',{})

def join_course(request, id_course):
    pass
