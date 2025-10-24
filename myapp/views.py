import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import (
    RegisterSerializer,
    VerifyOtpSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ChangePasswordSerializer,
    ResendOtpSerializer
)

User = get_user_model()


# ===========================
# Register View
# ===========================
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully. Check terminal for OTP.'}, status=201)
        return Response(serializer.errors, status=400)


# ===========================
# OTP Verify View
# ===========================
class VerifyOtpView(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                if user.otp == otp:
                    user.otp = None
                    user.is_active = True
                    user.save()
                    return Response({'message': 'OTP verified successfully '})
                return Response({'error': 'Invalid OTP'}, status=400)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        return Response(serializer.errors, status=400)



class ResendOtpView(APIView):
    def post(self, request):
        serializer = ResendOtpSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            print(email)
            try:
                user = User.objects.get(email=email)

                new_otp = str(random.randint(100000, 999999))
                user.otp = new_otp
                user.save()

                print(f"New OTP for {user.email} is: {new_otp}")

                return Response(
                    {"message": "OTP resent successfully.check your terminal"},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===========================
# Login View
# ===========================
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'role': user.role
            })
        return Response(serializer.errors, status=400)


# ===========================
# Forgot Password View
# ===========================
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                user.otp = str(random.randint(100000, 999999))
                user.save()
                print(f"Password reset OTP for {email}: {user.otp}")
                return Response({'message': 'OTP sent to terminal '})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        return Response(serializer.errors, status=400)


# ===========================
# Change Password View
# ===========================
class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                if user.otp == otp:
                    user.set_password(new_password)
                    user.otp = None
                    user.save()
                    return Response({'message': 'Password changed successfully '})
                return Response({'error': 'Invalid OTP'}, status=400)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        return Response(serializer.errors, status=400)


# ===========================
# Logout View
# ===========================
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful '})
        except Exception:
            return Response({'error': 'Invalid token'}, status=400)




from .serializers import CategorySerializers , ProductSerializers
from rest_framework.decorators import api_view , permission_classes

from .models import Category , Product



@api_view(['GET' , 'POST'])
def get_all_category(request):



    if request.method == 'GET':
        all_category = Category.objects.all()

        serarc_value =  request.GET.get('s') 
        print(serarc_value)
        if serarc_value :
            all_category = Category.objects.filter(name__icontains = serarc_value)


        serializers = CategorySerializers(all_category , many = True)
        return Response(serializers.data)




    
