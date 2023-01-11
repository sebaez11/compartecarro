from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        'circles/', 
        include(
            ('compartecarro.circles.urls','circles'), 
            namespace='circles'
        )
    ),
    path(
        'users/', 
        include(
            ('compartecarro.users.urls','users'), 
            namespace='users'
        )
    ),
    path(
        'rides/', 
        include(
            ('compartecarro.rides.urls','rides'), 
            namespace='rides'
        )
    ),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
