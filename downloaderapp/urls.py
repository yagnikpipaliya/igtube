from django.urls import path
from . import views

urlpatterns = [
    # root
    path('', views.index, name="index"),
    path('shorts', views.shorts, name="shorts"),
    path('ytvideodownload', views.ytvideodownload, name="ytvideodownload"),


    #For Both
    path('dp', views.dp, name="dp"),
    path('story', views.story, name="story"),
    path('singlepost', views.singlepost, name="singlepost"),
    path('allpost', views.allpost, name="allpost"),
    path('reels', views.reels, name="reels"),

]
