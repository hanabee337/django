from django import forms

class PostForm(forms):
    username = forms.CharField(max_length=100)
    password = forms.CharField(
        widget=forms.Textarea
    )