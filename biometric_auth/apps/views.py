from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import RegistrationSerializer
import face_recognition
import numpy as np

class RegisterWithFace(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            face_image = face_recognition.load_image_file(request.FILES['face_image'])
            encoding = face_recognition.face_encodings(face_image)
            if not encoding:
                return Response({'error': 'No face detected'}, status=400)
            user.face_encoding = encoding[0].tobytes()
            user.save()
            return Response({'message': 'Registered with face successfully'})
        return Response(serializer.errors, status=400)


from webauthn.helpers.structs import PublicKeyCredentialCreationOptions
from django.conf import settings
from django.core.cache import cache
from webauthn.helpers import options_to_json

class StartWebAuthnRegister(APIView):
    def post(self, request):
        username = request.data['username']
        user = CustomUser.objects.get(username=username)
        challenge = os.urandom(32)

        # Store challenge temporarily
        cache.set(f"webauthn_challenge_{user.id}", challenge, timeout=300)

        options = PublicKeyCredentialCreationOptions(
            rp={"name": "Biometric App"},
            user={"id": str(user.id).encode(), "name": user.username, "displayName": user.username},
            challenge=challenge,
            pub_key_cred_params=[{"type": "public-key", "alg": -7}],
        )
        return Response(options_to_json(options))


class FaceLoginView(APIView):
    def post(self, request):
        image = request.FILES['face_image']
        face_image = face_recognition.load_image_file(image)
        face_encodings = face_recognition.face_encodings(face_image)

        if not face_encodings:
            return Response({"error": "No face detected"}, status=400)

        input_encoding = face_encodings[0]

        for user in CustomUser.objects.exclude(face_encoding=None):
            user_encoding = np.frombuffer(user.face_encoding)
            match = face_recognition.compare_faces([user_encoding], input_encoding)[0]
            if match:
                return Response({"message": "Face login successful", "user": user.username})
        return Response({"error": "Face not recognized"}, status=401)


from django.shortcuts import render
def home(request):
    return render(request, 'home.html')



def webauth(request):
    return render(request, 'webauth_register.html')

def facereg(request):
    return render(request, 'face_register.html')
