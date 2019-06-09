from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from .models import Post


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"fullname",
			"nickname",
			"email",
			"phone",
			"address",
			"image",
		]



class SignUpForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)

	class Meta:
		model = User
		fields = ("username","first_name","last_name","email","password1","password2",)

		