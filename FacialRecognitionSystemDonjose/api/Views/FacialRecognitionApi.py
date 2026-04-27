from datetime import datetime, time
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ..models import Person, Attendance
from ..serializer.FacialRecognition import FaceMatchAttendanceSerializer
import tempfile
import numpy as np
import cv2
from deepface import DeepFace
import pytz

class FaceRecognitionWithIdAPIView(APIView):
    def post(self, request):
        person_id = request.data.get("person_id")
        if not person_id:
            return Response({"error": "person_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        upload = request.FILES.get("image")
        if not upload:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Get person by ID
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        if not person.image:
            return Response({"error": "This person has no stored image"}, status=status.HTTP_400_BAD_REQUEST)

        # Save uploaded image temporarily
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_img:
            for chunk in upload.chunks():
                temp_img.write(chunk)
            temp_img_path = temp_img.name

        try:
            # Decode DB image
            np_arr = np.frombuffer(person.image, np.uint8)
            db_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Force PH timezone
            ph_tz = pytz.timezone("Asia/Manila")

            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as db_img_file:
                cv2.imwrite(db_img_file.name, db_image)

                result = DeepFace.verify(
                    img1_path=temp_img_path,
                    img2_path=db_img_file.name,
                    enforce_detection=False
                )

                if result["verified"]:
                    timestamp = request.data.get("timestamp")

                    if not timestamp:
                        # Always localize timestamp to PH time
                        timestamp = timezone.localtime(timezone.now(), ph_tz)       
                    else:
                        # If client sends string timestamp → localize to PH time
                        timestamp = timezone.make_aware(
                            datetime.fromisoformat(timestamp),
                            ph_tz
                        )

                    today = timestamp.date()  # use PH-local date
                    attendance, created = Attendance.objects.get_or_create(
                        person=person,
                        timestamp__date=today,
                        defaults={"timestamp": timestamp}
                    )

                    hour = timestamp.hour
                    action_message = None

                    # ----- AM LOGIC -----
                    if 8 <= hour < 12:
                        if not attendance.time_in_am:
                            if hour < 8:  # deny before 8:00 AM
                                return Response(
                                    {"success": False, "message": "AM time-in not allowed before 8:00 AM"},
                                    status=status.HTTP_403_FORBIDDEN
                                )
                            attendance.time_in_am = timestamp
                            action_message = "AM time-in recorded successfully"
                        else:
                            attendance.time_out_am = timestamp
                            action_message = "AM time-out recorded successfully"

                    # ----- PM LOGIC -----
                    elif 13 <= hour < 18:
                        if attendance.time_in_am and not attendance.time_out_am:
                            attendance.time_out_am = datetime.combine(today, time(12, 0, tzinfo=ph_tz))

                        if not attendance.time_in_pm:
                            if hour < 13:  # deny before 1:00 PM
                                return Response(
                                    {"success": False, "message": "PM time-in not allowed before 1:00 PM"},
                                    status=status.HTTP_403_FORBIDDEN
                                )
                            attendance.time_in_pm = timestamp
                            action_message = "PM time-in recorded successfully"
                        else:
                            attendance.time_out_pm = timestamp
                            action_message = "PM time-out recorded successfully"

                    # ----- AFTER 5 PM LOGIC -----
                    elif hour >= 18:
                        if attendance.time_in_pm and not attendance.time_out_pm:
                            attendance.time_out_pm = datetime.combine(today, time(17, 0, tzinfo=ph_tz))
                            action_message = "Auto-set PM time-out to 5:00 PM"
                        else:
                            action_message = "Already logged out for today"

                    attendance.save()

                    return Response({
                        "success": True,
                        "message": action_message,
                        "data": FaceMatchAttendanceSerializer(attendance).data
                    }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error verifying face: {e}")
            return Response({"error": "Face recognition failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Face not verified"}, status=status.HTTP_400_BAD_REQUEST)




# class FaceRecognitionwithoutIdAPIView(APIView):
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

#                         # Get today's attendance (or create if missing)
#                         today = timezone.localdate()
#                         attendance, created = Attendance.objects.get_or_create(
#                             person=person,
#                             timestamp__date=today,
#                             defaults={"timestamp": timestamp}
#                         )

#                         hour = timestamp.hour

#                         # ----- AM LOGIC -----
#                         if 8 <= hour < 12:
#                             if not attendance.time_in_am:
#                                 attendance.time_in_am = timestamp
#                             else:
#                                 attendance.time_out_am = timestamp

#                         # ----- PM LOGIC -----
#                         elif 13 <= hour < 18:  # within working hours
#                             # Auto-fix AM timeout if missing
#                             if attendance.time_in_am and not attendance.time_out_am:
#                                 attendance.time_out_am = datetime.combine(today, time(12, 0, tzinfo=ph_tz))

#                             if not attendance.time_in_pm:
#                                 attendance.time_in_pm = timestamp
#                             else:
#                                 attendance.time_out_pm = timestamp

#                         # ----- AFTER 5 PM LOGIC -----
#                         elif hour >= 18:
#                             # If they missed PM timeout, auto-set to 5:00 PM
#                             if attendance.time_in_pm and not attendance.time_out_pm:
#                                 attendance.time_out_pm = datetime.combine(today, time(17, 0, tzinfo=ph_tz))

#                         attendance.save()
#                         return Response(FaceMatchAttendanceSerializer(attendance).data, status=status.HTTP_200_OK)

#             except Exception as e:
#                 print(f"Skipping a person due to error: {e}")
#                 continue

#         return Response({"detail": "No matching face found"}, status=status.HTTP_404_NOT_FOUND)






# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.utils import timezone
# from models import Person, Attendance
# from serializer.FacialRecognition import FaceMatchAttendanceSerializer
# import tempfile
# import numpy as np
# import cv2
# from deepface import DeepFace
# import pytz




# class FaceRecognitionAPIView(APIView):
#     """
#     POST: Upload an image to verify and mark attendance
#     """

#     def post(self, request):
#         upload = request.FILES.get("image")
#         if not upload:
#             return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

#         # Save uploaded image temporarily
#         with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_img:
#             for chunk in upload.chunks():
#                 temp_img.write(chunk)
#             temp_img_path = temp_img.name

#         # Timezone
#         ph_tz = pytz.timezone("Asia/Manila")

#         for person in Person.objects.all():
#             if not person.image:
#                 continue

#             try:
#                 # Decode person image from DB
#                 np_arr = np.frombuffer(person.image, np.uint8)
#                 db_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#                 with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as db_img_file:
#                     cv2.imwrite(db_img_file.name, db_image)

#                     # Verify face
#                     result = DeepFace.verify(img1_path=temp_img_path, img2_path=db_img_file.name, enforce_detection=False)
                    
#                     if result["verified"]:
#                         # Timestamp
#                         timestamp = request.data.get("timestamp")
#                         if not timestamp:
#                             timestamp = timezone.now().astimezone(ph_tz)

#                         # Create attendance
#                         attendance = Attendance.objects.create(
#                             person=person,
#                             timestamp=timestamp
#                         )

#                         serializer = FaceMatchAttendanceSerializer(attendance)
#                         return Response(serializer.data, status=status.HTTP_200_OK)

#             except Exception as e:
#                 print(f"Skipping person {person.name} due to error: {e}")
#                 continue

#         return Response({"detail": "No matching face found"}, status=status.HTTP_404_NOT_FOUND)
