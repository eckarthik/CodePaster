from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from .forms import PasteForm,SignUpForm,LoginForm

# Create your views here.
def create_paste(request):
    if request.method == 'POST':
        form = PasteForm(request.POST)
        if form.is_valid():
            paste = form.save(commit=False)
            paste.user = request.user #Let's add the user details
            if paste.save():
                return HttpResponse("Paste Saved")
            else:
                return HttpResponse("Could not save Paste")
    else:
        form = PasteForm()

    return render(request,'home.html',{'form':form,'user':request.user})

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form,'register_success':True})
        else:
            return render(request,'signup.html', {'form':form,'register_success':False})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form, 'user': request.user})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'user': request.user})
        else:
            print("Form not valid",form.errors)
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'user': request.user})