
from project_db import views
from django.urls import path

urlpatterns = [

    path('user/create/', views.create_user, name='create_user'),

    path('user/<int:user_id>/events/', views.get_events_for_user, name='get_events_for_user'),

    path('event/<int:event_id>/add-participant/<int:user_id>/', views.add_event_participant(), name='add_event_participant'),

    path('organization/create/', views.create_organization, name='create_organization'),

    path('event/<int:event_id>/remove-participant/<int:user_id>/', views.remove_event_participant, name='remove_event_participant'),
]
