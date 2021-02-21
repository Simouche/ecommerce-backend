from django.contrib import admin
from base_backend.admin import register_app_models
from authentication import signals

register_app_models('authentication')
