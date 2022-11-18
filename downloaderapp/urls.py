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


    # For Public Profile

    # path('pubstory', views.pubstory, name="pubstory"),

    # path('puballpost', views.puballpost, name="puballpost"),

    # For Private Profile
    # path('pridp', views.pridp, name="pridp"),
    # path('pristory', views.pristory, name="pristory"),
    # path('pripost', views.pripost, name="pripost"),
    # path('priallpost', views.priallpost, name="priallpost"),
    # path('ytvideodownloaded', views.ytvideodownloaded, name="ytvideodownloaded"),
    # path('national', views.national, name="national")
]
