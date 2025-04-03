from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='stuff'),
    path('out/', views.outputView, name='out'),
    path('plot/', views.downloaded_file, name='plot'),
    path('video/', views.video_stream, name="vid"),
    path('start-button/', views.start_button, name='start_button'),
    path('stop-button/', views.stop_button, name='stop_button'),
    path('start-video-button/', views.start_video_button, name='start_video_button'),
    path('stop-video-button/', views.stop_video_button, name='stop_video_button'),
    path('new-img/', views.new_img, name='new_img'),
    path('get-radar-img/', views.radar_img, name='get_radar_img'),
]