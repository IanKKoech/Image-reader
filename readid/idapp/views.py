import base64
import re

import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .forms import ImageUploadForm
from .models import IDData, PaySlipData, LoanApplicationData, EmployerData
from datetime import datetime
from django.contrib import messages
from PIL import Image
import pytesseract


# OpenAI API Key
api_key = "sk-proj-pZZ2JI1H1vYoFkum1OzST3BlbkFJSgKB7EFI0FlLYvNrOv73"

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def process_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist('image')
            loan_amount = request.POST.get('loan_amount')
            loan_tenure = request.POST.get('loan_tenure')

            # Check for 2 images uploaded
            if len(uploaded_files) < 2:
                messages.error(request, 'Please upload at least two images.')
                return redirect(reverse('upload'))

            results = []
            payslip_results = []
            loan_application_detail = []

            loan_application_detail.append(f"Loan Amount: {loan_amount}")
            loan_application_detail.append(f"Loan Tenure: {loan_tenure}")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            # Process the first image using Tesseract OCR
            first_file = uploaded_files[0]
            first_image = Image.open(first_file)
            ocr_text = pytesseract.image_to_string(first_image)
            print(f"OCR Extracted Text: {ocr_text}")

            id_data_instance = IDData()

            # Assuming ocr_text is the output from pytesseract
            # and id_data_instance is an instance of IDData

            # Extract the serial number
            serial_match = re.search(r'\b\d{9}\b', ocr_text)
            if serial_match:
                id_data_instance.serial_number = serial_match.group()
                results.append(f"Serial number: {serial_match.group()}")

            # Extract the ID number for both '1D NUMBER' and 'ID NUMBER'
            id_number_match = re.search(r'(?:1D|ID)\s+NUMBER\s*(\d+)', ocr_text)
            if id_number_match:
                id_data_instance.id_number = id_number_match.group(1)
                results.append(f"ID number: {id_number_match.group(1)}")

            # Extract the full name
            name_match = re.search(r'\b[A-Z]+\s+[A-Z]+\s+[A-Z]+\b', ocr_text)
            if name_match:
                id_data_instance.full_name = name_match.group()
                results.append(f"Full name: {name_match.group()}")

            # Extract the date of birth
            dob_match = re.search(r'\b\d{2}\.\s*\d{2}\.\s*\d{4}\b', ocr_text)
            if dob_match:
                id_data_instance.date_of_birth = dob_match.group()
                results.append(f"Date of birth: {dob_match.group()}")

            # Extract the sex
            sex_match = re.search(r'\bMALE\b|\bFEMALE\b', ocr_text)
            if sex_match:
                id_data_instance.sex = sex_match.group()
                results.append(f"Sex: {sex_match.group()}")

            # Extract the place of birth and district of birth
            place_of_birth_match = re.search(r'PLACE OF .*?\s+([A-Z]+)', ocr_text)
            district_of_birth_match = re.search(r'DISTRICT\s+OF\s+([A-Z]+)', ocr_text)

            if place_of_birth_match:
                id_data_instance.place_of_birth = place_of_birth_match.group(1)
                results.append(f"Place of issue: {place_of_birth_match.group(1)}")

            if district_of_birth_match:
                id_data_instance.district_of_birth = district_of_birth_match.group(1)
                results.append(f"District of birth: {district_of_birth_match.group(1)}")

            # Save the instance to the database
            id_data_instance.save()

            # Print the collected results
            print("These are the results of ID using Tesseract:", results)

            # fields_to_extract = {
            #     'Full names': 'full_name',
            #     'Serial number': 'serial_number',
            #     'ID number': 'id_number',
            #     'Date of birth': 'date_of_birth',
            #     'Sex': 'sex',
            #     'District of birth': 'district_of_birth',
            #     'Place of issue': 'place_of_birth',
            # }
            #
            # for line in ocr_text.split('\n'):
            #     print(f"Processing line: {line}")
            #     for key, value in fields_to_extract.items():
            #         if key.lower() in line.lower():
            #             extracted_value = line.split(':')[-1].strip().replace('*', '')
            #             print(f"Extracted {key}: {extracted_value}")
            #             if value == 'date_of_birth':
            #                 try:
            #                     extracted_value = datetime.strptime(extracted_value, '%d.%m.%Y').date()
            #                 except ValueError:
            #                     print("Date format does not match")
            #             setattr(id_data_instance, value, extracted_value)
            #             results.append(f"{key}: {extracted_value}")
            # print(f"These are the results of ID using teseract :",results)
            # id_data_instance.save()

            # Process the second image using GPT-4 for payslip extraction
            second_file = uploaded_files[1]
            second_base64_image = encode_image(second_file)
            second_payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract payslip information from this image."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{second_base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 200
            }

            try:
                # Handle the second payload
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=second_payload, timeout=30)
                response_data = response.json()
                response_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response content")

                payslip_data_instance = PaySlipData()
                fields_to_extract = {
                    'Teachers Service Commission - Teachers': 'employer',
                    'National Police Service - Police Department': 'employer',
                    'PF-Num': 'pf_num',
                    'Name': 'first_name',
                    'Station': 'station',
                    'ID-Num': 'id_num',
                    'Tax-PIN': 'tax_pin',
                    'Desig': 'designation_id',
                    'RoD': 'retirement_date',
                    'Basic Salary': 'basic_salary',
                    'Rental House Allowance': 'rental_house_allowance',
                    'Hardship Allowance': 'hardship_allowance',
                    'Commuter Allowance': 'commuter_allowance',
                    'TOTAL Deduction': 'total_deductions',
                    'TOTAL Earnings': 'total_earnings',
                }

                for line in response_text.split('\n'):
                    for key, field_name in fields_to_extract.items():
                        if key.lower() in line.lower():
                            extracted_value = line.split(':')[-1].strip().replace('*', '')
                            if field_name == 'employer':
                                employer_name = extracted_value
                                employer, created = EmployerData.objects.get_or_create(name=employer_name)
                                payslip_data_instance.employer = employer
                            else:
                                setattr(payslip_data_instance, field_name, extracted_value)
                            payslip_results.append(f"{key}: {extracted_value}")

                payslip_data_instance.save()

                # Create and save LoanApplicationData instance
                loan_application_instance = LoanApplicationData(
                    loan_amount=loan_amount,
                    loan_tenure=loan_tenure,
                    id_data=id_data_instance,
                    payslip_data=payslip_data_instance
                )
                loan_application_instance.save()

                return render(request, 'upload.html', {
                    'result': results,
                    'payslipResult': payslip_results,
                    'loanApplicationDetail': loan_application_detail
                })

            except requests.exceptions.RequestException as e:
                messages.error(request, 'There was an error processing your request.')
                return redirect(reverse('upload'))
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def read_database(request):
    data = IDData.objects.all()
    return render(request, 'data.html', {'data': data})

def read_payslip_database(request):
    data = PaySlipData.objects.all()
    return render(request, 'payslipData.html', {'data': data})

def read_applications_database(request):
    data = LoanApplicationData.objects.all()
    return render(request, 'applicationsData.html', {'data': data})

def view_application_form(request):
    latest_loan_application = LoanApplicationData.objects.last()
    
    if latest_loan_application:
        id_data = latest_loan_application.id_data
        payslip_data = latest_loan_application.payslip_data
        print("The loan application data :", payslip_data)
        context = {
            'loan_amount': latest_loan_application.loan_amount,
            'loan_tenure': latest_loan_application.loan_tenure,
            'id_data': {
                'full_name': id_data.full_name,
                'serial_number': id_data.serial_number,
                'id_number': id_data.id_number,
                'date_of_birth': id_data.date_of_birth,
                'sex': id_data.sex,
                'district_of_birth': id_data.district_of_birth,
                'place_of_birth': id_data.place_of_birth,
            },
            'payslip_data': {
                'employer': payslip_data.employer,
                'pf_num': payslip_data.pf_num,
                'first_name': payslip_data.first_name,
                'last_name': payslip_data.last_name,
                'station': payslip_data.station,
                'id_num': payslip_data.id_num,
                'tex_pin': payslip_data.tax_pin,
                'rental_house_allowance': payslip_data.rental_house_allowance,
                'basic_salary': payslip_data.basic_salary,
                'total_earnings': payslip_data.total_earnings,
                'total_deductions': payslip_data.total_deductions,
                'designation_id': payslip_data.designation_id,
                'dob': payslip_data.dob,
            },
        }
        return render(request, 'application_form.html', context)
    else:
        messages.error(request, 'No loan application data available.')
        return redirect(reverse('upload'))
