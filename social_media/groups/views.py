from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        PermissionRequiredMixin)

from django.urls import reverse
from django.views import generic
from . import models
from . import forms
from braces.views import SelectRelatedMixin,PrefetchRelatedMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    model = models.Group
    form_class = forms.GroupForm
    template_name = 'groups/group_form.html'

class UserGroupList(LoginRequiredMixin,PrefetchRelatedMixin,generic.ListView):
    # groups belonging to an user
    prefetch_related = ('members','posts')
    template_name = 'groups/user_group_list.html'
    context_object_name = 'user_group_list'

    def get_queryset(self):
        return models.Group.objects.filter(members__username__iexact=self.request.user.username)
    
class GroupDetail(PrefetchRelatedMixin,generic.DetailView):
    model = models.Group
    prefetch_related = ('members','posts')

class GroupList(PrefetchRelatedMixin,generic.ListView):
    model = models.Group
    prefetch_related = ('members','posts')
    

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    
    # Once joining the group, you will be directed to the group detail page
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:detail',kwargs={'slug':kwargs.get('slug')})

    # Make sure the group exists
    def get(self, request, *args, **kwargs):

        group = get_object_or_404(models.Group,slug=kwargs.get('slug'))
        
        try:
            models.GroupMembership.objects.create(user=request.user,group=group)
        
        except IntegrityError:
            messages.warning(request,'You are already a member!')
        
        else:
            messages.success(request,'Joined the group successfully')
        
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    
    # Once joining the group, you will be directed to the group detail page
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:detail',kwargs={'slug':kwargs.get('slug')})
    
    # Make sure the group exists
    def get(self, request, *args, **kwargs):
        
        try:
            membership = models.GroupMembership.objects.filter(
            user=request.user,
            group=get_object_or_404(
                models.Group,slug=kwargs.get('slug')),
            )
        
        except models.GroupMembership.DoesNotExist:
            messages.warning(request,'You aren\'t a group member')
        
        else:
            membership.delete()
            messages.success(request,'Left the group!')
        
        return super().get(request,*args,**kwargs)

