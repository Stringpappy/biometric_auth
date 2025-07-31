from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    face_encoding = models.BinaryField(null=True, blank=True)
    webauthn_credential_id = models.CharField(max_length=512, null=True, blank=True)
    webauthn_public_key = models.TextField(null=True, blank=True)
    webauthn_sign_count = models.IntegerField(default=0)
    
    REQUIRED_FIELDS = ['email']

