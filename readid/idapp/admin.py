from django.contrib import admin
from .models import IDData, PaySlipData, LoanApplicationData, EmployerData
# Register your models here.

admin.site.register(IDData)
admin.site.register(PaySlipData)
admin.site.register(LoanApplicationData)
admin.site.register(EmployerData)