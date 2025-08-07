from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from university.models import UniversityModel
from students.models import StudentProfileModel
from professors.models import ProfessorProfileModel
from accounts.models import UniversityUrlsModel
from django.contrib.auth.hashers import check_password
from django.db import transaction, IntegrityError


User = get_user_model()


class UniversityUrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityUrlsModel
        fields = "__all__"


class UniversityRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    university_name = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)
    number = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    website = serializers.URLField(write_only=True)
    description = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "university_name",
            "location",
            "number",
            "email",
            "website",
            "description",
        )

    def create(self, validated_data):
        with transaction.atomic():
            username = validated_data["username"]
            password = validated_data["password"]
            university_name = validated_data.pop("university_name")
            location = validated_data.pop("location")
            number = validated_data.pop("number")
            email = validated_data.pop("email")
            website = validated_data.pop("website")
            description = validated_data.pop("description")
            user = User.objects.create_user(username=username, password=password)
            UniversityModel.objects.create(
                user=user,
                name=university_name,
                location=location,
                number=number,
                email=email,
                website=website,
                description=description,
                longtitude="",
                latitude="",
            )
            return user


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    student_id = serializers.CharField(write_only=True)
    university = serializers.PrimaryKeyRelatedField(
        queryset=UniversityModel.objects.all(), write_only=True
    )
    department = serializers.CharField(write_only=True, required=False)
    year_of_study = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "student_id",
            "university",
            "department",
            "year_of_study",
        )

    def create(self, validated_data):
        with transaction.atomic():
            username = validated_data["username"]
            password = validated_data["password"]
            student_id = validated_data.pop("student_id")
            university = validated_data.pop("university")
            department = validated_data.pop("department", None)
            year_of_study = validated_data.pop("year_of_study", None)
            user = User.objects.create_user(username=username, password=password)
            StudentProfileModel.objects.create(
                user=user,
                student_id=student_id,
                university=university,
                department=department,
                year_of_study=year_of_study,
            )
            return user


class ProfessorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    professor_id = serializers.CharField(write_only=True)
    university = serializers.PrimaryKeyRelatedField(
        queryset=UniversityModel.objects.all(), write_only=True
    )

    class Meta:
        model = User
        fields = ("username", "password", "professor_id", "university")

        def create(self, validated_data):
            try:
                with transaction.atomic():
                    username = validated_data["username"]
                    password = validated_data["password"]
                    professor_id = validated_data.pop("professor_id")
                    university = validated_data.pop("university")

                    user = User(username=username)
                    user.set_password(password)
                    user.save()

                    ProfessorProfileModel.objects.create(
                        user=user,
                        professor_id=professor_id,
                        university=university,
                    )

                    return user

            except IntegrityError as e:
                raise serializers.ValidationError(
                    {"detail": "A database error occurred: " + str(e)}
                )
            except Exception as e:
                raise serializers.ValidationError(
                    {"detail": "Unexpected error: " + str(e)}
                )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        user_model = get_user_model()
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data


class ExternalLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    university_code = serializers.CharField()


class UniversityUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityUrlsModel
        fields = "__all__"
