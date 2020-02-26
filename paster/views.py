from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,Http404
from paster.models import Paste
from .forms import PasteForm,SignUpForm,LoginForm
import random,string

# Create your views here.
def create_paste(request):
    if request.method == 'POST':
        form = PasteForm(request.POST)
        if form.is_valid():
            paste = form.save(commit=False)
            if request.user.is_authenticated:
                paste.user = request.user #Let's add the user details
            else:
                paste.user = None
            paste.slug = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            paste.save()
            return redirect('/pastes/'+paste.slug)
    else:
        form = PasteForm()

    recent_pastes = Paste.objects.order_by('-created_at')[0:5]
    return render(request,'home.html',{'form':form,'user':request.user,'recent_pastes':recent_pastes})

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

def logout_user(request):
    logout(request)
    return redirect('/')

def view_paste(request,slug):
    try:
        paste = Paste.objects.get(slug__exact=slug)
    except Paste.DoesNotExist:
        raise Http404("Sorry! Paste does not exist")

    recent_pastes = Paste.objects.order_by('-created_at')[0:5]
    return render(request,'paste_view.html',{'paste':paste,'recent_pastes':recent_pastes})
