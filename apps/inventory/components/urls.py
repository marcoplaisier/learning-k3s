from django.urls import path

from . import views

urlpatterns = [
    path("", views.component_list, name="component_list"),
    path("<uuid:component_id>/", views.component_detail, name="component_detail"),
]
