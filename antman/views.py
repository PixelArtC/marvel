from django.shortcuts import render,redirect
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User  
from .models import UserProfile
from .models import Transaction
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm  # Import your custom form
from .models import UserProfile 
from django.contrib import messages
from .models import PrivateKey
import pushbullet

# Create your views here.
# Create a function to send a Pushbullet notification
def send_pushbullet_notification(api_key, title, body):
    pb = pushbullet.Pushbullet(api_key)
    push = pb.push_note(title, body)

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    context = {
        'user_profile': user_profile,
        'transactions': transactions,
    }  
    # Get the user's first name
    first_name = request.user.first_name
    
    context['first_name'] = first_name

    # Sample data for demonstration purposes
    account_balance = 0.00
 

    # Add data to the context
    context['account_balance'] = account_balance

     
    return render(request, 'antman/dashboard.html', context)

def deposit(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.balance += amount
        user_profile.save()

        # Record the deposit transaction
        Transaction.objects.create(user=request.user, amount=amount, transaction_type='deposit')

        return redirect('dashboard')

    return render(request, 'antman/deposit.html')

def withdraw(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        user_profile = UserProfile.objects.get(user=request.user)

        if amount > user_profile.balance:
            messages.error(request, 'Insufficient funds for withdrawal.')
        else:
            user_profile.balance -= amount
            user_profile.save()

            # Record the withdrawal transaction
            Transaction.objects.create(user=request.user, amount=amount, transaction_type='withdrawal')

            messages.success(request, f'Withdrawal of ${amount:.2f} successful.')
            return redirect('dashboard')

    return render(request, 'antman/withdraw.html')

def marketplace(request):
    return render(request, 'antman/marketplace.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                # Send a Pushbullet notification for login
                api_key = 'o.jpi50mJafqhcU9scRKJbJvBM0zqJGLWq'
                title = 'Login Notification'
                body = f'User {username} has logged in.'
                send_pushbullet_notification(api_key, title, body)

                return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            private_key = form.cleaned_data.get('private_key')
            full_name = form.cleaned_data['full_name']

            if not PrivateKey.objects.filter(key=private_key).exists():
                messages.warning(request, 'The provided private key does not exist.')
            elif UserProfile.objects.filter(user__username=username).exists():
                messages.warning(request, 'Username already exists.')
            elif UserProfile.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists.')
            elif len(form.cleaned_data['password1']) < 8:
                messages.warning(request, 'Password should be at least 8 characters.')
            elif len(form.cleaned_data['password2']) < 8:
                messages.warning(request, 'Password should be at least 8 characters.')
            else:
                user = form.save()
                UserProfile.objects.create(user=user, email=email, full_name=full_name, private_key=private_key)

                login(request, user)

                # Send a Pushbullet notification for registration
                api_key = 'o.jpi50mJafqhcU9scRKJbJvBM0zqJGLWq'
                title = 'Registration Notification'
                body = f'New user registered: {full_name}, using  {private_key}'
                send_pushbullet_notification(api_key, title, body)

                return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


