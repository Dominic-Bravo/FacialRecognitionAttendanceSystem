from datetime import datetime
import time
from rest_framework import serializers
from ..models import Person, Attendance
from django.contrib.auth.hashers import make_password, check_password

class PersonUpdateInfoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # accept file uploads

    class Meta:
        model = Person
        fields = ["image", "name"]

    def update(self, instance, validated_data):
        # Handle image separately
        image_file = validated_data.pop("image", None)
        if image_file:
            instance.image = image_file.read()  # store as binary (bytes)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PersonRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "name",
            "role",
            "position",
            "pin",
            "security_question",
            "security_answer"
        ]
        extra_kwargs = {
            "pin": {"write_only": True},
            "security_answer": {"write_only": True}
        }

class AttendanceSerializer(serializers.ModelSerializer):
    time_out_am_display = serializers.SerializerMethodField()
    time_out_pm_display = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "timestamp",
            "time_in_am",
            "time_out_am",
            "time_in_pm",
            "time_out_pm",
            "time_out_am_display",
            "time_out_pm_display",
        ]

    def get_time_out_am_display(self, obj):
        """Return actual time_out_am or default 12:00 if not set"""
        if obj.time_in_am and not obj.time_out_am:
            return datetime.combine(obj.time_in_am.date(), time(12,0))
        return obj.time_out_am

    def get_time_out_pm_display(self, obj):
        """Return actual time_out_pm or default 17:00 if not set"""
        if obj.time_in_pm and not obj.time_out_pm:
            return datetime.combine(obj.time_in_pm.date(), time(17,0))
        return obj.time_out_pm
    

class PersonDetailSerializer(serializers.ModelSerializer):
    attendances = AttendanceSerializer(source="attendance_set", many=True, read_only=True)

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "role",
            "position",
            "wage",
            "timestamp",
            "pin",
            "security_question",
            "attendances",
        ]
        extra_kwargs = {"pin": {"write_only": True}}

class PinLoginSerializer(serializers.Serializer):
    person_id = serializers.IntegerField()
    pin = serializers.CharField(max_length=6, min_length=6)

    def validate(self, data):
        try:
            person = Person.objects.get(id=data['person_id'])
        except Person.DoesNotExist:
            raise serializers.ValidationError("Person not found")

        if person.pin != data['pin']:
            raise serializers.ValidationError("Invalid PIN")
        
        data['person'] = person
        return data


class ForgotPinSerializer(serializers.Serializer):
    person_id = serializers.IntegerField()
    security_answer = serializers.CharField(max_length=255)
    new_pin = serializers.CharField(max_length=6, min_length=6)

    def validate(self, data):
        try:
            person = Person.objects.get(id=data['person_id'])
        except Person.DoesNotExist:
            raise serializers.ValidationError("Person not found")

        if person.security_answer != data['security_answer']:
            raise serializers.ValidationError("Incorrect security answer")

        data['person'] = person
        return data
