from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time


def upload_location(instance, filename):
	  return "%s/%s" %(instance.title, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=130)
    slug = models.SlugField(blank=True,unique=True)
    image = models.ImageField(
      upload_to=upload_location , 
      null=True,
      blank=True,
      )
    content = models.TextField()
    draft = models.BooleanField(default=False)
    read_time = models.IntegerField(default=0,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    view_count = models.IntegerField(default=0,null=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
      return self.title

    @property
    def raise_view_count(self):
        self.view_count = self.view_count +1
        return True

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['-timestamp', '-updated']
      

def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
      slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists() 
    if exists:
      new_slug = "%s-%s" %(slug,qs.first().id)
      return create_slug(instance,new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender,instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.content
        read_time = get_read_time(html_string)
        instance.read_time = read_time 


pre_save.connect(pre_save_post_receiver, sender=Post)
