from django.db.models import Prefetch

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Question, QuestionSequence, QuestionChoice, Questionnaire
from .serializers import (
    QuestionnaireSerializer, QuestionSerializer,
    QuestionChoiceSerializer, SequenceSerializer
)


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
        sequence_serializer = SequenceSerializer(data={'new_seq': request.data['seq']})
        if sequence_serializer.is_valid():
            # use questionnaire_pk, and pk to update seqs
            sequence_serializer.update_questionsequence(
                questionnaire_id=questionnaire_pk,
                question_id=pk
            )
        else:
            return Response(sequence_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=True, methods=['PUT'], url_path='sequence')
    def adjust_sequence(self, request, pk=None, questionnaire_pk=None):
        sequence_serializer = SequenceSerializer(data=request.data)
        if sequence_serializer.is_valid():
            # use questionnaire_pk, and pk to update seqs
            sequence_serializer.update_questionsequence(
                questionnaire_id=questionnaire_pk,
                question_id=pk
            )
            # save questionnaire to set updated_dtm to now
            Questionnaire.objects.get(id=questionnaire_pk).save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(sequence_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
