from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('app/', include('app.urls')),
    path('project/', include('project.urls')),
    path('taskmanager/', include('TaskManager.urls')),
    # path('shop/', include('shop.urls')),

    # token urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]