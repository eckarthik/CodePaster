from django.urls import path
from . import views
urlpatterns = [
    path('', views.create_paste),
    path('signup',views.register_user),
    path('login',views.login_user)
]
