from rest_framework import serializers
from university.models import (
    UniversityModel,
    FacultyModel,
    DepartmentModel,
    GroupModel,
    SubjectModel,
)


class FacultyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyModel
        fields = "__all__"


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = "__all__"


class SubjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectModel
        fields = "__all__"


class DepartmentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepartmentModel
        fields = ["id", "name", "code"]


class UniversityModelSerializer(serializers.ModelSerializer):
    facultys = FacultyModelSerializer(many=True, read_only=True)
    departments = DepartmentModelSerializer(many=True, read_only=True)

    class Meta:
        model = UniversityModel
        fields = "__all__"
