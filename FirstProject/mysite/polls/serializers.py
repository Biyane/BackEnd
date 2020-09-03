from rest_framework import serializers
from .models import Question, Choice
from django.utils import timezone


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text']
        ordering = ['pub_date']

    def create(self, validated_data):
        question = Question.objects.create(
            question_text=validated_data['question_text'],
            pub_date=validated_data['pub_date']
        )
        return question
    # return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.pub_date = validated_data.get('pub_date', timezone.now())
        instance.save()
        return instance


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        mode = Choice
        fields = ['choice_text', 'votes']

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.choice_text = validated_data.get('choice_text', None)
        instance.vote = validated_data.get('vote', 0)




