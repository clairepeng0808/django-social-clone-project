from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=256,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    members = models.ManyToManyField(User,through='GroupMembership')
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self,*arg,**kwargs):
        self.slug = slugify(self.name)
        # /claire peng --> /claire-peng
        super().save(*arg,**kwargs)
    
    def get_absolute_url(self):
        return reverse('groups:detail', kwargs={'slug':self.slug})
        

class GroupMembership(models.Model):
    group = models.ForeignKey(Group,related_name='membership',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='membership',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together = ('group','user')
    