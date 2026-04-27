import base64
from rest_framework import generics
from .models import Person, Attendance
from .serializers import GetPersonAttendanceSerializer, PersonSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
from .models import Person
from .serializers import PersonSerializer, AttendanceSerializer, RetrievePersonSerializer, UpdateUserPersonSerializer, DeletePersonSerializer
# from deepface import DeepFace
# import tempfile
# import cv2
# import numpy as np
# from django.utils import timezone
# import pytz
from api import serializers
from django.shortcuts import render

def dashboard(request):
    return render(request, "dashboard.html")

class PersonAttendanceByIdAPIView(generics.RetrieveAPIView):
    queryset = Person.objects.prefetch_related('attendance_set')
    serializer_class = serializers.PersonAttendanceSerializer
    lookup_field = 'id'

class DeletePersonAPIView(generics.DestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = DeletePersonSerializer
    lookup_field = 'id'

class UpdatePersonAPIView(generics.RetrieveUpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = UpdateUserPersonSerializer
    lookup_field = 'id'

class GetallpersonAPIView(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all().order_by('name')  # ascending alphabetical


class PersonAttendanceListAPIView(generics.ListAPIView):
    serializer_class = GetPersonAttendanceSerializer

    def get_queryset(self):
        queryset = Person.objects.all()
        person_id = self.request.GET.get('id')  
        if person_id:
            queryset = queryset.filter(id=person_id)
        return queryset

class GetUserByIdAPIView(generics.ListCreateAPIView):
    serializer_class = RetrievePersonSerializer

    def get_queryset(self):
        queryset = Person.objects.all().order_by('-timestamp')
        person_id = self.request.GET.get('id')  
        if person_id:
            queryset = queryset.filter(id=person_id)
        return queryset

class PersonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Person.objects.all().order_by('-timestamp')
    serializer_class = PersonSerializer

# class FaceMatchAPIView(APIView):
#     def post(self, request):
#         upload = request.FILES.get('image')
#         if not upload:
#             return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

#         with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_img:
#             for chunk in upload.chunks():
#                 temp_img.write(chunk)
#             temp_img_path = temp_img.name

#         for person in Person.objects.all():
#             if not person.image:
#                 continue

#             try:
#                 np_arr = np.frombuffer(person.image, np.uint8)
#                 db_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#                 ph_tz = pytz.timezone("Asia/Manila")

#                 with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as db_img_file:
#                     cv2.imwrite(db_img_file.name, db_image)

#                     result = DeepFace.verify(img1_path=temp_img_path, img2_path=db_img_file.name, enforce_detection=False)
                    
#                     if result["verified"]:
#                         timestamp = request.data.get("timestamp")
#                         if not timestamp:
#                             timestamp = timezone.now().astimezone(ph_tz)

#                         attendance = Attendance.objects.create(
#                             person=person,
#                             timestamp=timestamp
#                         )

#                         attendance_data = AttendanceSerializer(attendance).data
                        
#                         return Response(attendance_data, status=status.HTTP_200_OK)

#             except Exception as e:
#                 print(f"Skipping a person due to error: {e}")
#                 continue

#         return Response({"detail": "No matching face found"}, status=status.HTTP_404_NOT_FOUND)
        
#enw attendance model serializer testing

# class AttendanceSerializer(serializers.ModelSerializer):
#     person = serializers.SerializerMethodField()
#     image_upload = serializers.CharField(
#         write_only=True, required=False, allow_blank=True, allow_null=True
#     )

#     class Meta:
#         model = Attendance
#         fields = [
#             'id', 'person',
#             'time_in_am', 'time_out_am',
#             'time_in_pm', 'time_out_pm',
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

#         # Default current time for AM/PM in/out if not provided
#         now = timezone.now()
#         time_in_am = validated_data.get('time_in_am')
#         time_out_am = validated_data.get('time_out_am')
#         time_in_pm = validated_data.get('time_in_pm')
#         time_out_pm = validated_data.get('time_out_pm')

#         return Attendance.objects.create(
#             person=person,
#             time_in_am=time_in_am or now,
#             time_out_am=time_out_am,
#             time_in_pm=time_in_pm,
#             time_out_pm=time_out_pm
#         )


# User submits an excuse
# class ExcuseCreateView(generics.CreateAPIView):
#     serializer_class = ExcuseSerializer
#     permission_classes = [permissions.IsAuthenticated]

# # Admin can list and update excuses
# class ExcuseAdminListUpdateView(generics.ListUpdateAPIView):
#     queryset = Excuse.objects.all()
#     serializer_class = ExcuseSerializer
#     permission_classes = [permissions.IsAdminUser]  # Only admin can update


# class PersonDetailView(APIView):
#     def get(self, request):
#         pk = request.GET.get('id')
#         if not pk:
#             return Response({"error": "ID not provided"}, status=400)
#         try:
#             person = Person.objects.get(pk=pk)
#         except Person.DoesNotExist:
#             return Response({"error": "Person not found"}, status=404)
#         serializer = PersonAttendanceSerializer(person)
#         return Response(serializer.data)

    
# class FaceMatchAPIView(APIView):
#     def post(self, request):
#         upload = request.FILES.get('image')
#         if not upload:
#             return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

#         # Save uploaded image to a temp file
#         with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_img:
#             for chunk in upload.chunks():
#                 temp_img.write(chunk)
#             temp_img_path = temp_img.name

#         # Compare to all saved persons
#         for person in Person.objects.all():
#             if not person.image:
#                 continue

#             try:
#                 # Convert bytes to image
#                 np_arr = np.frombuffer(person.image, np.uint8)
#                 db_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#                 with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as db_img_file:
#                     cv2.imwrite(db_img_file.name, db_image)

#                     result = DeepFace.verify(
#                         img1_path=temp_img_path,
#                         img2_path=db_img_file.name,
#                         enforce_detection=False
#                     )
                    
#                     if result["verified"]:
#                         # Create attendance record
#                         Attendance.objects.create(
#                             person=person,
#                             timestamp=timezone.now()
#                         )

#                         serializer = PersonSerializer(person)
#                         return Response(serializer.data, status=status.HTTP_200_OK)

#             except Exception as e:
#                 print(f"Skipping a person due to error: {e}")
#                 continue

#         return Response({"detail": "No matching face found"}, status=status.HTTP_404_NOT_FOUND)