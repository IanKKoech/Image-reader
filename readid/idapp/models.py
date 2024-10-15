from django.db import models

class IDData(models.Model):
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.CharField(max_length=100, null=True, blank=True)  
    sex = models.CharField(max_length=10, null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    district_of_birth = models.CharField(max_length=100, null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.full_name or "ID Data"


class EmployerData(models.Model):
    pf_num = models.CharField(unique=True, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    designation_id = models.CharField(max_length=100, null=True)
    disability_exemption = models.BooleanField(default=False)
    station = models.CharField(max_length=100, null=True)
    id_num = models.CharField(max_length=100, null=True)
    tax_pin = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    employer_id = models.IntegerField(null=True) # replace with Employer foreign key
    employment_date = models.DateField(null=True)
    retirement_date = models.DateField(null=True)
    bank_name = models.CharField(max_length=100, null=True)
    bank_branch = models.CharField(max_length=100, null=True)

class Designation(models.Model):
    designation_id = models.AutoField(primary_key=True)
    employer_id = models.IntegerField(null=True) # replace with Employer foreign key
    designation = models.CharField(max_length=100, null=True)

class Employer(models.Model):
    employer_id = models.AutoField(primary_key=True)
    employer_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=100, null=True)
    contact_details = models.CharField(max_length=100, null=True)
    other_info = models.TextField(null=True)

class AllowanceTypes(models.Model):
    allowance_type = models.AutoField(primary_key=True)
    employer_id = models.IntegerField(null=True) # replace with Employer foreign key
    allowance_name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)


class PaySlipData(models.Model):
    pf_num = models.CharField(max_length=100, unique=True, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    designation_id = models.CharField(max_length=100, null=True)
    disability_exemption = models.BooleanField(default=False)
    station = models.CharField(max_length=100, null=True)
    id_num = models.CharField(max_length=100, unique=True, null=True)
    tax_pin = models.CharField(max_length=100, null=True)
    dob = models.CharField(max_length=100, null=True)
    employer = models.CharField(max_length=100, null=True, blank=True)
    employment_date = models.CharField(max_length=100,null=True, blank=True)
    retirement_date = models.CharField(max_length=100, null=True, blank=True)
    # Additional fields
    basic_salary = models.CharField(max_length=100, null=True, blank=True)
    rental_house_allowance = models.CharField(max_length=100, null=True, blank=True)
    commuter_allowance = models.CharField(max_length=100, null=True, blank=True)
    total_deductions = models.CharField(max_length=100, null=True, blank=True)
    total_earnings = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pf_num}"


class LoanApplicationData(models.Model):
    id = models.AutoField(primary_key=True)
    loan_amount = models.CharField(max_length=100, default="0.00", null=True, blank=True)
    loan_tenure = models.CharField(max_length=100, default="N/A", null=True, blank=True)  
    id_data = models.ForeignKey(IDData, on_delete=models.CASCADE, null=True, blank=True)
    payslip_data = models.ForeignKey(PaySlipData, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.loan_amount} {self.loan_tenure}"

