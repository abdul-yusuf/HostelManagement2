from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm\
    # , SignUpForm
import requests


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     # return render(request, 'store/signup.html', {'form': form})
#     return JsonResponse('Signup Successfull', safe=False)


def login_view(request):
    form = AuthenticationForm(request, data=request.POST)
    if request.method == 'POST':
        # referer = request.META.get('HTTP_REFERER')
        next = request.GET.get('next', 'home')
        try:
            next = request.POST.get('next', 'home')
        except:
            pass
        if form.is_valid():
            username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(request, username=username,password=raw_password)
            print(next)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully')
                return redirect(reverse(next))

    return render(request, 'registration/login.html', {'form': form})


# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         # referer = request.META.get('HTTP_REFERER')
#         next = request.GET.get('next', 'store')
#         try:
#             next = request.POST.get('next', 'store')
#         except:
#             pass
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             first_name = form.cleaned_data.get('first_name')
#             last_name = form.cleaned_data.get('last_name')
#             password = form.cleaned_data.get('password')
#             login(request, user)
#             messages.success(request, 'SignUp Successfull')
#             print(next)
#             # if referer:
#             #     return redirect(referer)
#             return redirect(reverse(next))
#     else:
#         form = SignUpForm()
#
#     return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successfull')
    return redirect('home')