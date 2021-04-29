from django.db.models import F
from rest_framework import serializers
from .models import (
    Question, QuestionSequence, QuestionChoice,
    QuestionChoiceSequence, Questionnaire
)


class QuestionChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = QuestionChoice
        fields = ['id', 'item']


class QuestionSerializer(serializers.ModelSerializer):
    seq = serializers.IntegerField(required=False)
    choices = QuestionChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        question_seq = validated_data.pop('seq', 0)
        choices_data = validated_data.pop('choices', [])

        # increment seq by 1 for all questions whose seqs are greater than question_seq
        QuestionSequence.objects.filter(
            questionnaire=validated_data['questionnaire']
        ).filter(seq__gte=question_seq).update(seq=F('seq') + 1)

        # create question
        question = Question.objects.create(**validated_data)

        # create question sequence for the question created above
        QuestionSequence.objects.create(
            questionnaire=question.questionnaire,
            question=question,
            seq=question_seq
        )

        # create question choice and its corresponding sequence
        for index, choice_data in enumerate(choices_data):
            questionchoice = QuestionChoice.objects.create(question=question, **choice_data)
            QuestionChoiceSequence.objects.create(
                question=question,
                questionchoice=questionchoice,
                seq=index
            )

        return question

    def update(self, instance, validated_data):
        validated_data.pop('seq', 0)

        choices_data = validated_data.pop('choices', [])

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        self.__updateChoice(instance, choices_data)

        return instance

    def __updateChoice(self, instance, choices_data):
        if choices_data is None:
            return

        choices_instance_dict = dict((i.id, i) for i in instance.choices.all())

        choice_instances = []

        for index, choice_data in enumerate(choices_data):
            if 'id' in choice_data:
                # update question choice
                choice_instance = choices_instance_dict.pop(choice_data['id'])
                for attr, val in choice_data.items():
                    setattr(choice_instance, attr, val)
                choice_instance.save()

                choice_instances.append(choice_instance)

                # update question choice sequence
                QuestionChoiceSequence.objects.filter(
                    question=instance, questionchoice=choice_instance
                ).update(seq=index)
            else:
                # create question choice
                question_choice = QuestionChoice.objects.create(question=instance, **choice_data)

                choice_instances.append(question_choice)

                # create question choice sequence
                QuestionChoiceSequence.objects.create(
                    question=instance,
                    questionchoice=question_choice,
                    seq=index
                )

        # delete
        if len(choices_instance_dict) > 0:
            for choice_instance in choices_instance_dict.values():
                choice_instance.delete()

        return choice_instances


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'


class QuestionnaireWithQuestionSerializer(QuestionnaireSerializer):
    questions = QuestionSerializer(many=True, read_only=True, required=False)


class SequenceSerializer(serializers.Serializer):
    old_seq = serializers.IntegerField(required=False)
    new_seq = serializers.IntegerField(required=True)

    def update_questionsequence(self, questionnaire_id, question_id):
        old_questionsequence = QuestionSequence.objects.get(
            questionnaire=questionnaire_id, question=question_id)

        new_seq = self.initial_data['new_seq']

        if new_seq == old_questionsequence.seq:
            return

        if new_seq < old_questionsequence.seq:
            (QuestionSequence.objects
                .filter(questionnaire=questionnaire_id)
                .filter(seq__gte=new_seq)
                .filter(seq__lt=old_questionsequence.seq)
                .update(seq=F('seq') + 1))
        else:
            (QuestionSequence.objects
                .filter(questionnaire=questionnaire_id)
                .filter(seq__gt=old_questionsequence.seq)
                .filter(seq__lte=new_seq)
                .update(seq=F('seq') - 1))

        old_questionsequence.seq = new_seq
        old_questionsequence.save()
