from django.shortcuts import render, redirect

from user.models import UserActivity
from .forms import SignUpForm
from django.contrib.auth import login
from datetime import datetime


# Create your views here.
def front_page(request):
    return render(request, 'base/frontpage.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            UserActivity.objects.create(
                user=user, is_online=True, status='online', when=datetime.now()
            )
            return redirect('frontpage')
    else:
        form = SignUpForm()
    return render(request, 'base/signup.html', {'form': form})


# def login(request):
#     if request.method == "POST":
#         # form = Login

#         return redirect('frontpage')
#     # else:

#     return render(request, 'base/login.html')
