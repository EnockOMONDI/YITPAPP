from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken!')
                return redirect('.')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered!')
                return redirect('.')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)
                return redirect('blog')
        else:
            messages.info(request, 'Password not matching!')
            return render('.')
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('blog')
        else:
            messages.info(request, 'Invalid Credentials!')
            return redirect('.')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')

def home(request):
    
    return render(request, 'users/index.html')

def courses(request):
    
    return render(request, 'users/courses.html')

def about(request):
    
    return render(request, 'users/about.html')

def team(request):
    
    return render(request, 'users/ourteam.html')

def registration(request):
    
    return render(request, 'users/registration.html')

def registration2(request):
    
    return render(request, 'users/registration2.html')


def events(request):
    
    return render(request, 'users/events.html')

def faqs(request):
    
    return render(request, 'users/faqs.html')

def contact(request):
    
    return render(request, 'users/contact.html') 
    

def coursedetail1(request):
    
    return render(request, 'users/coursedetail1.html')   

def coursedetail2(request):
    
    return render(request, 'users/coursedetail2.html')

def coursedetail3(request):
    
    return render(request, 'users/coursedetail3.html')  

def coursedetail4(request):
    
    return render(request, 'users/coursedetail4.html')      

def coursedetail5(request):
    
    return render(request, 'users/coursedetail5.html')

def coursedetail6(request):
    
    return render(request, 'users/coursedetail6.html')








