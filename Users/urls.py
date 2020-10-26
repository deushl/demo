from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:org_uuid>', views.OrgDetails.as_view(),
         name="Organization details"),
]
