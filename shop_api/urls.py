from django.contrib import admin
from django.urls import path, include
from . import swagger
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('product.urls')),
    path('api/v1/users/', include('users.urls')),
]

urlpatterns += swagger.urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
