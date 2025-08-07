from rest_framework import serializers
from professors.models import ProfessorProfileModel, ProfessorsSubjectModel


class ProfessorProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorProfileModel
        fields = '__all__'

class ProfessorsSubjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorsSubjectModel
        fields = '__all__'
