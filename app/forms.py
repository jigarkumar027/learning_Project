from django import forms

class myform(forms.Form):
    Username = forms.CharField(max_length=50)
    Email = forms.EmailField(max_length=50)
    Password = forms.CharField(max_length=50)