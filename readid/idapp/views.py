import base64
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .forms import ImageUploadForm
from .models import IDData
from datetime import datetime
from django.contrib import messages

# OpenAI API Key
api_key = "sk-proj-pZZ2JI1H1vYoFkum1OzST3BlbkFJSgKB7EFI0FlLYvNrOv73"

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def process_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            base64_image = encode_image(image)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What’s in this image?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            try:
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
                response_data = response.json()
                response_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response content")

                # Process and insert data into the database
                id_data_instance = IDData()

                fields_to_extract = {
                    'Full names': 'full_name',
                    'Serial number': 'serial_number',
                    'ID number': 'id_number',
                    'Date of birth': 'date_of_birth',
                    'Sex': 'sex',
                    'District of birth': 'district_of_birth',
                    'Place of issue': 'place_of_birth',
                    'Date of issue': None  # This field may not be present in all responses
                }

                for line in response_text.split('\n'):
                    for key, value in fields_to_extract.items():
                        if key.lower() in line.lower():
                            extracted_value = line.split(':')[-1].strip()
                            print(f"Extracted {key}: {extracted_value}")
                            if value:  # Ensure value is not None
                                if key == 'Date of birth':
                                    try:
                                        datetime.strptime(extracted_value, '%d.%m.%Y').date()
                                    except ValueError:
                                        pass  # Handle invalid date format gracefully
                                setattr(id_data_instance, value, extracted_value)

                id_data_instance.save()

                # Set success notification
                messages.success(request, 'Image uploaded and processed successfully.')
                return redirect(reverse('data'))

            except requests.Timeout:
                # Set error notification
                messages.error(request, 'The request timed out. Please try again with a smaller image or check your network connection.')
                return redirect(reverse('upload'))
            except Exception as e:
                # Set error notification
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect(reverse('upload'))
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'})

    form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def process_logbook_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            base64_image = encode_image(image)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What’s in this image?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            


def read_database(request):
    data = IDData.objects.all()
    return render(request, 'data.html', {'data': data})
