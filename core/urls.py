from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('commentpost', views.commentpost, name='commentpost'),
    path('updatepost', views.updatepost, name='updatepost'), 
    path('deletepost', views.deletepost, name='deletepost'),        
    path('likepost', views.likepost, name='likepost'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout')
]