from django.urls import path

from .views import ListAllStaticTextAPIView, TermsAndConditionView, CompanyDetailView, FaqView, PrivacyPolicyView, AboutUsView, DropDownList, \
    FaqCategoryListView

app_name = "statictext"

urlpatterns = [

    path('statictext/all/', ListAllStaticTextAPIView.as_view(), name='all-static-text'),
    path('terms&condition/', TermsAndConditionView.as_view(), name='terms&condition'),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('about_us/', AboutUsView.as_view(), name='about-us'),
    path('faq/all/', FaqView.as_view(), name='faq'),
    path('faq/category/all/', FaqCategoryListView.as_view(), name='faq-category'),
    path('company/detail/', CompanyDetailView.as_view(), name='company-detail'),
    path('dropdown/list/', DropDownList.as_view(), name='dropdown-list'),
]