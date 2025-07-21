from django.urls import path
from .views import RegisterCustomer,CheckEligibility,CreateLoan,Viewloan,ViewCustomerLoans
urlpatterns = [
    path('register',RegisterCustomer.as_view(),name='register-customer'),
    path('check-eligibility',CheckEligibility.as_view(),name='check-eligibility'),
    path('create-loan', CreateLoan.as_view(), name='create-loan'),
    path('view-loan/<int:loan_id>',Viewloan.as_view(),name='view-loan'),
    path('view-loans/<int:customer_id>',ViewCustomerLoans.as_view(),name='view-loans')

]