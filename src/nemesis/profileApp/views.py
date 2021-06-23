from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, HttpResponse
from profileApp.forms import UserForm
from django.contrib import messages
from .models import User
import jwt, json

# Create your views here.
def signUpView(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            messages.success(request, "new user registered")
            return redirect('/login')
        else:
            return render(request, 'signup.html', {'userform': userform})
    userform = UserForm()
    return render(request, 'signup.html', {'userform': userform})


def loginView(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            payload = {
                'username': username,
            }
            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
            current_user = User.objects.get(username=username)
            current_user.token = jwt_token["token"]
            current_user.save()
            return redirect(f'/edit/{jwt_token["token"]}')
        else:
            errors = "invalid login details"
            return render(request, 'login.html', {'errors':errors})


    return render(request, 'login.html')

def editView(request, token):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.token == token:
            return render(request, "edit.html", {'username' : current_user.username, 'email': current_user.email, 'address': current_user.address, 'token':token})
        else:
            return HttpResponse("authentification failed")
    else:
        return redirect('/login')
    

def updateView(request, field):
    if request.method == "POST" and request.user.is_authenticated:
        current_username = request.user.username
        current_user = User.objects.get(username=current_username)
        token = request.POST['token']
        if current_user.token == token:
            value = request.POST['value']
            if field == "username":
                current_user.username = value
            elif field == "email":
                current_user.email = value
            elif field == "address":
                current_user.address = value
            current_user.save()
            return redirect(f'/edit/{token}')
        else:
            return HttpResponse("authentification failed")
    else:
        return HttpResponse("no access")

def logoutView(request):
    logout(request)
    return redirect('/login')