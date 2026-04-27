from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import ExcuseLetter
from ..serializer.ExcuseLetter import ExcuseLetterSerializer

# ✅ Submit excuse (any user)
class ExcuseLetterCreateView(generics.CreateAPIView):
    queryset = ExcuseLetter.objects.all()
    serializer_class = ExcuseLetterSerializer
    permission_classes = [permissions.AllowAny]


# # ✅ List all excuses (any user, admin can filter)
# class ExcuseLetterListView(generics.ListAPIView):
#     queryset = ExcuseLetter.objects.all().order_by("-submitted_at")
#     serializer_class = ExcuseLetterSerializer
#     permission_classes = [permissions.AllowAny]


# # ✅ Approve excuse (admin only)
# class ExcuseLetterApproveView(generics.UpdateAPIView):
#     queryset = ExcuseLetter.objects.all()
#     serializer_class = ExcuseLetterSerializer
#     permission_classes = [permissions.IsAdminUser]

#     def update(self, request, *args, **kwargs):
#         excuse = self.get_object()
#         excuse.status = "APPROVED"
#         excuse.save()
#         serializer = self.get_serializer(excuse)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# # ✅ Reject excuse (admin only)
# class ExcuseLetterRejectView(generics.UpdateAPIView):
#     queryset = ExcuseLetter.objects.all()
#     serializer_class = ExcuseLetterSerializer
#     permission_classes = [permissions.IsAdminUser]

#     def update(self, request, *args, **kwargs):
#         excuse = self.get_object()
#         excuse.status = "REJECTED"
#         excuse.save()
#         serializer = self.get_serializer(excuse)
#         return Response(serializer.data, status=status.HTTP_200_OK)
