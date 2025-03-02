from django.urls import path
from common.views import LanguageListView, GlobalSearchViewAPI, redirect_to_oscar_index

app_name = "common"

urlpatterns = [
    path('get-languages/', LanguageListView.as_view(), name='language-list'),
    path('global-search/', GlobalSearchViewAPI.as_view(), name='global-search'),

]
