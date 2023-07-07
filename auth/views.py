from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as adminLogin ,logout as adminLogout
from django.core.mail import send_mail
from .forms import RegisterForm
from django.views import View

# Create your views here.

def home(request):
    return render(request,'auth/index.html')


class register(View):

    def get(self,request) :
        return render(request,'auth/register.html')

    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        registerForm = RegisterForm(request.POST)
        if not registerForm.is_valid():
            return render(request,'auth/register.html',{'form':registerForm})

        myUser = User.objects.create_user(username,email,password)
        myUser.first_name = name
        myUser.save()

        messages.success(request,"Your Account Has Been Successfully Created .")

        # Welcome Email
        subject = "Welcome To Our Django Login !"
        message = "Hello " + myUser.first_name  + "!! \n" + "Welcome To GFG !! \n Thank ypu For Visiting Our Website \n We have also send you a confirmation email, please confirm your email address in order to activate your account . \n\n Thanking"
        from_email = "mohamed@yahoo.com"
        to_list = [myUser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect('login')



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
