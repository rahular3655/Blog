from django.urls import path

from .views import CategoryList, CategoryDetails, ListCategoryChildren

urlpatterns = [
    path('all/', CategoryList.as_view(), name='category-list'),
    path('<slug:slug>/', CategoryDetails.as_view(), name='category-details'),
    path('get-children/<slug:slug>/', ListCategoryChildren.as_view(), name='category-childrens'),

]
