from rest_framework import serializers
from assignments.models import (
    AssignmentModel,
    AssignmentAttachmentsModel,
    AssignmentsGroupModel,
    QuestionModel,
    QuestionChoiceModel,
)


class AssignmentAttachmentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentAttachmentsModel
        fields = "__all__"


class QuestionChoiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoiceModel
        fields = "__all__"


class QuestionModelSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(read_only=True)
    choices = QuestionChoiceModelSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionModel
        fields = "__all__"


class QuestionCreateSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(queryset=AssignmentModel.objects.all(), write_only=True)
    class Meta:
        model = QuestionModel
        fields = "__all__"


class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentModel
        exclude = ["professor"]


class AssignmentModelSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(read_only=True)
    attachments = AssignmentAttachmentsModelSerializer(many=True, read_only=True)
    questions = QuestionModelSerializer(many=True, read_only=True)

    class Meta:
        model = AssignmentModel
        fields = "__all__"


class AssignmentsGroupModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentsGroupModel
        fields = "__all__"
