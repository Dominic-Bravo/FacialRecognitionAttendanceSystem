from rest_framework import serializers
from ..models import Person, Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "timestamp",
            "time_in_am",
            "time_out_am",
            "time_in_pm",
            "time_out_pm",
            "remarks",
        ]


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
            # ⚠️ security_answer excluded for security reasons
            "attendances",
        ]

class PersonSerializer(serializers.ModelSerializer):
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
        ]
