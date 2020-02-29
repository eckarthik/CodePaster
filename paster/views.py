from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,Http404
from paster.models import Paste,Profile
from .forms import PasteForm,SignUpForm,LoginForm
import random,string,datetime
from django.views.generic import View,RedirectView,TemplateView,CreateView,UpdateView,DetailView,ListView

# # Create your views here.

class PasteCreateView(CreateView):
    template_name = "home.html"
    form_class = PasteForm
    success_url = "/pastes/"
    http_method_names = ['get','post']

    def form_valid(self, form):
        paste = form.save(commit=False)
        if self.request.user.is_authenticated:
            paste.user = self.request.user
        else:
            paste.user = None
        paste.slug = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        paste.save()
        self.success_url = self.success_url+paste.slug
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasteForm()
        context['recent_pastes'] = Paste.objects.order_by('-created_at')[0:5]
        context['user'] = self.request.user
        return context

class RegisterUserView(CreateView):
    form_class = SignUpForm
    template_name = "signup.html"
    extra_context = {}
    success_url = "/signup/"
    http_method_names = ['get','post']

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form,'register_success':"success"})
        else:
            return render(request,'signup.html', {'form':form,'register_success':"failure"})


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

class LogoutView(RedirectView):
    url = "/"

    def dispatch(self, request, *args, **kwargs):
        logout(self.request)
        return super().dispatch(request,*args,**kwargs)

class ViewPaste(UpdateView):
    template_name = "paste_view.html"
    extra_context = {'can_be_edited':False}
    slug_field = "slug"
    slug_url_kwarg = "slug"
    model = Paste
    fields = '__all__'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.queryset = Paste.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paste'] = self.object
        context['recent_pastes'] = Paste.objects.order_by('-created_at')[0:5]
        context.update(self.extra_context)
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.queryset)
        if request.user.is_authenticated:
            if request.user == self.object.user:
                self.extra_context['can_be_edited'] = True
        # updating the pasteview counters
        self.object.views = self.object.views+1
        self.object.save()
        return self.render_to_response(context=self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.queryset)
        if request.user.is_authenticated and request.user == self.object.user:
            self.object.content = request.POST.get('content')
            self.object.created_at = datetime.datetime.now()
            self.object.save()
            return self.render_to_response(context=self.get_context_data())
        else:
            return self.render_to_response(context=self.get_context_data())

class ProfileView(DetailView):
    template_name = "profile.html"

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            return render(request,'profile.html',{'profile':profile})
        else:
            return redirect('/')

    def post(self,request,*args,**kwargs):
        profile = Profile.objects.get(user=request.user)
        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.save()
        return render(request,'profile.html',{'profile_saved':True,'profile':profile})

class MyPastesView(ListView):
    template_name = "my_pastes.html"
    context_object_name = "my_pastes"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.queryset = Paste.objects.filter(user=request.user)
        return super().dispatch(request,*args,**kwargs)

class DownloadPasteView(View):

    def get(self, request, *args, **kwargs):
        paste = Paste.objects.get(slug=self.kwargs['slug'])
        response = HttpResponse(content=paste.content)
        paste_title = paste.title.replace(" ","_")
        response['Content-Disposition'] = 'attachment; filename={}.{}'.format(paste_title, "txt")
        return response

class RawPasteView(View):

    def get(self, request, *args, **kwargs):
        paste = Paste.objects.get(slug=self.kwargs['slug'])
        response = HttpResponse(content=paste.content)
        response['Content-Type'] = 'text/plain'
        return response

class ClonePasteView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paste = Paste.objects.get(slug__exact=self.kwargs['slug'])
        recent_pastes = Paste.objects.order_by('-created_at')[0:5]
        form = PasteForm(initial={'title':paste.title,'content':paste.content,'syntax':paste.syntax,'expiry':paste.expiry})
        context['form'] = form
        context['user'] = self.request.user
        context['recent_pastes'] = recent_pastes
        return context



# def create_paste(request):
#     if request.method == 'POST':
#         form = PasteForm(request.POST)
#         if form.is_valid():
#             paste = form.save(commit=False)
#             if request.user.is_authenticated:
#                 paste.user = request.user #Let's add the user details
#             else:
#                 paste.user = None
#             paste.slug = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#             paste.save()
#             return redirect('/pastes/'+paste.slug)
#     else:
#         form = PasteForm()
#
#     recent_pastes = Paste.objects.order_by('-created_at')[0:5]
#     return render(request,'home.html',{'form':form,'user':request.user,'recent_pastes':recent_pastes})


# def register_user(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = SignUpForm()
#             return render(request, 'signup.html', {'form': form,'register_success':"success"})
#         else:
#             return render(request,'signup.html', {'form':form,'register_success':"failure"})
#     else:
#         form = SignUpForm()
#         return render(request, 'signup.html', {'form': form, 'user': request.user})


# def logout_user(request):
#     logout(request)
#     return redirect('/')


# def view_paste(request,slug):
#     try:
#         paste = Paste.objects.get(slug__exact=slug)
#     except Paste.DoesNotExist:
#         raise Http404("Sorry! Paste does not exist")
#
#     recent_pastes = Paste.objects.order_by('-created_at')[0:5]
#     can_be_edited = False
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             if request.user == paste.user:
#                 can_be_edited = True
#         #updating the pasteview counters
#         paste.views = paste.views+1
#         paste.save()
#         return render(request,'paste_view.html',{'paste':paste,'can_be_edited':can_be_edited,'recent_pastes':recent_pastes})
#     elif request.method == 'POST':
#         if request.user.is_authenticated and request.user == paste.user:
#             paste.content = request.POST.get('content')
#             paste.save()
#             return render(request,'paste_view.html',{'paste':paste,'can_be_edited':can_be_edited,'paste_edit_success':"success",'recent_pastes':recent_pastes})
#         else:
#             return render(request, 'paste_view.html',
#                           {'paste': paste, 'can_be_edited': can_be_edited,'paste_edit_success':"failure",'recent_pastes': recent_pastes})

# def profile(request):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             profile = Profile.objects.get(user=request.user)
#             return render(request,'profile.html',{'profile':profile})
#         else:
#             return redirect('/')
#     elif request.method == "POST":
#         profile = Profile.objects.get(user=request.user)
#         profile.bio = request.POST.get('bio')
#         profile.location = request.POST.get('location')
#         profile.save()
#         return render(request,'profile.html',{'profile_saved':True,'profile':profile})


# def my_pastes(request):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             pastes = Paste.objects.filter(user=request.user)
#             return render(request,"my_pastes.html",{'my_pastes':pastes})
#         else:
#             return redirect('/')


# def download_paste(request,slug):
#     paste = Paste.objects.get(slug=slug)
#     response = HttpResponse(content=paste.content)
#     paste_title = paste.title.replace(" ","_")
#     response['Content-Disposition'] = 'attachment; filename={}.{}'.format(paste_title, "txt")
#     return response

# def paste_raw(request,slug):
#     paste = Paste.objects.get(slug=slug)
#     response = HttpResponse(content=paste.content)
#     response['Content-Type'] = 'text/plain'
#     return response