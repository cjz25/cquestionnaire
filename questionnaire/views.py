from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Question, QuestionSequence, QuestionChoice, Questionnaire
from .serializers import QuestionnaireSerializer, QuestionSerializer, QuestionChoiceSerializer


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
        return (
            Question.objects.filter(
                questionnaire=self.kwargs['questionnaire_pk']
            )
            .order_by('questionsequence__seq')
            .prefetch_related(
                Prefetch(
                    'choices',
                    queryset=QuestionChoice.objects.order_by('questionchoicesequence__seq')
                )
            )
        )

    def create(self, request, questionnaire_pk=None):
        request.data['questionnaire'] = questionnaire_pk
        return super().create(request)

    def update(self, request, pk=None, questionnaire_pk=None):
        request.data['questionnaire'] = questionnaire_pk
        response = super().update(request)
        choices = QuestionChoice.objects.filter(question=pk).order_by('questionchoicesequence__seq')
        response.data['choices'] = QuestionChoiceSerializer(choices, many=True).data
        return response

    def destroy(self, request, pk=None, questionnaire_pk=None):
        response = super().destroy(request)

        question_sequences = QuestionSequence.objects.filter(
            questionnaire=questionnaire_pk).order_by('seq')

        for index, question_sequence in enumerate(question_sequences):
            question_sequence.seq = index

        QuestionSequence.objects.bulk_update(question_sequences, ['seq'])

        return response
