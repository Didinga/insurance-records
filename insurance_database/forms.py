from django import forms
from .models import InsuredPerson, User, InsuranceDetail

class InsuredPersonForm(forms.ModelForm):
    detail_insurance = forms.ModelMultipleChoiceField(queryset=InsuranceDetail.objects.all(), required=False)

    class Meta:
        model = InsuredPerson
        fields = ["first_name", "last_name", "age", "address", "insurance", "detail_insurance"]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
