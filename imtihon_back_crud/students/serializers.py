from rest_framework import serializers
from students.models import (
    StudentProfileModel,
    StudentsGroupModel,
    StudentCourseProgressModel,
    StudentAnswerModel,
    StudentCourseModel,
    StudentSessionModel,
    StudentTimetableModel,
    StudentTimeTablesubjectModel,
    CheatingEvidenceModel,
)
from university.models import SubjectModel
from professors.models import ProfessorProfileModel
from university.serializers import SubjectModelSerializer
from professors.serializers import ProfessorProfileModelSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfileModel
        fields = [
            "id",
            "user",
            "student_id_number",
            "image_url",
            "first_name",
            "second_name",
            "third_name",
            "full_name",
            "short_name",
            "birth_date",
            "passport_pin",
            "passport_number",
            "email",
            "phone",
            "gender_code",
            "gender_name",
            "university",
            "department",
            "year_of_study",
        ]


class StudentProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfileModel
        fields = "__all__"


class StudentsGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsGroupModel
        fields = "__all__"


class StudentCourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseModel
        fields = [
            "id",
            "course",
            "student",
            "start_time",
            "end_time",
            "is_completed",
            "grade",
        ]
        read_only_fields = [
            "student",
            "is_completed",
            "grade",
            "start_time",
            "end_time",
        ]

    def validate_course(self, course):
        user = self.context["request"].user
        if not hasattr(user, "student_profile"):
            raise serializers.ValidationError("user is not a student")

        university = user.student_profile.university

        if course.subject.university != university:
            raise serializers.ValidationError("Student cannot attend other's courses")

        return course


class StudentCourseProgressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseProgressModel
        fields = ["id", "student_course", "lesson", "is_completed"]

    def validate_student_course(self, student_course):
        user = self.context["request"].user
        if not hasattr(user, "student_profile"):
            raise serializers.ValidationError("user is not a student")

        if student_course.student != user.student_profile:
            raise serializers.ValidationError("course is not the student's")

        return student_course

    def validate(self, attrs):
        attrs = super().validate(attrs)

        student_course = attrs.get("student_course")
        lesson = attrs.get("lesson")

        if student_course and lesson and lesson.section.course != student_course.course:
            raise serializers.ValidationError(
                "Lesson does not belong to the selected course"
            )

        return attrs


class StudentSessionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSessionModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop("remove_fields", [])
        super().__init__(*args, **kwargs)
        for field in remove_fields:
            self.fields.pop(field, None)


class StudentSessionStartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSessionModel
        fields = ["id", "assignment", "student"]
        read_only_fields = ["student"]


class CheatingEvidenceModelSerializer(serializers.ModelSerializer):
    evidence_file = serializers.FileField(required=True)

    class Meta:
        model = CheatingEvidenceModel
        fields = ["id", "evidence_file", "type", "session"]


class StudentAnswerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswerModel
        fields = "__all__"

    def validate(self, data):
        request = self.context.get("request")
        session = data.get("session")

        if request and session:
            if session.student != request.user.student_profile:
                raise serializers.ValidationError(
                    "You do not have permission to submit an answer for this session."
                )

        if session.end_time is not None:
            raise serializers.ValidationError(
                "This session has already ended. You cannot submit answers."
            )
        # You can also call the earlier question-type validation here
        question = data.get("question")
        if question:
            qtype = question.type  # e.g. "text", "multiple_choice", etc.
            ta = data.get("text_answer")
            ch = data.get("choice")
            tf = data.get("true_false_answer")

            if qtype == "open":
                if not ta or ch or tf is not None:
                    raise serializers.ValidationError(
                        "Invalid answer for text question."
                    )
            elif qtype == "mcq":
                if not ch or ta or tf is not None:
                    raise serializers.ValidationError(
                        "Invalid answer for multiple choice question."
                    )
            elif qtype == "true_false":
                if tf is None or ta or ch:
                    raise serializers.ValidationError(
                        "Invalid answer for true/false question."
                    )

        return data


class StudentTimeTablesubjectModelSerializer(serializers.ModelSerializer):
    subject = SubjectModelSerializer(read_only=True)
    professor = ProfessorProfileModelSerializer(read_only=True)

    class Meta:
        model = StudentTimeTablesubjectModel
        fields = "__all__"


class StudentTimetableModelSerializer(serializers.ModelSerializer):
    subjects = StudentTimeTablesubjectModelSerializer(many=True, read_only=True)

    class Meta:
        model = StudentTimetableModel
        fields = "__all__"
