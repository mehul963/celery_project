from django import forms
from django.contrib.auth.hashers import make_password
from dashboard.models import CustomUser
from .models import Lead

class UserCreationForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields = ('email', 'password')
    
    def save(self,commit:bool=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        
        return user

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'phone']


        