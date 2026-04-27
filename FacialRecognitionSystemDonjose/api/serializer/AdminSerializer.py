from rest_framework import serializers
from ..models import Person

class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["role", "position", "wage"]

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
            "security_answer",
        ]
        extra_kwargs = {"pin": {"write_only": True}, "security_answer": {"write_only": True}}
