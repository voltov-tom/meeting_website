from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from userprofile.views import CreateUserView, UserViewSet, Logout, UserLikesView

router = SimpleRouter()

router.register(r'api/list', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token, name='obtain-auth-token'),
    path('logout/', Logout.as_view()),
    path('api/clients/<int:id>/match', UserLikesView.as_view()),
    path('api/clients/create/', CreateUserView.as_view()),
]
urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
