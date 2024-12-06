from datetime import timedelta
import plotly.express as px
import pandas as pd
from django.db.models import Count, F
from django.utils import timezone
from django.utils.timezone import now
from django.http import JsonResponse

from project_db.services import RepositoryService
from project_db.models import Users, Organizations, Events, OrganizationUsers, EventParticipants
from django.shortcuts import redirect
service = RepositoryService()

from django.shortcuts import render


def plot_event_duration_statistics(request):
    events_with_duration = Events.objects.annotate(
        duration=F('end_time') - F('start_time')
    )
    data = list(events_with_duration.values('title', 'duration'))
    df = pd.DataFrame(data)
    fig = px.pie(df, values='duration', names='title', title='Event Duration Statistics')
    graph = fig.to_html(full_html=False)

    return render(request, 'plotly_graph.html', {'graph': graph})

def plot_users_participation(request):
    users_participation_count = EventParticipants.objects.values('user__name').annotate(
        participation_count=Count('user')).order_by('-participation_count')
    data = list(users_participation_count)
    df = pd.DataFrame(data)

    fig = px.bar(df, x='participation_count', y='user__name', orientation='h', title='User Participation in Events')
    graph = fig.to_html(full_html=False)

    return render(request, 'plotly_graph.html', {'graph': graph})

def plot_organizations_with_many_events(request):
    organizations_with_event_count = Organizations.objects.annotate(event_count=Count('events'))
    organizations_with_more_than_five_events = organizations_with_event_count.filter(event_count__gte=5)
    data = list(organizations_with_more_than_five_events.values('name', 'event_count'))
    df = pd.DataFrame(data)

    fig = px.bar(df, x='name', y='event_count', title='Organizations With More Than 5 Events')
    graph = fig.to_html(full_html=False)

    return render(request, 'plotly_graph.html', {'graph': graph})

def plot_recent_events(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_events = Events.objects.filter(start_time__gte=thirty_days_ago)
    data = list(recent_events.values('title', 'start_time', 'end_time'))

    df = pd.DataFrame(data)

    fig = px.line(df, x='start_time', y=df.index, title='Recent Events (Last 30 Days)', markers=True)
    graph = fig.to_html(full_html=False)

    return render(request, 'plotly_graph.html', {'graph': graph})

def plot_events_with_many_participants(request):
    events_with_many_participants = Events.objects.annotate(participant_count=Count('eventparticipants')).filter(participant_count__gte=5)
    data = list(events_with_many_participants.values('title', 'participant_count'))
    df = pd.DataFrame(data)

    fig = px.bar(df, x='title', y='participant_count', title='Events With Many Participants')
    graph = fig.to_html(full_html=False)

    return render(request, 'plotly_graph.html', {'graph': graph})


def plot_events_per_organization(request):
    organizations_with_event_count = Organizations.objects.annotate(event_count=Count('events'))
    data = list(organizations_with_event_count.values('name', 'event_count'))

    df = pd.DataFrame(data)

    fig = px.bar(df, x='name', y='event_count', title='Events Per Organization')
    graph = fig.to_html(full_html=False)

    return render(request, 'plotly_graph.html', {'graph': graph})


def example_view(request):
    return render(request, 'project_db/example.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        telegram = request.POST.get('telegram')

        try:
            new_user = Users.objects.create(
                name=name,
                email=email,
                password=password,
                telegram=telegram,
                role_id=1
            )
            return redirect('login')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, 'project_db/register.html')


def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Users.objects.get(id=user_id)
    return render(request, 'project_db/dashboard.html', {'user': user})

def events_dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Users.objects.get(id=user_id)
    user_events = Events.objects.filter(eventparticipants__user_id=user_id)
    all_events = Events.objects.all()
    user_event_ids = user_events.values_list('id', flat=True)
    user_organizations = Organizations.objects.filter(organizationusers__user_id=user_id)

    return render(request, 'project_db/events_dashboard.html', {
        'user': user,
        'user_events': user_events,
        'all_events': all_events,
        'user_event_ids': user_event_ids,
        'user_organizations': user_organizations,
    })

def join_event_view(request, event_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        EventParticipants.objects.create(event_id=event_id, user_id=user_id, participation_date=now())
        return redirect('events_dashboard')
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def leave_event_view(request, event_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        EventParticipants.objects.filter(event_id=event_id, user_id=user_id).delete()
        return redirect('events_dashboard')
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def create_event_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        organization_id = request.POST.get('organization_id')

        try:
            Events.objects.create(
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                organization_id=organization_id
            )
            return redirect('events_dashboard')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return redirect('events_dashboard')

def register_organization_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        contact_email = request.POST.get('contact_email')
        website_url = request.POST.get('website_url')

        try:
            new_org = Organizations.objects.create(
                name=name,
                description=description,
                contact_email=contact_email,
                website_url=website_url,
                is_verified=0
            )
            user_id = request.session.get('user_id')
            OrganizationUsers.objects.create(organization=new_org, user_id=user_id)
            return redirect('dashboard')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, 'project_db/register_organization.html')


def join_organization_view(request):
    if request.method == 'POST':
        organization_id = request.POST.get('organization_id')

        try:
            user_id = request.session.get('user_id')
            OrganizationUsers.objects.create(organization_id=organization_id, user_id=user_id)
            return redirect('dashboard')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    organizations = Organizations.objects.all()
    return render(request, 'project_db/join_organization.html', {'organizations': organizations})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Users.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)

    return render(request, 'project_db/login.html')




def create_user(request):
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        telegram = request.POST.get('telegram')
        role_id = request.POST.get('role_id')

        new_user = service.create_user(
            name=name,
            email=email,
            password=password,
            telegram=telegram,
            role_id=role_id
        )

        return JsonResponse({
            "status": "User created successfully",
            "user_id": new_user.id
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def get_events_for_user(request, user_id):
    try:
        events = service.get_events_for_user(user_id)
        events_data = [{"event_id": event.id, "title": event.title, "start_time": event.start_time} for event in events]
        return JsonResponse({"events": events_data}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def add_event_participant(request, event_id, user_id):
    try:
        participation_date = request.GET.get('participation_date', None)
        service.add_event_participant(event_id, user_id, participation_date)
        return JsonResponse({"status": "Participant added successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def create_organization(request):
    try:
        name = request.POST.get('name')
        description = request.POST.get('description')
        contact_email = request.POST.get('contact_email', None)
        website_url = request.POST.get('website_url', None)

        new_org = service.create_organization(name, description, contact_email, website_url)
        return JsonResponse({"status": "Organization created", "organization_id": new_org.id}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def remove_event_participant(request, event_id, user_id):
    try:
        service.remove_event_participant(event_id, user_id)
        return JsonResponse({"status": "Participant removed successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

