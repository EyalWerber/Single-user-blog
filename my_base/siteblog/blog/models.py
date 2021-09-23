from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
# Create your models here.
# Post model is using Rich Text Editor. Paper here - https://developpaper.com/django-building-personal-blogs-using-django-ckeditor-rich-text-editor/
from django.db.models.deletion import CASCADE


class Post(models.Model):
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title= models.CharField(max_length=40)
    text = RichTextUploadingField()
    create_date = models.DateTimeField(default=timezone.now())
    publication_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.publication_date=timezone.now()
        self.save()

    def approve_comment(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})


class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    text =models.TextField(max_length=300)
    create_date=models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self): 
        return reverse('post_list')

    def __str__(self):
        return self.text
