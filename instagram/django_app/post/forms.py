from django import forms


class CommentForm(forms.Form):
    content = forms.CharField()

class LikeForm(forms.Form):
    like = forms.CharField()