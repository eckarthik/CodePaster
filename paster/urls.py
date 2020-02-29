from django.urls import path
from . import views
urlpatterns = [
    path('', views.PasteCreateView.as_view(),name="createpaste"),
    path('signup',views.RegisterUserView.as_view(),name="signup"),
    path('login',views.login_user,name="login"),
    path('logout',views.LogoutView.as_view(),name="logout"),
    path('pastes/<slug:slug>',views.ViewPaste.as_view(),name="pastes"),
    path('profile',views.ProfileView.as_view(),name="profile"),
    path('mypastes',views.MyPastesView.as_view(),name="mypastes"),
    path('download/<slug:slug>',views.DownloadPasteView.as_view(),name="downloadpaste"),
    path('pastes/<slug:slug>/raw',views.RawPasteView.as_view(),name="rawpaste"),
    path('pastes/<slug:slug>/clone',views.ClonePasteView.as_view(),name="clonepaste")
]
