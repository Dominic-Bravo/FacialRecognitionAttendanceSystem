from rest_framework import serializers
from .models import Person, Attendance
from django.utils import timezone
import base64



# retireve left join 
class AttendanceTimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['timestamp']

class PersonAttendanceSerializer(serializers.ModelSerializer):
    attendances = AttendanceTimestampSerializer(many=True, source='attendance_set')

    class Meta:
        model = Person
        fields = ['id', 'name', 'role', 'wage', 'attendances']


# delete methid 
class DeletePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id']

# Update serializer 
# for tthe user only not admin
class UpdateAdminPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'role', 'position', 'wage', 'timestamp']

class UpdateUserPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name']

class GetAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['timestamp']

class GetPersonAttendanceSerializer(serializers.ModelSerializer):
    attendance = GetAttendanceSerializer(source='attendance_set', many=True, read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'role', 'position', 'wage', 'attendance']

#new serializer for testing 
class PersonEmbeddingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'role', 'position', 'timestamp', 'image', 'embedding']
        read_only_fields = ['embedding']  # embedding will be generated automatically

class RetrievePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'role', 'position', 'timestamp']

class PersonSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_upload = serializers.CharField(
        write_only=True, required=False, allow_blank=True, allow_null=True
    )

    class Meta:
        model = Person
        fields = ['id', 'name', 'role', 'position', 'timestamp', 'wage', 'image', 'image_upload']

    def get_image(self, obj):
        if obj.image:
            return base64.b64encode(obj.image).decode('utf-8')
        return None

    def create(self, validated_data):
        image_file = self.context['request'].FILES.get('image')
        image_bytes = image_file.read() if image_file else None
        validated_data['image'] = image_bytes
        return Person.objects.create(**validated_data)


class AttendanceSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()
    image_upload = serializers.CharField(
        write_only=True, required=False, allow_blank=True, allow_null=True
    )

    class Meta:
        model = Attendance
        fields = ['id', 'person', 'timestamp','image_upload'] 

    def get_person(self, obj):
        if obj.person:
            return {
                'id': obj.person.id,
                'name': obj.person.name,
                'role': obj.person.role,
                'position': obj.person.position,
                'wage': obj.person.wage,
                # 'image': base64.b64encode(obj.person.image).decode('utf-8') if obj.person.image else None
            }
        return None

    def create(self, validated_data):
        person = validated_data.get('person')
        if not person:
            raise serializers.ValidationError("Person is required for attendance.")

        timestamp = validated_data.get('timestamp') or timezone.now()

        return Attendance.objects.create(
            person=person,
            timestamp=timestamp
        )

# new attendance model serializer testing

# class AttendanceSerializer(serializers.ModelSerializer):
#     person = serializers.SerializerMethodField()
#     image_upload = serializers.CharField(
#         write_only=True, required=False, allow_blank=True, allow_null=True
#     )

#     class Meta:
#         model = Attendance
#         fields = [
#             'id', 'person',
#             'time_in_am', 'time_out_am', 'status_am',
#             'time_in_pm', 'time_out_pm', 'status_pm',
#             'image_upload'
#         ]

#     def get_person(self, obj):
#         if obj.person:
#             return {
#                 'id': obj.person.id,
#                 'name': obj.person.name,
#                 'role': obj.person.role,
#                 'position': obj.person.position,
#                 'image': base64.b64encode(obj.person.image).decode('utf-8') if obj.person.image else None
#             }
#         return None

#     def create(self, validated_data):
#         person = validated_data.get('person')
#         if not person:
#             raise serializers.ValidationError("Person is required for attendance.")

#         now = timezone.now()
#         time_in_am = validated_data.get('time_in_am')
#         time_out_am = validated_data.get('time_out_am')
#         status_am = 'Present' if time_in_am else 'Absent'

#         time_in_pm = validated_data.get('time_in_pm')
#         time_out_pm = validated_data.get('time_out_pm')
#         status_pm = 'Present' if time_in_pm else 'Absent'

#         return Attendance.objects.create(
#             person=person,
#             time_in_am=time_in_am,
#             time_out_am=time_out_am,
#             status_am=status_am,
#             time_in_pm=time_in_pm,
#             time_out_pm=time_out_pm,
#             status_pm=status_pm
#         )

# exuces ltter models

# class ExcuseSerializer(serializers.ModelSerializer):
#     person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.filter(role='user'), default=None)

#     class Meta:
#         model = Excuse
#         fields = ['id', 'person', 'reason', 'submitted_at', 'status', 'approved_by']
#         read_only_fields = ['submitted_at', 'status', 'approved_by']


    # def create(self, validated_data):
    #     """
    #     This assumes that the view using this serializer has already verified the face
    #     and is passing in the matching Person instance in validated_data.
    #     """
    #     person = validated_data.get('person')
    #     if not person:
    #         raise serializers.ValidationError("Person is required for attendance.")

    #     return Attendance.objects.create(
    #         person=person,
    #         timestamp=validated_data.get('timestamp')
    #     )