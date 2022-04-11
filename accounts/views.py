from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def signupaccount(request):
  if request.method == 'GET':
    return render(request, 'signupaccount.html', {'form': UserCreateForm})
  else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(request.POST['username'], 
                password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('home')
      except IntegrityError:
        return render(request, 'signupaccount.html', {'form':UserCreateForm, 
                              'error':'Username already taken. Choose new username.'})
    else:
      return render(request, 'signupaccount.html', {'error': 'Passwords to not match'})


@login_required
def logoutaccount(request):        
    logout(request)
    return redirect('home')

def loginaccount(request):    
    if request.method == 'GET':
        # print("if clause")
        return render(request, 'loginaccount.html', 
                      {'form':AuthenticationForm})            
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])  
        # print("else clause")
        # print(user.is_authenticated)
        # print(user.get_username)          
        if user is None: 
            # print("calling loginaccount")                               
            return render(request,'loginaccount.html', 
                    {'form': AuthenticationForm(), 
                    'error': 'username and password do not match'})
        else: 
            # print("performing login and redirect")
            login(request,user)
            return redirect('home')
