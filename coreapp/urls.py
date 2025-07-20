from django.urls import path
from .views import RegisterCustomer,CheckEligibility
urlpatterns = [
    path('register',RegisterCustomer.as_view(),name='register-customer'),
    path('check-eligibility',CheckEligibility.as_view(),name='check-eligibility')
]