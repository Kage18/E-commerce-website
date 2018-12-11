from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=200)
    slugthing = models.SlugField(max_length=200)
    author = models.ForeignKey(User,related_name="blog_posts",on_delete=models.CASCADE)
    body = RichTextUploadingField()
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.id,self.slugthing])

@receiver(pre_save,sender = Post)
def pre_save_slug(sender,**kwargs):
    # print(kwargs)
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slugthing = slug

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    reply = models.ForeignKey('self',null=True,on_delete=models.CASCADE,related_name='replies')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.post.title,str(self.user.username))

