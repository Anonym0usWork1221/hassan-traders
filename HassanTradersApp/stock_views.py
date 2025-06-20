from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import StockRecord, StockUser
from .forms import StockForm, StockUserForm

""" ---------------- Stock USER -------------------------"""


class StockUserDetailsEnum:
    def __init__(self, user, balance):
        self.user = user
        self.balance = balance


def stock_users(request):
    all_stock_users = StockUser.objects.all()
    stock_users_details = []
    for stock_user in all_stock_users:
        try:
            latest_balance_record = StockRecord.objects.filter(user_id=stock_user)
            length_of_records = len(latest_balance_record)
            calculated_index = length_of_records - 1 if length_of_records > 0 else 0
            latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
            closing_balance = latest_balance_record.balance
        except (StockRecord.DoesNotExist, IndexError):
            closing_balance = 0

        details = StockUserDetailsEnum(user=stock_user, balance=closing_balance)
        # details = {'closing_balance': closing_balance, 'user': stock_user}
        stock_users_details.append(details)

    context = {
        'stock_detail_url': 'stock_details',
        'add_url': 'add_stock_user',
        'edit_stock_url': 'edit_stock_user',
        'delete_stock_url': 'delete_stock_user',
        'records': stock_users_details,
    }

    return render(request, 'stock_users.html', context=context)


def add_stock_user(request):
    if request.method == 'POST':
        form = StockUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('stock_users'))

    else:
        StockUserForm()
    all_stock_users = StockUser.objects.all()
    context = {
        'stock_detail_url': 'stock_details',
        'add_url': 'add_stock_user',
        'edit_stock_url': 'edit_stock_user',
        'delete_stock_url': 'delete_stock_user',
        'records': all_stock_users
    }

    return render(request, 'stock_users.html', context)


def edit_stock_user(request, record_id):
    stock_record = get_object_or_404(StockUser, primary_key=record_id)
    if not stock_record:
        return redirect(reverse('stock_users'))

    default_context = {
        'top_title': 'Update User',
        'success_alert': 'The User updated successfully.',
        'form_top_legend': 'Update stock User Records',
        'return_url': 'stock_users',
        'edit_url': f'edit_stock_user {stock_record.primary_key}'
    }

    if request.method == 'POST':
        form = StockUserForm(request.POST, instance=stock_record)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'success': True,
                'record': stock_record
            }
            context.update(default_context)
            return render(request, 'edit.html', context=context)

    form = StockUserForm(instance=stock_record)
    context = {
        'form': form,
        'success': False,
        'record': stock_record
    }
    context.update(default_context)
    return render(request, 'edit.html', context=context)


def delete_stock_user(request, record_id):
    stock_record = get_object_or_404(StockUser, primary_key=record_id)
    if not stock_record:
        return redirect(reverse('stock_users'))

    if request.method == 'POST':
        stock_record.delete()
    return HttpResponseRedirect(reverse(f'stock_users'))


""" ---------------- Stock DETAILS -------------------------"""


def stock_details(request, user_id):
    default_context = {
        'stock_detail_url': 'stock_details',
        'edit_stock_url': 'edit_stock',
        'add_stock_url': 'add_stock',
        'delete_stock_url': 'delete_stock',
    }
    user = get_object_or_404(StockUser, primary_key=user_id) if user_id else None
    if not user:
        return redirect(reverse('stock_details', args=[user_id]))

    try:
        latest_balance_record = StockRecord.objects.filter(user_id=user)
        length_of_records = len(latest_balance_record)
        calculated_index = length_of_records - 1 if length_of_records > 0 else 0
        latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
        previous_balance = latest_balance_record.balance
    except (StockRecord.DoesNotExist, IndexError):
        previous_balance = 0

    records = StockRecord.objects.filter(user_id=user)
    context = {'user': user, 'records': records, 'previous_balance': previous_balance}
    context.update(default_context)
    return render(request, 'stock_register.html', context=context)


def add_stock(request, user_id):
    user = get_object_or_404(StockUser, primary_key=user_id) if user_id else None

    if not user:
        return redirect(reverse('stock_details', args=[user_id]))

    try:
        latest_balance_record = StockRecord.objects.filter(user_id=user)
        length_of_records = len(latest_balance_record)
        calculated_index = length_of_records - 1 if length_of_records > 0 else 0
        latest_balance_record = latest_balance_record.order_by('-date')[calculated_index]
        previous_balance = latest_balance_record.balance
    except (StockRecord.DoesNotExist, IndexError):
        previous_balance = 0

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.instance.user_id = user
            form.save()
        return redirect(reverse('stock_details', args=[user_id]))
    else:
        form = StockForm(initial={'balance': previous_balance})

    context = {
        'user': user,
        'records': StockRecord.objects.filter(user_id=user),
        'form': form,
        'previous_balance': previous_balance,
    }
    return render(request, 'stock_register.html', context)


def edit_stock(request, record_id):
    stock_record = get_object_or_404(StockRecord, primary_key=record_id)
    if not stock_record:
        return redirect(reverse('stock_users'))

    default_context = {
        'top_title': 'Update stock',
        'success_alert': 'The stock updated successfully.',
        'form_top_legend': 'Update stock Records',
        'return_url': f'stock_details {stock_record.user_id.primary_key}',
        'edit_url': f'edit_stock {stock_record.primary_key}'
    }

    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock_record)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'success': True,
                'record': stock_record
            }
            context.update(default_context)
            return render(request, 'edit.html', context=context)

    form = StockForm(instance=stock_record)
    context = {
        'form': form,
        'success': False,
        'record': stock_record
    }
    context.update(default_context)
    return render(request, 'edit.html', context=context)


def delete_stock(request, record_id):
    stock_record = get_object_or_404(StockRecord, primary_key=record_id)
    if not stock_record:
        return redirect(reverse('stock_users'))

    if request.method == 'POST':
        stock_record.delete()
    return HttpResponseRedirect(reverse(f'stock_details', args=[stock_record.user_id.primary_key]))
