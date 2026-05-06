from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Ashram - User Settings & Profile logic.
    Thin view yielding standard GET & PUT via robust serializer.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Forces resolution strictly to the `request.user` to avoid permission tampering
        return self.request.user

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class GurukulTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends default JWT payload with Gurukul specific context (claims).
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims for frontend consumption
        token['email'] = user.email
        token['is_student'] = user.is_student
        
        # Avoid breaking if profile isn't fully migrated yet
        if hasattr(user, 'profile'):
            token['level'] = user.profile.level
            
        return token

class GurukulTokenObtainPairView(TokenObtainPairView):
    """
    Uses the enhanced Gurukul Payload Token Serializer.
    """
    serializer_class = GurukulTokenObtainPairSerializer
