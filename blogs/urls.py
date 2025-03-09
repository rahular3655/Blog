from django.urls import path

from blogs.views.blog import BlogDetailAPIView, ListAllBlogsAPIView, ListRelatedBlogsAPIView, ListAllAuthorsAPIView, AuthorsDetailAPIView, \
    ListForYouBlogsAPIView

app_name = "blogs"

urlpatterns = [

    # Blogs
    path('all/', ListAllBlogsAPIView.as_view(), name='list-all-blogs'),
    path('detail/<slug:slug>/', BlogDetailAPIView.as_view(), name='blog-detail'),
    path('get-related-blogs/<slug:slug>/', ListRelatedBlogsAPIView.as_view(), name='list-related-blog'),
    path('for-you/', ListForYouBlogsAPIView.as_view(), name='for-you'),

    path('authors/', ListAllAuthorsAPIView.as_view(), name='list-all-authors'),
    path('author/<slug:slug>/', AuthorsDetailAPIView.as_view(), name='author-detail'),

]
