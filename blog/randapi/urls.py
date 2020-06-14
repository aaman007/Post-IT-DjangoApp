from django.urls import path
from blog.randapi import views as randapi_views

urlpatterns = [
    path('ncategory-posts/<str:category>/<int:quantity>', randapi_views.NCategoryListAPIView.as_view(), name="ncategory-list-api"),
]