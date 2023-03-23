import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .models import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def home(request):
    return render(request,'accounts/home.html')

def login_attempt(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,"User not found")
            return redirect('/login')
        
        profile_obj = Profile.objects.filter(user=user_obj).first()
        
        if not profile_obj.is_verified:
            messages.success(request,'Profile is not verified. Check your mail')
            return redirect('/login')

        user = authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'Wrong Password')
            return redirect('/login')
        
        login(request,user)
        return redirect('/')
        
    return render(request,'accounts/login.html')

def register_attempt(request):

    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username = username).first():
                print("first")
                messages.success(request,'Username is taken')
                return redirect('/register')
            
            if User.objects.filter(email = email).first():
                print("second")
                messages.success(request,'Email is taken')
                return redirect('/register')

            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token= auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token')

        except Exception as e:
            print(f"Exception:- {e}")


    return render(request,'accounts/register.html')

def success(request):
    return render(request,'accounts/success.html')

def token_send(request):
    return render(request,'accounts/token_send.html')

def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your account is already verified')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,"Your account has been verified")
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return render(request,'accounts/error.html')

def send_mail_after_registration(email,token):
    subject = "Your account needs to be verified"
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
