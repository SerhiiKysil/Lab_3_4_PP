from datetime import timedelta

import pandas as pd
from django.db.models import Count, F
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from project_db.models import EventParticipants, Events, Users, OrganizationUsers, Organizations, Roles
from project_db.serializers import UserSerializer, OrganizationSerializer, EventSerializer


class EventsPerOrganizationAPIView(APIView):
    def get(self, request):
        organizations_with_event_count = Organizations.objects.annotate(event_count=Count('events'))

        data = list(organizations_with_event_count.values('name', 'event_count'))
        df = pd.DataFrame(data)

        return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)

class RecentEventsAPIView(APIView):
    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_events = Events.objects.filter(start_time__gte=thirty_days_ago)
        data = list(recent_events.values('title', 'start_time', 'end_time'))
        df = pd.DataFrame(data)

        return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)

class OrganizationsWithMoreThanFiveEventsAPIView(APIView):
    def get(self, request):
        organizations_with_event_count = Organizations.objects.annotate(event_count=Count('events'))
        organizations_with_more_than_five_events = organizations_with_event_count.filter(event_count__gte=5)
        data = list(organizations_with_more_than_five_events.values('name', 'event_count'))
        df = pd.DataFrame(data)

        return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)

class EventsWithManyParticipantsAPIView(APIView):
    def get(self, request):
        events_with_many_participants = Events.objects.annotate(participant_count=Count('eventparticipants')).filter(
            participant_count__gte=5)

        data = list(events_with_many_participants.values('title', 'participant_count'))
        df = pd.DataFrame(data)

        return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)

class UsersParticipationStatisticsAPIView(APIView):
    def get(self, request):
        users_participation_count = EventParticipants.objects.values('user__name').annotate(
            participation_count=Count('user')).order_by('-participation_count')

        data = list(users_participation_count)
        df = pd.DataFrame(data)

        return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)

class EventDurationStatisticsAPIView(APIView):
    def get(self, request):
        events_with_duration = Events.objects.annotate(
            duration=F('end_time') - F('start_time')
        )

        data = list(events_with_duration.values('title', 'duration'))
        df = pd.DataFrame(data)

        mean_duration = df['duration'].mean()
        median_duration = df['duration'].median()
        min_duration = df['duration'].min()
        max_duration = df['duration'].max()

        stats_data = {
            "mean_duration": [mean_duration],
            "median_duration": [median_duration],
            "min_duration": [min_duration],
            "max_duration": [max_duration]
        }

        stats_df = pd.DataFrame(stats_data)

        return Response(stats_df.to_dict(orient='records'), status=status.HTTP_200_OK)

class RepositoryBase:
    model = None

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, pk, **kwargs):
        instance = self.get_by_id(pk)
        if instance:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

    def delete(self, pk):
        instance = self.get_by_id(pk)
        if instance:
            instance.delete()
        return instance


class EventParticipantsRepository(RepositoryBase):
    model = EventParticipants

    def get_by_event_and_user(self, event_id, user_id):
        return self.model.objects.filter(event_id=event_id, user_id=user_id).first()


class EventsRepository(RepositoryBase):
    model = Events


class OrganizationUsersRepository(RepositoryBase):
    model = OrganizationUsers

    def get_by_organization_and_user(self, organization_id, user_id):
        return self.model.objects.filter(organization_id=organization_id, user_id=user_id).first()


class OrganizationsRepository(RepositoryBase):
    model = Organizations


class RolesRepository(RepositoryBase):
    model = Roles


class UsersRepository(RepositoryBase):
    model = Users


class UserList(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class OrganizationList(generics.ListCreateAPIView):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer

class EventList(generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer