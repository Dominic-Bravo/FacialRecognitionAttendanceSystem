from django.urls import path
from .views import PersonAttendanceListAPIView, PersonListCreateAPIView, UpdatePersonAPIView, dashboard
from .Views.ExcuseletterApi import ExcuseLetterCreateView
from .Views.AuthenticationApi import PersonRegisterView, PersonUpdateInfoView, PinLoginView, ForgotPinView, PinLoginAlldataView
from .Views.AdminApi import PersonUpdateView, PersonListView, PersonDetailView, PersonDeleteView
from .Views.FacialRecognitionApi import FaceRecognitionWithIdAPIView
from .Views.userDataApi import PersonAttendanceDetailView, GetallpersonAPIView
from .Views.SuperUserApi import SuperUserCreateView
from api import views

urlpatterns = [
    path("", dashboard, name="dashboard"),
    # Person endpoints
    path('persons/', PersonListCreateAPIView.as_view(), name='person-list-create'),
    path('updatePerson/<int:id>/', UpdatePersonAPIView.as_view(), name='update-person'),
    path('deletePerson/<int:id>/', views.DeletePersonAPIView.as_view(), name='delete-person'),
    path('getUserAttendance/', PersonAttendanceListAPIView.as_view(), name='person-attendance'),
    path('getAttendanceById/<int:id>/', views.PersonAttendanceByIdAPIView.as_view(), name='attendance'),

    # Face recognition
    #path('face-match/', FaceMatchAPIView.as_view(), name='face-match'),

        # Face recognition and attendance marking new apu url POST
    path("facial-recognition/", FaceRecognitionWithIdAPIView.as_view(), name="face-match-withID"),
    # face recognition and attendance marking PUT

    # Excuse letter endpoints
    path("excuse-letters/create/", ExcuseLetterCreateView.as_view(), name="excuse-create"),
    # path("excuse-letters/list/", ExcuseLetterListView.as_view(), name="excuse-list"),
    # path("excuse-letters/<int:pk>/approve/", ExcuseLetterApproveView.as_view(), name="excuse-approve"),
    # path("excuse-letters/<int:pk>/reject/", ExcuseLetterRejectView.as_view(), name="excuse-reject"),

    # Authentication endpoints this enndpoint if successs it will retreieve all the data of the user
    # POST → Login via PIN and retrieve user + attendance
    path("auth/pin-login/", PinLoginAlldataView.as_view(), name="pin-login-all-data"),

     # POST → Login using PIN can be done by any user offline
    path("auth/pin-login-simple/", PinLoginView.as_view(), name="pin-login"),

    # POST → Reset PIN using security question
    path("auth/forgot-pin/", ForgotPinView.as_view(), name="forgot-pin"),

    # POST → Register new user
    path("register/", PersonRegisterView.as_view(), name="person-register"),
    # PUT → Update personal info (name, position, security question/answer) - no role/wage/pin
    path("person/update-info/<int:id>/", PersonUpdateInfoView.as_view(), name="person-update-info"),


    # Admin endpoints can be added here
    path("person/<int:id>/update/", PersonUpdateView.as_view(), name="person-update"),
    path("persons/", PersonListView.as_view(), name="person-list"),          # GET: all users
    path("person/<int:id>/", PersonDetailView.as_view(), name="person-detail"),  # GET: user by ID
    path("person/<int:id>/delete/", PersonDeleteView.as_view(), name="person-delete"),  # DELETE user

    #user data
    path("person/attendance/<int:id>/", PersonAttendanceDetailView.as_view(), name="person-attendance-detail"),

    # SuperUser creation endpoint
    path("create-superuser/", SuperUserCreateView.as_view(), name="create-superuser"),

]
