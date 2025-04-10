from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='stuff'),
    path('out/', views.outputView, name='out'),
    path('plot/', views.plot_page, name='plot'),
    path('plot2/', views.plot_page2, name='plot2'),
    path('video/', views.video_stream, name="vid"),
    path('start-button/', views.start_button, name='start_button'),
    path('stop-button/', views.stop_button, name='stop_button'),
    path('start-video-button/', views.start_video_button, name='start_video_button'),
    path('stop-video-button/', views.stop_video_button, name='stop_video_button'),
    path('new-img/', views.new_img, name='new_img'),
    path('get-radar-img/', views.radar_img, name='get_radar_img'),
    path('get-radar-room-state/', views.get_radar_room_state, name='get_radar_room_state'),
    path('start-radar-button/', views.start_video_button, name='start_radar_button'),
    path('stop-radar-button/', views.stop_video_button, name='stop_radar_button'),
    path('video_feed/', views.proxy_video_feed, name='proxy_video_feed'),
]