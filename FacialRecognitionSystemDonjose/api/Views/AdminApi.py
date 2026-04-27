from rest_framework import generics
from ..models import Person
from ..serializer.AdminSerializer import PersonUpdateSerializer, PersonSerializer

class PersonUpdateView(generics.UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonUpdateSerializer
    lookup_field = "id" 

# Get all users
class PersonListView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

# Get user by ID
class PersonDetailView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "id"

# Delete user by ID
class PersonDeleteView(generics.DestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "id"
