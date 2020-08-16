from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import Http404
from django.shortcuts import get_object_or_404

from braces.views import SelectRelatedMixin
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

    # todo: https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/learn/lecture/7133892#questions/3081816
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_groups'] = models.Group.objects.filter(members__in=[self.request.user])
        context['other_groups'] = models.Group.objects.exclude(members__in=[self.request.user])
        return context

class UserPostList(LoginRequiredMixin,SelectRelatedMixin,generic.ListView):
    # posts belonging to an user
    model = models.Post
    select_related = ('user','group')

    # def get_queryset(self):
    #     return super().get_queryset().filter(user__username__iexact=self.request.user.username)
    #     # use "self.request.user.username" if it's login required

    # def get_queryset(self):

    #     try: 
    #         # try to check if the user exists
    #         self.post_user = User.objects.prefetch_related('posts').get(
    #             username__iexact=self.kwargs.get('username')
    #             )

    #     except User.DoesNotExist:
    #         raise Http404

    #     else:
    #         return self.post_user.posts.all
    
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_user"] = self.post_user
    #     return context

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
        return super().get_queryset().filter(user__username=self.request.user.username)
        # use "self.request.user.username" if it's login required
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request,'Post Deleted!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        group_slug = self.object.group.slug
        return reverse_lazy('groups:detail',kwargs={'slug':group_slug})

