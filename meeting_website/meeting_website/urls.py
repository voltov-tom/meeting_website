from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from userprofile.views import UserListView, UserViewSet, Logout

router = SimpleRouter()

router.register(r'api/clients', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token, name='obtain-auth-token'),
    path('logout/', Logout.as_view()),
    path('api/clients/create/', UserListView.as_view()),
]
urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
