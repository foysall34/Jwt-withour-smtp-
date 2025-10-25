from django.urls import path
from .views import (
    RegisterView,
    VerifyOtpView,
    LoginView,
    ForgotPasswordView,
    ChangePasswordView,
    LogoutView,
    ResendOtpView,


)

from . import views 


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOtpView.as_view(), name='resend-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
   
#  -------------------------  urls ------------------------

    path('categories/', views.category_list_create),
    path('categories/<int:pk>/', views.category_detail),

    path('products/', views.product_list_create),
    path('products/<int:pk>/', views.product_detail),

    path('customers/', views.customer_list_create),
    path('customers/<int:pk>/', views.customer_detail),

   
    
]
