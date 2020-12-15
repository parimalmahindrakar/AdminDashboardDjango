from django import forms
from .models import Order,Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re



class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'first_name',
			'last_name',
			'password1',
			'password2'
		]
	
        

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"



class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = "__all__"
		exclude = ['user']

	def clean_phone(self):
		number = self.cleaned_data['phone']
		pattern = re.compile("^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$")
		isMobNum = pattern.match(number)
		if isMobNum == None:
			raise forms.ValidationError("Enter the valid mobile number.")



	# def clean_phone(self):
 #        number = self.cleaned_data['phone']
 #        pattern = re.compile("^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$")
 #        isMobNum = pattern.match(number)
 #        if isMobNum == None:
 #            raise forms.ValidationError("Enter the valid mobile number.")