from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home_user(request):
    return render(request, 'logreg_app/index.html')

def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'logreg_app/dashboard.html', {'fname':fname})
        else:
            messages.error(request, "Username or Password Not Correct!")
            return redirect('home')

    return render(request, 'logreg_app/login.html')

def register_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try other username!")
            return redirect('register')
    
        if User.objects.filter(email=email):
            messages.error(request, "email already register")
            return redirect('register')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 character")
            return redirect('register')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!!!")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('register')



        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname

        user.save()

        messages.success(request, "Your Account have been successfully created!!!")

        return redirect("login")

    return render(request, 'logreg_app/register.html')

# def dashboard_user(request):
#     return render(request, 'logreg_app/dashboard.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You are Successfully Logged Out!!!")
    return redirect('home')
    #return render(request, 'logreg_app/logout.html')
