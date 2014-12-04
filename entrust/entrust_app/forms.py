from django import forms
from django.contrib.auth.models import User
from models import *

class signupform(forms.Form):
	firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Firstname'}))
	lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Lastname'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
	nickname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nickname'}))
	password=forms.CharField(max_length=15,label='password',widget=forms.PasswordInput(attrs={'placeholder':'password'}))
	password1=forms.CharField(max_length=15,label='Retype password',widget=forms.PasswordInput(attrs={'placeholder':'Retype password'}))
	doorno = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Door Number'}))
	street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street'}))
	city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City'}))
	state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	country = forms.CharField(max_length = 27,initial="United States Of America")
	pincode = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'ZIP'}))
	phoneno = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Contact Number','border-color':'10px'}))
	dateofbirth = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'DOB'}))
	
	def clean(self):
		cleaned_data=super(signupform,self).clean()
		nickname=cleaned_data.get('nickname')
		firstname=cleaned_data.get('firstname')
		lastname=cleaned_data.get('lastname')
		email=cleaned_data.get('email')
		password=cleaned_data.get('password')
		password1=cleaned_data.get('password1')
		if nickname and len(nickname) > 8:
			raise forms.ValidationError("Nickname should be lesser than 8 characters")
		if User.objects.filter(username=nickname).count():
			raise forms.ValidationError("Nickname exists. Choose another one")
		if password and len(password) < 7:
			raise forms.ValidationError("Password must be atleast 7 Characters")
		if password and password1 and password!=password1:
			raise forms.ValidationError("Passwords do not match")
		return cleaned_data

class loginform(forms.Form):
                
        username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
        password=forms.CharField(max_length=15,label='password',widget=forms.PasswordInput(attrs={'placeholder':'password'}))

class UserInforForm(forms.ModelForm):
		class Meta:
			model = User_information
			exclude = ('user', 'rating_stars', 'rating_cumulative', 'rating_count', )
			widgets = {'picture' : forms.FileInput() }
