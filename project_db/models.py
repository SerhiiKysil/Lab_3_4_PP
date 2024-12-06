from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django.db import models


class EventParticipants(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    participation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_participants'
        unique_together = (('event', 'user'),)


class Events(models.Model):
    organization = models.ForeignKey('Organizations', models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'events'


class OrganizationUsers(models.Model):
    organization = models.OneToOneField('Organizations', models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organization_users'
        unique_together = (('organization', 'user'),)


class Organizations(models.Model):
    active_events_count = models.IntegerField(default=0, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    is_verified = models.IntegerField(blank=True, null=True)
    name = models.CharField(unique=True, max_length=255)
    website_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organizations'


class Roles(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'roles'


class Users(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.CharField(unique=True, max_length=255)
    is_verified = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    telegram = models.CharField(unique=True, max_length=255)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users'

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def check_password(self, password):
        return django_check_password(password, self.password)

