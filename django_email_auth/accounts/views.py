from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'accounts/home.html')

def login_attempt(request):
    return render(request,'accounts/login.html')

def register_attempt(request):
    return render(request,'accounts/register.html')

def success(request):
    return render(request,'accounts/success.html')

def token_send(request):
    return render(request,'accounts/token_send.html')
