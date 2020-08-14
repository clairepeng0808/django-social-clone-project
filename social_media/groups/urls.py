from django.urls import path,include
from . import views
from . import forms

app_name = 'groups'

urlpatterns = [
    path('', views.GroupList.as_view(),name='list'),
    path('create/', views.CreateGroup.as_view(),name='create'),
    path('mygroup/',views.UserGroupList.as_view(),name='mygroup'),
    path('<slug>/', views.GroupDetail.as_view(),name='detail'),
    path('join/<slug>/', views.JoinGroup.as_view(),name='join'),
    path('leave/<slug>', views.LeaveGroup.as_view(),name='leave'),
]