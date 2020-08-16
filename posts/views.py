from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import Http404
from django.shortcuts import get_object_or_404,redirect

from braces.views import SelectRelatedMixin,PrefetchRelatedMixin
from . import models
from . import forms
from django.contrib import messages


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class PostList(SelectRelatedMixin,generic.ListView):
    # posts belonging to a group
    model = models.Post
    select_related = ('user','group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user_groups'] = models.Group.objects.filter(members__in=[self.request.user])
        # context['other_groups'] = models.Group.objects.exclude(members__in=[self.request.user])
        return context

class UserPostList(LoginRequiredMixin,SelectRelatedMixin,generic.ListView):
    # posts belonging to one user
    model = models.Post
    select_related = ('user','group')
    template_name = 'posts/user_post_list.html'
    context_object_name = 'user_post_list'

    def get_queryset(self):
        post_user = get_object_or_404(User,username=self.kwargs.get('username'))
        qs = super().get_queryset()
        return qs.filter(user__username=post_user.username)

    # if you want to redirect when the object doesnot exist
    # def get(self, request, *args, **kwargs):
        
    #     post_user = self.get_queryset()
        
    #     if not post_user:
    #         messages.warning(request,'The member does not exist')
    #         return redirect('posts:list')
        
    #     return super().get(request,*args,**kwargs)

    

class CreatPost(SelectRelatedMixin,LoginRequiredMixin,generic.CreateView):
    model = models.Post
    form_class = forms.PostForm
    select_related = ('user','group')

    # TODO: https://stackoverflow.com/questions/24041649/filtering-a-model-in-a-createview-with-get-queryset
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        group_slug = self.object.group.slug
        return reverse('groups:detail',kwargs={'slug':group_slug})
    
    
class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):

    model = models.Post
    select_related = ('user','group')
    
    def get_queryset(self):
        return super().get_queryset().filter(user__username__iexact=self.request.user.username)
        # use "self.request.user.username" if it's login required
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request,'Post Deleted!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        group_slug = self.object.group.slug
        return reverse_lazy('groups:detail',kwargs={'slug':group_slug})

