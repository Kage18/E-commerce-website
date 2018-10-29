from django.shortcuts import render
from register.forms import LoginForm,RegisterForm

# Create your views here.
def home(request):
    return render(request,'register/index.html')

def register(request):

    registered = False

    if request.method == "POST":
        loginform = LoginForm(data=request.POST)
        registerform=RegisterForm(data=request.POST)

        if loginform.is_valid() and registerform.is_valid():

            user = loginform.save()
            user.set_password(user.password)
            user.save()

            profile =registerform.save(commit=False)
            profile.user =user

            profile.save()

            registered = True
        else:
            print(loginform.errors, registerform.errors)
    else:
        loginform = LoginForm()
        registerform = RegisterForm()

    return render(request,'register/registration.html',
                  {'loginform':loginform,
                   'registerform':registerform,
                   'registered':registered})

