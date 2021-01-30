from rest_framework_nested import routers
from questionnaire.views import QuestionnaireViewSet, QuestionViewSet

router = routers.SimpleRouter()
router.register(r'questionnaires', QuestionnaireViewSet, basename='questionnaire')

questionnaires_router = routers.NestedSimpleRouter(
    router, r'questionnaires', lookup='questionnaire')
questionnaires_router.register(
    r'questions', QuestionViewSet, basename='questionnaire-questions')
