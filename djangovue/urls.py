from django.contrib import admin
from django.urls import include, path
from .routers import router, questionnaires_router

from questionnaire.views import (
    QuestionnaireListAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(questionnaires_router.urls)),
    path('api/questionnaires/list', QuestionnaireListAPIView.as_view(), name='questionnaires_list'),
]
