from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:id>/', views.project, name="project"),
    path('bookmark_project/', views.bookmark_project, name="bookmark_project"),
    path('handle_pending_project_requests/', views.handle_pending_project_requests, name="handle_pending_project_requests"),
    path('handle_project_request/', views.handle_project_request, name="handle_project_request"),
    path('leave_project_request/', views.leave_project_request, name="leave_project_request"),
    path('add-issue/<int:id>/', views.addIssue, name="issue"),
    path(
        'issue-status/<int:project_id>/<int:issue_id>/<int:status>/', 
        views.changeIssueStatus, 
        name="issueState"
        ),
    path('end_project/<int:id>/', views.end_project, name="end_project"),
    path('restart_project/<int:id>/', views.restart_project, name="restart_project"),
    #profile urls
    path('show_user_bookmarked_projects/<int:id>/', views.user_projects_bookmarked, name="user_projects_bookmarked"),
    path('show_user_working_projects/<int:id>/', views.user_working_projects, name="user_projects_bookmarked"),
    path('show_user_requested_projects/<int:id>/', views.user_requested_projects, name="user_projects_bookmarked"),
    path('user_requests_rejected/<int:id>/', views.user_requests_rejected, name="user_projects_bookmarked"),
    path('projects_created/<int:id>/', views.projects_created, name="projects_created"),
    path('projects_completed/<int:id>/', views.projects_completed, name="projects_completed"),
    path('kick_out_dev/',views.kick_out_dev, name="kick_out"),
    path('invite_devs/', views.invite_devs, name="invite_devs"),
    path('cancel_invite/', views.cancel_invite, name="cancel_invite")
]