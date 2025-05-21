from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import Dashboard
from django.contrib import messages

@receiver(user_logged_in)
def handle_dashboard_invite(sender, request, user, **kwargs):
    dashboard_id = request.session.pop('dashboard_id', None)
    if dashboard_id:
        try:
            dashboard = Dashboard.objects.get(id=dashboard_id)
            dashboard.allowed_users.add(user)
            messages.success(request, 'You have been added as a viewer to the dashboard.')
        except Dashboard.DoesNotExist:
            messages.error(request, 'The dashboard no longer exists.')