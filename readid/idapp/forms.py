from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    loan_amount = forms.CharField(max_length=100, required=True)
    loan_tenure = forms.CharField(max_length=100, required=True)
