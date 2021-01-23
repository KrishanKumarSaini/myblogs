from django import forms
from .models import post, Comments

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('title', 'content', 'thumbnail', 'tags')
        exclude = ['status']

class EmailPostForm(forms.Form):
    to = forms.EmailField()
    subject = forms.CharField(max_length=100)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name','body')