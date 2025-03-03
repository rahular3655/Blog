from django.urls import path
from .views import image_upload, video_upload, file_upload

urlpatterns = [
    path('image_upload/', image_upload, name='froala_editor_image_upload'),
    path('file_upload/', file_upload, name='froala_editor_file_upload'),
    path('video_upload/', video_upload, name='froala_editor_video_upload'),
]
