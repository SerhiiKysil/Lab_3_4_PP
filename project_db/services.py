
from project_db.repositories import (
    EventParticipantsRepository,
    EventsRepository,
    OrganizationUsersRepository,
    OrganizationsRepository,
    RolesRepository,
    UsersRepository
)


class RepositoryService:
    def __init__(self):
        self.event_participants_repo = EventParticipantsRepository()
        self.events_repo = EventsRepository()
        self.organization_users_repo = OrganizationUsersRepository()
        self.organizations_repo = OrganizationsRepository()
        self.roles_repo = RolesRepository()
        self.users_repo = UsersRepository()

    def create_user(self, name, email, password, telegram, role_id):
        new_user = self.users_repo.create(
            name=name,
            email=email,
            password=password,
            telegram=telegram,
            role_id=role_id
        )
        return new_user

    def check_user_password(self, user, password):
        from django.contrib.auth.hashers import check_password
        return check_password(password, user.password)

    def add_event_participant(self, event_id, user_id, participation_date=None):
        return self.event_participants_repo.create(
            event_id=event_id,
            user_id=user_id,
            participation_date=participation_date
        )

    def get_events_for_user(self, user_id):
        participants = self.event_participants_repo.model.objects.filter(user_id=user_id)
        events = [participant.event for participant in participants]
        return events

    def create_organization(self, name, description, contact_email=None, website_url=None):
        new_org = self.organizations_repo.create(
            name=name,
            description=description,
            contact_email=contact_email,
            website_url=website_url
        )

        new_org.active_events_count = 0
        new_org.save()

        return new_org

    def assign_user_to_organization(self, organization_id, user_id):
        return self.organization_users_repo.create(
            organization_id=organization_id,
            user_id=user_id
        )

    def get_users_by_role(self, role_id):
        return self.users_repo.model.objects.filter(role_id=role_id)

    def update_organization(self, organization_id, **kwargs):
        return self.organizations_repo.update(organization_id, **kwargs)

    def remove_event_participant(self, event_id, user_id):
        return self.event_participants_repo.delete(event_id, user_id)

    def add_event(self, event_data):
        event = self.events_repo.create(**event_data)

        organization = event.organization
        organization.active_events_count += 1
        organization.save()

        return event

    def remove_event(self, event_id):
        event = self.events_repo.model.objects.get(id=event_id)
        organization = event.organization

        self.events_repo.delete(event_id)

        organization.active_events_count -= 1
        organization.save()
