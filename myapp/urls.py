from django.urls import path
from .views import (
    RegisterView,
    VerifyOtpView,
    LoginView,
    ForgotPasswordView,
    ChangePasswordView,
    LogoutView,
    ResendOtpView,
    get_all_category

)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOtpView.as_view(), name='resend-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get_all_category/' , get_all_category , name= 'cate')

   
    
]
