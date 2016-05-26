from django.shortcuts import render
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import logout

def home(request):
	return render(request,'login/home.html')
def signUp(request):
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
            return HttpResponse('<p> ok. password changed/p>')
    else:
        return render(request,'login/passwordChange.html');
