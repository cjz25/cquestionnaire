from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Question, QuestionChoice, Questionnaire
from .serializers import QuestionnaireSerializer, QuestionSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        return Questionnaire.objects.prefetch_related(
            Prefetch(
                'questions',
                queryset=Question.objects.filter(
                    questionnaire=self.kwargs['pk']
                ).order_by('questionsequence__seq')
                .prefetch_related(
                    Prefetch(
                        'choices',
                        queryset=QuestionChoice.objects.order_by('questionchoicesequence__seq')
                    )
                )
            )
        )

    def list(self, request):
        queryset = Questionnaire.objects.all()
        return Response(queryset.values())


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(
            questionnaire=self.kwargs['questionnaire_pk']
        ).prefetch_related(
            Prefetch(
                'choices',
                queryset=QuestionChoice.objects.order_by('questionchoicesequence__seq')
            )
        )

    def create(self, request, questionnaire_pk=None):
        request.data['questionnaire'] = questionnaire_pk
        return super().create(request)

    def update(self, request, pk=None, questionnaire_pk=None):
        request.data['questionnaire'] = questionnaire_pk
        response = super().update(request)
        response.data['choices'] = sorted(response.data['choices'], key=lambda x: x['seq'])
        return response
