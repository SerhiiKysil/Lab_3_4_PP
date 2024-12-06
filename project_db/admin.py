from django.contrib import admin
from .models import EventParticipants, Events, Users, OrganizationUsers, Organizations, Roles

admin.site.register(EventParticipants)
admin.site.register(Events)
admin.site.register(Users)
admin.site.register(OrganizationUsers)
admin.site.register(Organizations)
admin.site.register(Roles)
