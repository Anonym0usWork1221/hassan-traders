from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import LedgerRecord, LedgerUser
from .forms import LedgerForm, LedgerUserForm

""" ---------------- Ledger USER -------------------------"""


class LedgerUserDetailsEnum:
    def __init__(self, user, balance):
        self.user = user
        self.balance = balance


def ledger_users(request):
    all_ledger_users = LedgerUser.objects.all()
    ledger_users_details = []
    for ledger_user in all_ledger_users:
        try:
            latest_balance_record = LedgerRecord.objects.filter(user_id=ledger_user)
            length_of_records = len(latest_balance_record)
            calculated_index = length_of_records - 1 if length_of_records > 0 else 0
            latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
            closing_balance = latest_balance_record.balance
        except (LedgerRecord.DoesNotExist, IndexError):
            closing_balance = 0

        details = LedgerUserDetailsEnum(user=ledger_user, balance=closing_balance)
        ledger_users_details.append(details)

    context = {
        'ledger_detail_url': 'ledger_details',
        'add_url': 'add_ledger_user',
        'edit_ledger_url': 'edit_ledger_user',
        'delete_ledger_url': 'delete_ledger_user',
        'records': ledger_users_details
    }
    return render(request, 'ledger_users.html', context=context)


def add_ledger_user(request):
    if request.method == 'POST':
        form = LedgerUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('ledger_users'))

    else:
        LedgerUserForm()
    all_ledger_users = LedgerUser.objects.all()
    context = {
        'ledger_detail_url': 'ledger_details',
        'add_url': 'add_ledger_user',
        'edit_ledger_url': 'edit_ledger_user',
        'delete_ledger_url': 'delete_ledger_user',
        'records': all_ledger_users
    }

    return render(request, 'ledger_users.html', context)


def edit_ledger_user(request, record_id):
    ledger_record = get_object_or_404(LedgerUser, primary_key=record_id)
    if not ledger_record:
        return redirect(reverse('ledger_users'))

    default_context = {
        'top_title': 'Update User',
        'success_alert': 'The User updated successfully.',
        'form_top_legend': 'Update Ledger User Records',
        'return_url': 'ledger_users',
        'edit_url': f'edit_ledger_user {ledger_record.primary_key}'
    }

    if request.method == 'POST':
        form = LedgerUserForm(request.POST, instance=ledger_record)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'success': True,
                'record': ledger_record
            }
            context.update(default_context)
            return render(request, 'edit.html', context=context)

    form = LedgerUserForm(instance=ledger_record)
    context = {
        'form': form,
        'success': False,
        'record': ledger_record
    }
    context.update(default_context)
    return render(request, 'edit.html', context=context)


def delete_ledger_user(request, record_id):
    ledger_record = get_object_or_404(LedgerUser, primary_key=record_id)
    if not ledger_record:
        return redirect(request, "ledger_users.html")

    if request.method == 'POST':
        ledger_record.delete()
    return HttpResponseRedirect(reverse(f'ledger_users'))


""" ---------------- Ledger DETAILS -------------------------"""


def ledger_details(request, user_id):
    default_context = {
        'ledger_detail_url': 'ledger_details',
        'edit_ledger_url': 'edit_ledger',
        'add_ledger_url': 'add_ledger',
        'delete_ledger_url': 'delete_ledger',
    }

    user = get_object_or_404(LedgerUser, primary_key=user_id) if user_id else None
    if not user:
        return redirect(reverse('ledger_details', args=[user_id]))

    try:
        latest_balance_record = LedgerRecord.objects.filter(user_id=user)
        length_of_records = len(latest_balance_record)
        calculated_index = length_of_records - 1 if length_of_records > 0 else 0
        latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
        previous_balance = latest_balance_record.balance
    except (LedgerRecord.DoesNotExist, IndexError):
        previous_balance = 0

    records = LedgerRecord.objects.filter(user_id=user)
    context = {'user': user, 'records': records, 'previous_balance': previous_balance}
    context.update(default_context)
    return render(request, 'ledger_register.html', context=context)


def add_ledger(request, user_id):
    user = get_object_or_404(LedgerUser, primary_key=user_id) if user_id else None

    if not user:
        return redirect(reverse('ledger_details', args=[user_id]))

    # Get the latest record to get the previous balance
    try:
        latest_balance_record = LedgerRecord.objects.filter(user_id=user)
        length_of_records = len(latest_balance_record)
        calculated_index = length_of_records - 1 if length_of_records > 0 else 0
        latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
        previous_balance = latest_balance_record.balance
    except (LedgerRecord.DoesNotExist, IndexError):
        previous_balance = 0

    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.instance.user_id = user
            form.save()
        return redirect(reverse('ledger_details', args=[user_id]))
    else:
        # Set initial balance in the form to be the previous balance
        form = LedgerForm(initial={'balance': previous_balance})

    context = {
        'user': user,
        'records': LedgerRecord.objects.filter(user_id=user),
        'form': form,
        'previous_balance': previous_balance,
    }
    return render(request, 'ledger_register.html', context)


def edit_ledger(request, record_id):
    ledger_record = get_object_or_404(LedgerRecord, primary_key=record_id)
    if not ledger_record:
        return redirect(reverse('ledger_users'))

    default_context = {
        'top_title': 'Update Ledger',
        'success_alert': 'The Ledger updated successfully.',
        'form_top_legend': 'Update Ledger Records',
        'return_url': f'ledger_details {ledger_record.user_id.primary_key}',
        'edit_url': f'edit_ledger {ledger_record.primary_key}'
    }

    if request.method == 'POST':
        form = LedgerForm(request.POST, instance=ledger_record)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'success': True,
                'record': ledger_record
            }
            context.update(default_context)
            return render(request, 'edit.html', context=context)

    form = LedgerForm(instance=ledger_record)
    context = {
        'form': form,
        'success': False,
        'record': ledger_record
    }
    context.update(default_context)
    return render(request, 'edit.html', context=context)


def delete_ledger(request, record_id):
    ledger_record = get_object_or_404(LedgerRecord, primary_key=record_id)
    if not ledger_record:
        return redirect(reverse('ledger_users'))

    if request.method == 'POST':
        ledger_record.delete()
    return HttpResponseRedirect(reverse(f'ledger_details', args=[ledger_record.user_id.primary_key]))
