from django.urls import path

from .views import ListAllTagsAPIView, TagDetailAPIView

urlpatterns = [
    path('all/', ListAllTagsAPIView.as_view(), name='tag-list'),
    path('detail/<slug:slug>/', TagDetailAPIView.as_view(), name='tag-detail'),
]
