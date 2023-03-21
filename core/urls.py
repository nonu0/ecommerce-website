from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
    path('api/token/verify/',TokenVerifyView.as_view()),
    path('admin/', admin.site.urls),
    path('',include('website.urls')),
    path('authentication/',include('authentication.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
