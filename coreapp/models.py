from django.db import models
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    monthly_income = models.FloatField()
    approved_limit = models.FloatField()
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='loans')
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField();
    monthly_installment = models.FloatField()
    repayments_left = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    emis_paid_on_time = models.IntegerField(default=0) #this will come from excel
    
