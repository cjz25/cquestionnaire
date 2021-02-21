from rest_framework import serializers
from .models import Question, QuestionChoice, Questionnaire


class QuestionChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = QuestionChoice
        fields = ['id', 'item']


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        choices_data = validated_data.pop('choices') if 'choices' in validated_data else []
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            QuestionChoice.objects.create(question=question, **choice_data)
        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices')
        choices_instance_dict = dict((i.id, i) for i in instance.choices.all())

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        for choice_data in choices_data:
            if 'id' in choice_data:
                # update
                choice_instance = choices_instance_dict.pop(choice_data['id'])
                for attr, val in choice_data.items():
                    setattr(choice_instance, attr, val)
                choice_instance.save()
            else:
                # create
                QuestionChoice.objects.create(question=instance, **choice_data)

        # delete
        if len(choices_instance_dict) > 0:
            for choice_instance in choices_instance_dict.values():
                choice_instance.delete()

        return instance


class QuestionnaireSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Questionnaire
        fields = '__all__'
