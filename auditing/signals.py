from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from .local_user import get_current_user
from trips.models import Trip, Package
from customers.models import Customer
from vendors.models import Vendor
from vehicles.models import Vehicle

User = get_user_model()

print("AUDITING SIGNALS LOADED!")  # Debug print


def get_client_ip(request):
    """Gets the user's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login events"""
    print(f"LOGIN SIGNAL TRIGGERED for {user.username}")  # Debug print
    ip = get_client_ip(request)
    message = f"User logged in from IP address: {ip}"

    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(user).id,
        object_id=user.pk,
        object_repr=str(user),
        action_flag=CHANGE,
        change_message=message
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout events"""
    print(f"LOGOUT SIGNAL TRIGGERED for {user.username if user else 'Unknown'}")  # Debug print
    if user and user.is_authenticated:
        ip = get_client_ip(request)
        message = f"User logged out from IP address: {ip}"

        LogEntry.objects.log_action(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(user).id,
            object_id=user.pk,
            object_repr=str(user),
            action_flag=CHANGE,
            change_message=message
        )


@receiver(post_save, sender=Package)
def log_package_changes(sender, instance, created, **kwargs):
    """Log Package model changes"""
    print(f"PACKAGE SIGNAL TRIGGERED: {instance.name}, created: {created}")  # Debug print
    current_user = get_current_user()
    print(f"Current user from middleware: {current_user}")  # Debug print

    if current_user and current_user.is_authenticated:
        if created:
            action_flag = ADDITION
            message = f"Package '{instance.name}' was created"
        else:
            action_flag = CHANGE
            message = f"Package '{instance.name}' was updated"

        print(f"Creating log entry: {message}")  # Debug print

        try:
            LogEntry.objects.log_action(
                user_id=current_user.id,
                content_type_id=ContentType.objects.get_for_model(instance).id,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=action_flag,
                change_message=message
            )
            print("Log entry created successfully!")  # Debug print
        except Exception as e:
            print(f"Error creating log entry: {e}")  # Debug print
    else:
        print("No authenticated user found - not logging")  # Debug print


@receiver(post_save, sender=Customer)
def log_customer_changes(sender, instance, created, **kwargs):
    """Log Customer model changes"""
    print(f"CUSTOMER SIGNAL TRIGGERED: {instance.name}, created: {created}")  # Debug print
    current_user = get_current_user()
    print(f"Current user from middleware: {current_user}")  # Debug print

    if current_user and current_user.is_authenticated:
        if created:
            action_flag = ADDITION
            message = f"Customer '{instance.name}' was created"
        else:
            action_flag = CHANGE
            message = f"Customer '{instance.name}' was updated"

        print(f"Creating log entry: {message}")  # Debug print

        try:
            LogEntry.objects.log_action(
                user_id=current_user.id,
                content_type_id=ContentType.objects.get_for_model(instance).id,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=action_flag,
                change_message=message
            )
            print("Log entry created successfully!")  # Debug print
        except Exception as e:
            print(f"Error creating log entry: {e}")  # Debug print
    else:
        print("No authenticated user found - not logging")  # Debug print


@receiver(post_save, sender=Trip)
def log_trip_changes(sender, instance, created, **kwargs):
    """Log Trip model changes"""
    print(f"TRIP SIGNAL TRIGGERED: Trip #{instance.id}, created: {created}")  # Debug print
    current_user = get_current_user()
    print(f"Current user from middleware: {current_user}")  # Debug print

    if current_user and current_user.is_authenticated:
        if created:
            action_flag = ADDITION
            message = f"Trip #{instance.id} was created"
        else:
            action_flag = CHANGE
            if hasattr(instance, 'status') and instance.status == 'Cancelled':
                message = f"Trip #{instance.id} was cancelled"
            else:
                message = f"Trip #{instance.id} was updated"

        print(f"Creating log entry: {message}")  # Debug print

        try:
            LogEntry.objects.log_action(
                user_id=current_user.id,
                content_type_id=ContentType.objects.get_for_model(instance).id,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=action_flag,
                change_message=message
            )
            print("Log entry created successfully!")  # Debug print
        except Exception as e:
            print(f"Error creating log entry: {e}")  # Debug print
    else:
        print("No authenticated user found - not logging")  # Debug print


@receiver(post_save, sender=Vendor)
def log_vendor_changes(sender, instance, created, **kwargs):
    """Log Vendor model changes"""
    print(f"VENDOR SIGNAL TRIGGERED: {instance.name}, created: {created}")  # Debug print
    current_user = get_current_user()
    print(f"Current user from middleware: {current_user}")  # Debug print

    if current_user and current_user.is_authenticated:
        if created:
            action_flag = ADDITION
            message = f"Vendor '{instance.name}' was created"
        else:
            action_flag = CHANGE
            message = f"Vendor '{instance.name}' was updated"

        print(f"Creating log entry: {message}")  # Debug print

        try:
            LogEntry.objects.log_action(
                user_id=current_user.id,
                content_type_id=ContentType.objects.get_for_model(instance).id,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=action_flag,
                change_message=message
            )
            print("Log entry created successfully!")  # Debug print
        except Exception as e:
            print(f"Error creating log entry: {e}")  # Debug print
    else:
        print("No authenticated user found - not logging")  # Debug print


@receiver(post_save, sender=Vehicle)
def log_vehicle_changes(sender, instance, created, **kwargs):
    """Log Vehicle model changes"""
    print(f"VEHICLE SIGNAL TRIGGERED: {instance.number}, created: {created}")  # Debug print
    current_user = get_current_user()
    print(f"Current user from middleware: {current_user}")  # Debug print

    if current_user and current_user.is_authenticated:
        if created:
            action_flag = ADDITION
            message = f"Vehicle '{instance.number}' was created"
        else:
            action_flag = CHANGE
            message = f"Vehicle '{instance.number}' was updated"

        print(f"Creating log entry: {message}")  # Debug print

        try:
            LogEntry.objects.log_action(
                user_id=current_user.id,
                content_type_id=ContentType.objects.get_for_model(instance).id,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=action_flag,
                change_message=message
            )
            print("Log entry created successfully!")  # Debug print
        except Exception as e:
            print(f"Error creating log entry: {e}")  # Debug print
    else:
        print("No authenticated user found - not logging")  # Debug print


# Delete signals with debug prints
@receiver(post_delete, sender=Package)
def log_package_deletion(sender, instance, **kwargs):
    """Log Package deletions"""
    print(f"PACKAGE DELETE SIGNAL TRIGGERED: {instance.name}")  # Debug print
    current_user = get_current_user()

    if current_user and current_user.is_authenticated:
        try:
            LogEntry.objects.log_action(
                user_id=current_user.id,
                content_type_id=ContentType.objects.get_for_model(instance).id,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=DELETION,
                change_message=f"Package '{instance.name}' was deleted"
            )
            print("Delete log entry created successfully!")  # Debug print
        except Exception as e:
            print(f"Error creating delete log entry: {e}")  # Debug print


print("ALL SIGNAL HANDLERS REGISTERED!")  # Debug print