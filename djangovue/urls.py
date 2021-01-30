from django.contrib import admin
from django.urls import include, path
from .routers import router, questionnaires_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(questionnaires_router.urls)),
]
