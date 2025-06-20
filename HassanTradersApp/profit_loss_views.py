from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProfitForm, ProfitUserForm
from django.http import HttpResponseRedirect
from .models import ProfitRecord, ProfitUser
from django.urls import reverse

""" ---------------- Profit USER -------------------------"""


class ProfitUserDetailsEnum:
    def __init__(self, user, balance):
        self.user = user
        self.balance = balance


def profit_users(request):
    all_profit_users = ProfitUser.objects.all()
    profit_users_details = []
    for profit_user in all_profit_users:
        try:
            latest_balance_record = ProfitRecord.objects.filter(user_id=profit_user)
            length_of_records = len(latest_balance_record)
            calculated_index = length_of_records - 1 if length_of_records > 0 else 0
            latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
            closing_balance = latest_balance_record.balance
        except (ProfitRecord.DoesNotExist, IndexError):
            closing_balance = 0

        details = ProfitUserDetailsEnum(user=profit_user, balance=closing_balance)
        profit_users_details.append(details)

    context = {
        'profit_detail_url': 'profit_details',
        'add_url': 'add_profit_user',
        'edit_profit_url': 'edit_profit_user',
        'delete_profit_url': 'delete_profit_user',
        'records': profit_users_details,
    }

    return render(request, 'profit_loss_users.html', context=context)


def add_profit_user(request):
    if request.method == 'POST':
        form = ProfitUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('profit_users'))

    else:
        ProfitUserForm()
    all_profit_users = ProfitUser.objects.all()
    context = {
        'profit_detail_url': 'profit_details',
        'add_url': 'add_profit_user',
        'edit_profit_url': 'edit_profit_user',
        'delete_profit_url': 'delete_profit_user',
        'records': all_profit_users
    }

    return render(request, 'profit_loss_users.html', context)


def edit_profit_user(request, record_id):
    profit_record = get_object_or_404(ProfitUser, primary_key=record_id)
    if not profit_record:
        return redirect(reverse('profit_users'))

    default_context = {
        'top_title': 'Update User',
        'success_alert': 'The User updated successfully.',
        'form_top_legend': 'Update profit User Records',
        'return_url': 'profit_users',
        'edit_url': f'edit_profit_user {profit_record.primary_key}'
    }

    if request.method == 'POST':
        form = ProfitUserForm(request.POST, instance=profit_record)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'success': True,
                'record': profit_record
            }
            context.update(default_context)
            return render(request, 'edit.html', context=context)

    form = ProfitUserForm(instance=profit_record)
    context = {
        'form': form,
        'success': False,
        'record': profit_record
    }
    context.update(default_context)
    return render(request, 'edit.html', context=context)


def delete_profit_user(request, record_id):
    profit_record = get_object_or_404(ProfitUser, primary_key=record_id)
    if not profit_record:
        return redirect(reverse('profit_users'))

    if request.method == 'POST':
        profit_record.delete()
    return HttpResponseRedirect(reverse(f'profit_users'))


""" ---------------- Profit DETAILS -------------------------"""


def profit_details(request, user_id):
    default_context = {
        'profit_detail_url': 'profit_details',
        'edit_profit_url': 'edit_profit',
        'add_profit_url': 'add_profit',
        'delete_profit_url': 'delete_profit',
    }
    # print("hello")
    user = get_object_or_404(ProfitUser, primary_key=user_id) if user_id else None
    # user = ProfitUser.objects.get(pk=user_id)
    # print("get", user)
    if not user:
        return redirect(reverse('profit_details', args=[user_id]))

    try:
        latest_balance_record = ProfitRecord.objects.filter(user_id=user)
        length_of_records = len(latest_balance_record)
        calculated_index = length_of_records - 1 if length_of_records > 0 else 0
        latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
        previous_balance = latest_balance_record.balance
    except (ProfitRecord.DoesNotExist, IndexError):
        previous_balance = 0

    records = ProfitRecord.objects.filter(user_id=user)
    context = {'user': user, 'records': records, 'previous_balance': previous_balance}
    context.update(default_context)
    return render(request, 'profit_loss_register.html', context=context)


def add_profit(request, user_id):
    user = get_object_or_404(ProfitUser, primary_key=user_id) if user_id else None

    if not user:
        return redirect(reverse('profit_details', args=[user_id]))

    # Get the latest record to get the previous balance
    try:
        latest_balance_record = ProfitRecord.objects.filter(user_id=user)
        length_of_records = len(latest_balance_record)
        calculated_index = length_of_records - 1 if length_of_records > 0 else 0
        latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
        previous_balance = latest_balance_record.balance
    except (ProfitRecord.DoesNotExist, IndexError):
        previous_balance = 0

    if request.method == 'POST':
        form = ProfitForm(request.POST)
        if form.is_valid():
            form.instance.user_id = user
            form.save()
        return redirect(reverse('profit_details', args=[user_id]))
    else:
        form = ProfitForm(initial={'balance': previous_balance})

    context = {
        'user': user,
        'records': ProfitRecord.objects.filter(user_id=user),
        'form': form,
        'previous_balance': previous_balance,
    }
    return render(request, 'profit_loss_register.html', context)


def edit_profit(request, record_id):
    profit_record = get_object_or_404(ProfitRecord, primary_key=record_id)
    if not profit_record:
        return redirect(reverse('profit_users'))

    default_context = {
        'top_title': 'Update profit',
        'success_alert': 'The profit updated successfully.',
        'form_top_legend': 'Update profit Records',
        'return_url': f'profit_details {profit_record.user_id.primary_key}',
        'edit_url': f'edit_profit {profit_record.primary_key}'
    }

    if request.method == 'POST':
        form = ProfitForm(request.POST, instance=profit_record)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'success': True,
                'record': profit_record
            }
            context.update(default_context)
            return render(request, 'edit.html', context=context)

    form = ProfitForm(instance=profit_record)
    context = {
        'form': form,
        'success': False,
        'record': profit_record
    }
    context.update(default_context)
    return render(request, 'edit.html', context=context)


def delete_profit(request, record_id):
    profit_record = get_object_or_404(ProfitRecord, primary_key=record_id)
    if not profit_record:
        return redirect(reverse('profit_users'))

    if request.method == 'POST':
        profit_record.delete()
    return HttpResponseRedirect(reverse(f'profit_details', args=[profit_record.user_id.primary_key]))
