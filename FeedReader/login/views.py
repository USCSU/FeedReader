from django.shortcuts import render
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import logout

def home(request):
	return render(request,'login/home.html')
def signUp(request):
	return render(request,'login/signup.html')