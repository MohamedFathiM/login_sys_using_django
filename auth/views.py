from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as adminLogin ,logout as adminLogout

# Create your views here.

def home(request):
    return render(request,'auth/index.html')


def register(request):

    if request.method == 'POST' :
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        myUser = User.objects.create_user(username,email,password)
        myUser.first_name = name
        myUser.save()

        messages.success(request,"Your Account Has Been Successfully Created .")

        return redirect('login')

    return render(request,'auth/register.html')


def login(request):

    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            adminLogin(request=request,user=user)

            return render(request,'auth/home.html',{'first_name' : user.first_name})

        else :
            messages.error(request=request,message='Bad Credentials')

            return redirect('home')

    return render(request,'auth/login.html')


def logout(request):
    adminLogout(request)
    messages.success(request=request,message='Logged Out Successfully')

    return redirect('home')
