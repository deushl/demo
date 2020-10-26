from django.urls import path
from . import views

urlpatterns = [
    path('', views.RepoInfo.as_view(), name="information"),
    path('<int:repo_uuid>', views.SingleRepoInfo.as_view(), name='single_repo_info')
]
