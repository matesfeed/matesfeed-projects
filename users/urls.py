from django.urls import path
from . import views

urlpatterns = [
    path('developers/', views.developers, name="developers"),
    path('profile/', views.profile, name="profile"),
    path('profile/<int:id>/', views.show_profile, name="show_profile"),
    path('search/', views.search_users, name="search_user"),
    path('devs_connected/', views.devs_connected, name="devs_connected"),
    path('dev_requests_inbox/', views.dev_requests_inbox, name="dev_requests_inbox"),
    path('dev_requests_sent/', views.dev_requests_sent, name="dev_requests_sent"),
    path('send_dev_request/<int:id>/', views.send_dev_request, name="send_dev_request"),
    path('reject_dev_request/<int:id>/', views.reject_dev_request, name="reject_dev_request"),
    path('cancel_dev_request/<int:id>/', views.cancel_dev_request, name="cancel_dev_request"),
    path('accept_dev_request/<int:id>/', views.accept_dev_request, name="accept_dev_request"),
    path('break_connection/<int:id>/', views.break_connection, name="break_connection"),
    path('projects_invited/', views.projects_invited, name="project_requests"),
    path('handle_project_invite/', views.handle_project_invite, name="handle_project_invite")
]