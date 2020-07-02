from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
def register(request):
    if request.method == 'POST' :
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'You are now registered successfully')
                    return redirect('register')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
def login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successfull, Session started')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials, Please check the information you\'ve typed')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You have successfully logged out')
        return redirect('index')
