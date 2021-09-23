from django import forms
from django.db.models import fields
from django.forms.models import model_to_dict
from .models import Post,Comment
from django.contrib.auth.models import User
from captcha.fields import CaptchaField



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username  = forms.CharField(max_length=20)
    email = forms.EmailField()


    class Meta:
        model=User
        fields=('username','password','email')


class PostForm(forms.ModelForm):   
    
    class  Meta():
        model = Post
        fields=('author','title','text')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}), #this will be the html and representation of the form for the form.as_p tag
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}) #This is the required class to work with
        }
    

class CommentForm(forms.ModelForm):
    captcha = CaptchaField()   #captcha needs to be outside Meta class
    class Meta():
        model =Comment
        fields = ('author','text')
        

        widget={
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
            }