from django.urls import path
from .views import RegisterWithFace, FaceLoginView, StartWebAuthnRegister, home, facereg, webauth, face_login

urlpatterns = [
    path('', home, name='home'),
    path('facereg/', facereg, name='facereg'),
    path('face_login/', face_login, name='face_login'),
    path('webauth/', webauth, name='webauth'),
    path('api/register/face/', RegisterWithFace.as_view()),
    path('login/face/', FaceLoginView.as_view()),
    path('register/fingerprint/start/', StartWebAuthnRegister.as_view()),
    # path('register/fingerprint/finish/', ...)  # finish step to be implemented
]




