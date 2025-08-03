from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from .forms import StaffUserCreationForm, StaffUserChangeForm


@permission_required('auth.add_user', raise_exception=True)
def create_staff_view(request):
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff user created successfully!')
            return redirect('dashboard')  # Or a user list page
    else:
        form = StaffUserCreationForm()

    context = {
        'form': form,
        'title': 'Create Staff User'
    }
    return render(request, 'authentication/user_form.html', context)


@permission_required('auth.view_user', raise_exception=True)
def user_list_view(request):
    users = User.objects.all().order_by('username')
    context = {
        'users': users,
        'title': 'User Management'
    }
    return render(request, 'authentication/user_list.html', context)


@permission_required('auth.change_user', raise_exception=True)
def user_update_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = StaffUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user_list')
    else:
        form = StaffUserChangeForm(instance=user)

    context = {
        'form': form,
        'title': f'Edit User: {user.username}'
    }
    return render(request, 'authentication/user_form.html', context)


@permission_required('auth.delete_user', raise_exception=True)
def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_superuser:
        messages.error(request, 'Cannot delete a superuser.')
        return redirect('user_list')

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')

    context = {
        'user_to_delete': user,
        'title': 'Delete User'
    }
    return render(request, 'authentication/user_confirm_delete.html', context)

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')