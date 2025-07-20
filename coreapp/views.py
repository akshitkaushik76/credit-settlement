from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Loan
from .serializers import CustomerSerializer
from datetime import date
import math

class RegisterCustomer(APIView):
    def post(self,request):
        data = request.data
        income = int(data.get('monthly_income',0))
        approved_limit = round((36*income)/100000)*100000
        data['approved_limit'] = approved_limit
        serializer = CustomerSerializer(data = data)

        if serializer.is_valid():
            customer = serializer.save()
            return Response({
                "customer_id":customer.id,
                "name":f"{customer.first_name} {customer.last_name}",
                "age":customer.age,
                "monthly_income":customer.monthly_income,
                "approved_limit":customer.approved_limit,
                "phone_number":customer.phone_number
            },status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CheckEligibility(APIView):
    def post(self,request):
        data  = request.data
        customer_id = data.get("customer_id")
        loan_amount = float(data.get("loan_amount"))
        interest_rate = float(data.get("interest_rate"))
        tenure = int(data.get("tenure"))
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return response({"error":"Customer not found"},status=404)
        loans = Loan.objects.filter(customer=customer)
        current_year = date.today().year
        total_emi = 0
        score = 100

        total_debt = sum(loan.loan_amount for loan in loans)
        if total_debt > customer.approved_limit:
            score = 0
        emis_on_time = sum(loan.emis_paid_on_time for loan in loans)
        if emis_on_time < len(loans)*tenure:
            score-=10
        if len(loans) > 5:
            score-=10
        if loans.filter(start_date__year = current_year).count()>1:
            score-=10
        if total_debt > 10_00_000:
            score-=5
        for loan in loans:
            total_emi+=loan.monthly_installement
        monthly_salary = customer.monthly_income
        if total_emi > 0.5* monthly_salary:
            return Response({
                "customer_id":customer.id,
                "approval":False,
                "reason":"Total EMI exceeds 50% of monthly salary"
            })    

        r = interest_rate / (12*100)
        monthly_installment = loan_amount * r * (1+r)**tenure/((1+r)**tenure - 1)
        approved = False
        corrected_interest = interest_rate
        if score > 50:
            approved = True
        elif 30<score<=50:
            if interest_rate >=12:
                approved = True
            else:
                corrected_interest = 12
        elif 10<score<=30:
            if interest_rate>=16:
                approved = True
            else:
                corrected_interest = 16    
        else:
            approved = False
        return Response({
            "customer_id":customer_id,
            "approval":approved,
            "interest_rate":interest_rate,
            "corrected_interest_rate":corrected_interest,
            "tenure":tenure,
            "monthly_installment":round(monthly_installment,2)
        })                                                        