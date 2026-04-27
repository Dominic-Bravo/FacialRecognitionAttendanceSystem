from rest_framework import generics, status
from rest_framework.response import Response
from ..models import Person
from ..serializer.userDataSerializer import PersonDetailSerializer, PersonSerializer



class PersonAttendanceDetailView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonDetailSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        try:
            person = self.get_object()
            serializer = self.get_serializer(person)
            return Response({
                "success": True,
                "message": f"Attendance and info for {person.name}",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)
        
class GetallpersonAPIView(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all().order_by('name')  # ascending alphabetical

