from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('bookmark_resource/', views.bookmark_resource, name="bookmark_resource"),
    path('filter/exp/<str:level>/', views.resource_exp_filter, name="resource_exp_filter"),
    path('filter/lang/<str:lang>/', views.resource_lang_filter, name="resource_lang_filter"),
    path('add_resource_to_project/', views.add_resource_to_project, name="add_resource_to_project"),
    path('remove_resource_from_project/', views.remove_resource_from_project, name="remove_resource_from_project"),
    path('project_resources/<int:id>/', views.project_resources, name="project_resources"),
    #profile urls
    path('show_user_resources_bookmarked/<int:id>/', views.user_resources_bookmarked, name="user_resources_bookmarked"),
    path('resources_added/<int:id>/', views.resources_added, name="resources_added"),
]