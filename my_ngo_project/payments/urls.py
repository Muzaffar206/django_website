from django.urls import path
from . import views

urlpatterns = [
    path('create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
]