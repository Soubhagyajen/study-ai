import os
import json
import firebase_admin
from firebase_admin import credentials, auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# ─── Firebase Admin SDK Initialization ───────────────────────────────
def initialize_firebase():
    """Initialize Firebase Admin SDK exactly once."""
    if not firebase_admin._apps:
        cred_source = os.environ.get("FIREBASE_CREDENTIALS")
        if cred_source:
            try:
                if cred_source.strip().startswith("{"):
                    cred_dict = json.loads(cred_source)
                    cred = credentials.Certificate(cred_dict)
                else:
                    cred = credentials.Certificate(cred_source)
                firebase_admin.initialize_app(cred)
                print("[OK] Firebase Admin SDK initialized.")
            except Exception as e:
                print(f"[WARNING] Firebase Admin init failed: {e}")
        else:
            # No service account — initialize without credentials for basic usage
            # Token verification will still work if your project ID is correct
            try:
                firebase_admin.initialize_app()
                print("[OK] Firebase Admin SDK initialized (default credentials).")
            except Exception as e:
                print(f"[WARNING] Firebase Admin default init failed: {e}")

# Run initialization at module load
initialize_firebase()


# ─── Token Verification ──────────────────────────────────────────────
def verify_firebase_token(id_token):
    """
    Validate a Firebase ID token against Google's public keys.
    Returns dict with uid, email, name, picture on success; None on failure.
    """
    try:
        decoded = auth.verify_id_token(id_token)
        return {
            "uid": decoded.get("uid"),
            "email": decoded.get("email"),
            "name": decoded.get("name", ""),
            "picture": decoded.get("picture", ""),
            "email_verified": decoded.get("email_verified", False),
        }
    except Exception as e:
        print(f"[ERROR] Firebase token verification failed: {e}")
        return None


# ─── DRF API View ────────────────────────────────────────────────────
class FirebaseLoginView(APIView):
    """
    POST /api/auth/firebase-login/

    Accepts a Firebase ID token, verifies it, creates/retrieves the
    corresponding Django user, and returns Gurukul JWT access + refresh tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response(
                {"error": "id_token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Verify with Firebase Admin SDK
        firebase_user = verify_firebase_token(id_token)
        if firebase_user is None:
            return Response(
                {"error": "Invalid or expired Firebase token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = firebase_user.get("email")
        if not email:
            return Response(
                {"error": "Firebase account has no email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Get-or-create Django user
        from users.models import CustomUser, UserProfile

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "is_student": True,
            },
        )

        if created:
            # Set unusable password — this user authenticates via Google only
            user.set_unusable_password()
            user.save()
            # Create default profile
            UserProfile.objects.get_or_create(user=user)
            print(f"[OK] New Google user created: {email}")

        # 3. Issue Gurukul JWT tokens (same format as email/password login)
        refresh = RefreshToken.for_user(user)
        # Inject custom claims to match GurukulTokenObtainPairSerializer
        refresh["email"] = user.email
        refresh["is_student"] = user.is_student
        if hasattr(user, "profile"):
            refresh["level"] = user.profile.level

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "created": created,
        })
