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

    PRAKRITI_CATEGORY_CHOICES = (
        ('AN', 'Anatomical'),
        ('PH', 'Physiological'),
        ('PS', 'Psychological')
    )

    id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.ChoiceField(choices=PRAKRITI_CATEGORY_CHOICES)
    order = serializers.IntegerField()


class PrakritiOptionTypeSerializer(serializers.Serializer):

    PRAKRITI_PROPERTY_CHOICES = (
        ('v', 'Vatika'),
        ('p', 'Paittika'),
        ('k', 'Kaphaja')
    )

    id = serializers.IntegerField()
    name = serializers.CharField()
    property_id = serializers.IntegerField()
    prakṛti_type = serializers.ChoiceField(choices=PRAKRITI_PROPERTY_CHOICES)


class PrakritiPropertySerializer(serializers.Serializer):
    property = PrakritiPropertyTypeSerializer()
    option = PrakritiOptionTypeSerializer()


class PrakritiQuestionnaireSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    date = serializers.DateField()
    vatika_score = serializers.IntegerField()
    paittika_score = serializers.IntegerField()
    kaphaja_score = serializers.IntegerField()
    properties = PrakritiPropertySerializer(many=True)
