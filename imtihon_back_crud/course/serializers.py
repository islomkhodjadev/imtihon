from rest_framework import serializers
from course.models import (
    CourseModel,
    CourseSectionModel,
    CourseLessonModel,
    CourseAttachmentsModel,
)


class CourseLessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonModel
        fields = ["id", "section", "name", "text", "video", "image"]

    def validate_section(self, section):
        user = self.context["request"].user

        if hasattr(user, "student_profile"):
            university = user.student_profile.university

        elif hasattr(user, "professor_profile"):
            university = user.professor_profile.university
        elif hasattr(user, "university"):
            university = user.university

        else:
            raise serializers.ValidationError(
                "User is not associated with a university."
            )

        if section.course.subject.university != university:
            raise serializers.ValidationError(
                "You can only assign sections from your own university."
            )

        return section


class CourseSectionModelSerializer(serializers.ModelSerializer):
    lessons = CourseLessonModelSerializer(read_only=True, many=True)

    class Meta:
        model = CourseSectionModel
        fields = [
            "id",
            "course",
            "name",
            "description",
            "intro_video",
            "intro_image",
            "lessons",
        ]

    def validate_course(self, course):
        user = self.context["request"].user

        if hasattr(user, "student_profile"):
            university = user.student_profile.university

        elif hasattr(user, "professor_profile"):
            university = user.professor_profile.university
        elif hasattr(user, "university"):
            university = user.university

        else:
            raise serializers.ValidationError(
                "User is not associated with a university."
            )

        if course.subject.university != university:
            raise serializers.ValidationError(
                "You can only assign courses from your own university."
            )

        return course


class CourseAttachmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAttachmentsModel
        fields = ["id", "course", "attachment_file"]

    def validate_course(self, course):
        user = self.context["request"].user

        if hasattr(user, "student_profile"):
            university = user.student_profile.university

        elif hasattr(user, "professor_profile"):
            university = user.professor_profile.university
        elif hasattr(user, "university"):
            university = user.university

        else:
            raise serializers.ValidationError(
                "User is not associated with a university."
            )

        if course.subject.university != university:
            raise serializers.ValidationError(
                "You can only assign courses from your own university."
            )

        return course


class CourseModelSerializer(serializers.ModelSerializer):
    course_attachments = CourseAttachmentModelSerializer(many=True, read_only=True)

    class Meta:
        model = CourseModel
        fields = [
            "id",
            "subject",
            "intro_image",
            "name",
            "description",
            "course_attachments",
        ]

    def validate_subject(self, subject):
        user = self.context["request"].user

        if hasattr(user, "student_profile"):
            university = user.student_profile.university

        elif hasattr(user, "professor_profile"):
            university = user.professor_profile.university
        elif hasattr(user, "university"):
            university = user.university

        else:
            raise serializers.ValidationError(
                "User is not associated with a university."
            )

        if subject.university != university:
            raise serializers.ValidationError(
                "You can only assign subjects from your own university."
            )

        return subject
