from datetime import timezone
from rest_framework import serializers
from api.models import ExcuseLetter

class ExcuseLetterSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source="person.name", read_only=True)

    class Meta:
        model = ExcuseLetter
        fields = [
            "id",
            "person",
            "person_name",
            "reason",
            "start_date",
            "end_date",
            "submitted_at",
            "status",
        ]
        read_only_fields = ["submitted_at", "status"]
