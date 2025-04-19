from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import CustomSignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'app/index.html')

def exploreStations(request):
    return render(request,'app/explore_stations.html')

def my_stations(request):
    return render(request,'app/my_stations.html')



def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
            )
            login(request,user)
            messages.success(request, "Account created and logged in!")
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'app/signup.html', {'form':form})

def login_view(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            #get the user using email
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return render(request,'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    user = request.user
    return render(request, 'app/dashboard.html',{
        'username':user.username,
        'email':user.email
    })