# Generated by Django 3.1.5 on 2021-02-21 04:04

from django.db import migrations


def migrate_question_seq(apps, schema_editor):
    '''
    We can't import the Question and QuestionSequence models directly as they may be the newer
    version than this migration expects. We use the historical version.
    '''
    Question = apps.get_model('questionnaire', 'Question')
    QuestionSequence = apps.get_model('questionnaire', 'QuestionSequence')
    for question in Question.objects.all():
        QuestionSequence.objects.create(
            questionnaire_id=question.questionnaire_id,
            question_id=question.id,
            seq=question.seq
        )


def migrate_questionchoice_seq(apps, schema_editor):
    '''
    We can't import the QuestionChoice and QuestionChoiceSequence models directly as they may be
    the newer version than this migration expects. We use the historical version.
    '''
    QuestionChoice = apps.get_model('questionnaire', 'QuestionChoice')
    QuestionChoiceSequence = apps.get_model('questionnaire', 'QuestionChoiceSequence')
    for questionchoice in QuestionChoice.objects.all():
        QuestionChoiceSequence.objects.create(
            question_id=questionchoice.question_id,
            questionchoice_id=questionchoice.id,
            seq=questionchoice.seq
        )


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_questionchoicesequence_questionsequence'),
    ]

    operations = [
        migrations.RunPython(migrate_question_seq),
        migrations.RunPython(migrate_questionchoice_seq),
    ]