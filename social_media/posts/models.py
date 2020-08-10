from django.db import models
from django.urls import reverse
from django.conf import settings
from  django.utils import timezone
import misaka
from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, default='', related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    message = models.TextField(default='',blank=True)
    message_html = models.TextField(editable=False,blank=True)
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.message
    
    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'username':self.user.username,
                                               'pk': self.pk})
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [('user','message')]
