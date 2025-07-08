from django.shortcuts import render, redirect
from userauth.forms import UserRegisterForm
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from django.conf import settings
from userauth.models import User


#User = settings.AUTH_USER_MODEL

# Create your views here.
def signup(request):
    
    if request.method=="POST":
         form = UserRegisterForm(request.POST or None)
         if form.is_valid():
             new_user = form.save()
             username = form.cleaned_data.get("username")
             messages.success(request, f"hey {username}, account created successfully")
             new_user = authenticate(username=form.cleaned_data['email'],
                                      password=form.cleaned_data['password1'])
             login (request,new_user)
             return redirect("uwapp:index")
    else:
        form = UserRegisterForm()
   
 
    context={
        'form':form,
    }
 
    return render(request,'auth/signup.html',context)



def signin(request):
    if request.user.is_authenticated:
       return redirect("uwapp:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request,email=email, password=password)
        
            if user is not None:
                login(request,user)
                messages.success(request,"logged in")
                return redirect("uwapp:index")
            else:
                messages.warning(request,"user does not exist, please signup")
    
        except:
            messages.warning(request,f"{email} does not exist")
            
        
    return render(request,'auth/login.html')     
     

def signout(request):
    logout(request) 
    return redirect("userauth:login")    
    