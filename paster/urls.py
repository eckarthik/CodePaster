from django.urls import path
from . import views
urlpatterns = [
    path('', views.create_paste),
    path('signup',views.register_user,name="signup"),
    path('login',views.login_user,name="login"),
    path('logout',views.logout_user,name="logout"),
    path('pastes/<slug:slug>',views.view_paste,name="pastes"),
    path('profile',views.profile,name="profile"),
    path('mypastes',views.my_pastes,name="mypastes")
]
