from celery import shared_task
import pandas as pd
from .models import Customer,Loan
@shared_task
def test_task(name):
    return f"Hello, {name}!"

@shared_task
def ingest_excel_data(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.create(
            first_name=row['First Name'],
            last_name=row['Last Name'],
            age=row['Age'],
            phone_number=row['Phone Number'],
            monthly_income=row['Monthly Salary'],
            approved_limit=row['Approved Limit']
        )
    return f"imported {len(df)} records successfully."    

@shared_task
def ingest_loan_excel(file_path):
    df = pd.read_excel(file_path)
    created_count = 0
    for _, row in df.iterrows():
        try:
            customer=Customer.objects.get(id=row['Customer ID'])
            repayments_left = row['Tenure'] - row['EMIs paid on Time']
            Loan.objects.create(
                customer=customer,
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_installment=row['Monthly payment'],
                repayments_left=repayments_left,
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=row['Date of Approval'],
                end_date=row['End Date']
            )
            created_count+=1
        except Customer.DoesNotExist:
                print(f"Customerwith ID {row['Customer ID']} not found. Skipping")
    return f"Imported {created_count} loan records successfully"
    
