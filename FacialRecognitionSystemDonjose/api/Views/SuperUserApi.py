from rest_framework import generics
from api.serializer.SuperUser import SuperUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SuperUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SuperUserSerializer