from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Questionnaire(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_dtm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):

    # short answer, multiple choice, checkboxes
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#enumeration-types
    class QuestionType(models.TextChoices):
        SHORT_ANSWER = 'SA', _('Short Answer')
        MULTIPLE_CHOICE = 'MC', _('Multiple Choice')
        CHECKBOXES = 'CB', _('Checkboxes')

    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    seq = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    required = models.BooleanField()
    question_type = models.CharField(
        max_length=2,
        choices=QuestionType.choices,
        default=QuestionType.SHORT_ANSWER,
    )
    visible = models.BooleanField()

    def __str__(self):
        return f'{self.questionnaire.title} | {self.title}'


class QuestionSequence(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    seq = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('questionnaire', 'question'),)


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    seq = models.PositiveSmallIntegerField()
    item = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.question.title} | {self.item}'


class QuestionChoiceSequence(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    questionchoice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)
    seq = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('question', 'questionchoice'),)


# response master
class QuestionResponseMaster(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)


# response detail
class QuestionResponseDetail(models.Model):
    response_master_id = models.ForeignKey(QuestionResponseMaster, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


# response for question types: multiple choice, checkboxes
class QuestionResponseSelection(models.Model):
    response_detail_id = models.ForeignKey(QuestionResponseDetail, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)


# response for question type: short answer
class QuestionResponseText(models.Model):
    response_detail_id = models.ForeignKey(QuestionResponseDetail, on_delete=models.CASCADE)
    text = models.TextField()
