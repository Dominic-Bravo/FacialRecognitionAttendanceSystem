from rest_framework import generics, status
from rest_framework.response import Response
from api import serializers
from ..models import Person
from ..serializer.Authentication import PersonRegisterSerializer, PersonUpdateInfoSerializer, PinLoginSerializer, ForgotPinSerializer, PersonDetailSerializer

class PersonUpdateInfoView(generics.UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonUpdateInfoSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": f"{instance.name}'s info updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class PersonRegisterView(generics.CreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = serializer.save()
        return Response({
            "success": True,
            "message": "Account created successfully",
            "data": {
                "id": person.id,
                "name": person.name,
                "role": person.role,
                "position": person.position
            }
        }, status=status.HTTP_201_CREATED)

class PinLoginAlldataView(generics.GenericAPIView):
    """
    POST: Login via person ID + 6-digit PIN and retrieve user info + attendance
    """
    serializer_class = PersonDetailSerializer

    def post(self, request):
        person_id = request.data.get("id")
        pin = request.data.get("pin")

        if not person_id or not pin:
            return Response(
                {"error": "Person ID and PIN are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            person = Person.objects.get(id=person_id, pin=pin)
        except Person.DoesNotExist:
            return Response(
                {"error": "Invalid ID or PIN"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PersonDetailSerializer(person)
        return Response(
            {
                "success": True,
                "message": f"Login successful for {person.name}",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ✅ Login via PIN
class PinLoginView(generics.GenericAPIView):
    serializer_class = PinLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = serializer.validated_data['person']
        return Response({
            "success": True,
            "message": f"Login successful for {person.name}",
            "person_id": person.id,
            "name": person.name
        }, status=status.HTTP_200_OK)


# ✅ Reset PIN via security question
class ForgotPinView(generics.GenericAPIView):
    serializer_class = ForgotPinSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = serializer.validated_data['person']
        person.pin = serializer.validated_data['new_pin']
        person.save()
        return Response({
            "success": True,
            "message": "PIN has been reset successfully"
        }, status=status.HTTP_200_OK)
