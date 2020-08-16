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
        context['user_groups'] = models.Group.objects.filter(members__in=[self.request.user])
        context['other_groups'] = models.Group.objects.exclude(members__in=[self.request.user])
        return context

class UserPostList(LoginRequiredMixin,SelectRelatedMixin,generic.ListView):
    # posts belonging to one user
    model = models.Post
    select_related = ('user','group')
    template_name = 'posts/user_post_list.html'
    context_object_name = 'user_post_list'

    def get(self, request, *args, **kwargs):
        post = self.get_queryset()
        # try:
        #     post_user = User.objects.get(
        #         username__iexact=self.kwargs.get('username')
        #     )         
        # except User.DoesNotExist:
        #     return redirect('posts:list')
        #     messages.warning(request,'You are already a member!')
        if not post:
            return redirect('posts:list')
        return super().get(request,*args,**kwargs)


    def get_queryset(self):
        self.post_user = User.objects.get(username__iexact=self.kwargs.get('username'))
        return self.post_user.posts.all()

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        return super().get_queryset().filter(user__username__iexact=self.kwargs.get('username'))

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
        return super().get_queryset().filter(user=self.request.user)
        # use "self.request.user.username" if it's login required
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request,'Post Deleted!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        group_slug = self.object.group.slug
        return reverse_lazy('groups:detail',kwargs={'slug':group_slug})

