from rest_framework import serializers

from .models import User, Student, Category, Course
from .mixins import BaseMixinSerializer


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["phone", "date_of_birth", "city"]


class RegisterSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "student"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("student")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.role = User.Roles.STUDENT
        user.save()
        Student.objects.create(user=user, **profile_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role == User.Roles.STUDENT:
            student = Student.objects.filter(user=instance).first()
            data["profile"] = StudentSerializer(student).data if student else None
        return data


class CategorySerializer(BaseMixinSerializer):
    class Meta(BaseMixinSerializer.Meta):
        model = Category
        fields = BaseMixinSerializer.Meta.fields + ["label"]


class CourseSerializer(BaseMixinSerializer):
    class Meta(BaseMixinSerializer.Meta):
        model = Course
        fields = BaseMixinSerializer.Meta.fields + [
            "title",
            "description",
            "image",
            "category",
        ]
