from rest_framework import serializers


class SvasthyaQuestionTypeSerializer(serializers.Serializer):
    question = serializers.CharField()
    positive = serializers.BooleanField()
    order = serializers.IntegerField()


class SvasthyaQuestionSerializer(serializers.Serializer):
    question = SvasthyaQuestionTypeSerializer()
    response = serializers.IntegerField()


class SvasthyaQuestionnaireSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    date = serializers.DateField()
    score = serializers.IntegerField()
    questions = SvasthyaQuestionSerializer(many=True)


class PrakritiPropertyTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    order = serializers.IntegerField()
