from django.shortcuts import render
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

def home(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username,password = password)
		if user is None:
			return HttpResponse("<p> No such user existed</p>")
		else:
			login(request,user)
			# return HttpResponseRedirect(reverse('index'),args=[username])
			return render(request,'feed/index.html',{'username':username})
	else:
		return render(request,'login/home.html')



def signUp(request):
	if request.method == 'POST':
		firstName = request.POST.get('firstName')
		lastName = request.POST.get('lastName')
		username = request.POST.get('username')
		password = request.POST.get('newpass')
		try:
			user = User.objects.get(username = username)
			return HttpResponse('<p> user existed</p>')
		except Exception:
			user = User.objects.create_user(username,username,password)
			user.first_name = firstName
			user.last_name = lastName
			user.save()

			return render(request,'login/home.html')
	else:
		return render(request,'login/signup.html')

def passwordChange(request):
    if request.method == 'POST':
        usernames = request.POST.get('username')
        oldPassword = request.POST.get('oldpass')
        newPassword = request.POST.get('newpass')
        try:
            user = User.objects.get(username=usernames)
        except Exception:
            # return render(request,'registration/WrongUserOrPassword.html')
            return HttpResponse('<p> wrong user or passwd</p>')
        if not user.check_password(oldPassword):
            # return render(request,'registration/WrongUserOrPassword.html')  
            return HttpResponse('<p> wrong user or passwd</p>')
        else:
            user.set_password(newPassword)
            user.save();
            # return render(request,'registration/SuccessPasswdChange.html')  
            return HttpResponse('<p> ok. password changed</p>')
    else:
        return render(request,'login/passwordChange.html');
