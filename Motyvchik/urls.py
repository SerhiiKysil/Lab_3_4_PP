"""
URL configuration for Motyvchik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from pandas.core.dtypes.astype import astype_is_view

from project_db.repositories import OrganizationsWithMoreThanFiveEventsAPIView, RecentEventsAPIView, \
    EventsWithManyParticipantsAPIView, UsersParticipationStatisticsAPIView, EventDurationStatisticsAPIView, \
    EventsPerOrganizationAPIView, UserList, UserDetail, OrganizationList, OrganizationDetail, EventList, EventDetail
from project_db.views import  \
    example_view, register_view, login_view, dashboard_view, register_organization_view, join_organization_view, \
    join_event_view, create_event_view, events_dashboard_view, leave_event_view, plot_events_per_organization, \
    plot_events_with_many_participants, plot_recent_events, plot_event_duration_statistics, plot_users_participation, \
    plot_organizations_with_many_events

urlpatterns = [
    path('plotly/recent-events/', plot_recent_events),
    path('plotly/organizations-with-many-events/', plot_organizations_with_many_events),
    path('plotly/users-participation/', plot_users_participation),
    path('plotly/event-duration-statistics/', plot_event_duration_statistics),
    path('plotly/events-with-many-participants/', plot_events_with_many_participants),
    path('plotly/events-per-organization/', plot_events_per_organization),
    path('api/organizations-more-5-events', OrganizationsWithMoreThanFiveEventsAPIView.as_view()),
    path('api/recent-events/', RecentEventsAPIView.as_view()),
    path('api/events-with-many-participants/', EventsWithManyParticipantsAPIView.as_view()),
    path('api/users-participation-statistics/', UsersParticipationStatisticsAPIView.as_view()),
    path('api/event-duration-statics/', EventDurationStatisticsAPIView.as_view()),
    path('api/events-per-organization/', EventsPerOrganizationAPIView.as_view()),
    path('example/', example_view),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register_organization/', register_organization_view, name='register_organization'),
    path('join_organization/', join_organization_view, name='join_organization'),
    path('events/', events_dashboard_view, name='events_dashboard'),
    path('events/join/<int:event_id>/', join_event_view, name='join_event'),
    path('events/leave/<int:event_id>/', leave_event_view, name='leave_event'),
    path('events/create/', create_event_view, name='create_event'),
    path('admin/', admin.site.urls),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('organizations/', OrganizationList.as_view()),
    path('organizations/<int:pk>/', OrganizationDetail.as_view()),
    path('events/bobo/', EventList.as_view()),
    path('events/<int:pk>/', EventDetail.as_view()),
]
