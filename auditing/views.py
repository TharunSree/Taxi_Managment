from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.models import LogEntry
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def action_log_view(request):
    # Get content type for User model
    user_content_type = ContentType.objects.get_for_model(User)

    # Fetch all log entries, getting related user and content type for efficiency
    all_logs = LogEntry.objects.select_related('user', 'content_type').all().order_by('-action_time')

    # Filter for session logs (login/logout) - these are logged against User model
    session_logs = all_logs.filter(
        content_type=user_content_type,
        change_message__icontains='logged'
    )

    # Get all non-user model logs (Trip, Customer, Vendor, Vehicle actions)
    action_logs = all_logs.exclude(content_type=user_content_type)

    print(f"Total logs: {all_logs.count()}")
    print(f"Session logs: {session_logs.count()}")
    print(f"Action logs: {action_logs.count()}")

    context = {
        'action_logs': action_logs,
        'session_logs': session_logs,
        'title': 'User Action Logs'
    }
    return render(request, 'auditing/log_list.html', context)