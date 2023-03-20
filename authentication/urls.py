from django.urls import path
from authentication.views import *
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login',LoginView.as_view(),name='login'),
    path('register',RegisterView.as_view(),name='register'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate_user,name='activate')
]