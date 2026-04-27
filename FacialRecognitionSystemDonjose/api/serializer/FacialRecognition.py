from rest_framework import serializers
from ..models import Attendance

class FaceMatchAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "person",
            "timestamp",
            "time_in_am",
            "time_out_am",
            "time_in_pm",
            "time_out_pm"
        ]
