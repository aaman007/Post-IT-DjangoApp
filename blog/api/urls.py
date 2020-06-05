from django.urls import path
from .views import (
    api_detail_post_view,
    api_create_post_view,
    api_delete_post_view,
    api_update_post_view,
    ApiPostListView
)

urlpatterns = [
    path('<int:pk>/', api_detail_post_view, name='api-post-detail'),
    path('new', api_create_post_view, name='api-post-create'),
    path('<int:pk>/update', api_update_post_view, name='api-post-update'),
    path('<int:pk>/delete', api_delete_post_view, name='api-post-delete'),
    path('list', ApiPostListView.as_view(), name='api-post-list'),
]