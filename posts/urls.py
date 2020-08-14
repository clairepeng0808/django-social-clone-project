from django.urls import path,include
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.PostList.as_view(),name='list'),
    path('new/',views.CreatPost.as_view(),name='create'),
    path('delete/<int:pk>',views.DeletePost.as_view(),name='delete'),
    path('<username>/',views.UserPostList.as_view(),name='user_post'),
    path('<username>/<int:pk>',views.PostDetail.as_view(),name='detail')
]