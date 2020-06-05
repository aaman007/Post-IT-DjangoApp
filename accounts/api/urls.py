from django.urls import path
from .views import (
    registration_view,
    account_properties_view,
    update_account_view
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns =[
    path('register', registration_view, name="api-register"),
    path('login', obtain_auth_token, name="api-login"),
    path('properties', account_properties_view, name="api-account-properties"),
    path('properties/update', update_account_view, name="api-update-account"),
]