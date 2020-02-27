from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,Http404
from paster.models import Paste,Profile
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
            return render(request, 'signup.html', {'form': form,'register_success':"success"})
        else:
            return render(request,'signup.html', {'form':form,'register_success':"failure"})
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
                return render(request, 'login.html', {'form': form, 'user': request.user,'login_success':"failure"})
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
    can_be_edited = False
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user == paste.user:
                can_be_edited = True
        return render(request,'paste_view.html',{'paste':paste,'can_be_edited':can_be_edited,'recent_pastes':recent_pastes})
    elif request.method == 'POST':
        if request.user.is_authenticated and request.user == paste.user:
            paste.content = request.POST.get('content')
            paste.save()
            return render(request,'paste_view.html',{'paste':paste,'can_be_edited':can_be_edited,'paste_edit_success':"success",'recent_pastes':recent_pastes})
        else:
            return render(request, 'paste_view.html',
                          {'paste': paste, 'can_be_edited': can_be_edited,'paste_edit_success':"failure",'recent_pastes': recent_pastes})

def profile(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            return render(request,'profile.html',{'profile':profile})
        else:
            return redirect('/')
    elif request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.save()
        return render(request,'profile.html',{'profile_saved':True,'profile':profile})

def my_pastes(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            pastes = Paste.objects.filter(user=request.user)
            return render(request,"my_pastes.html",{'my_pastes':pastes})
        else:
            return redirect('/')

