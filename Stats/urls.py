from django.urls import path
from . import views

urlpatterns = [
    path('', views.Stats.as_view(),
         name="Stats"),
]
