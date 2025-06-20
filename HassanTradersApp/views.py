from .models import LedgerRecord, StockRecord, LedgerUser, StockUser, ProfitRecord, ProfitUser
from HassanTraders.settings import ENABLE_FIREBASE
from django.shortcuts import render, redirect
from plotly.subplots import make_subplots
from background_task import background
import plotly.graph_objects as go
from django.urls import reverse
from firebase_admin import db
import requests

if not ENABLE_FIREBASE:
    ref = None
else:
    ref = db.reference("/")


def index(request):
    sync_data_with_firebase(repeat=60, repeat_until=None)
    ledger_data = LedgerRecord.objects.all()
    stock_data = StockRecord.objects.all()
    profit_data = ProfitRecord.objects.all()
    fig_ledger = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                               subplot_titles=("Ledger Record",))

    fig_ledger.add_trace(go.Scatter(x=[record.date for record in ledger_data],
                                    y=[record.balance for record in ledger_data],
                                    mode='lines+markers', name="Ledger Balance"))

    fig_stock = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                              subplot_titles=("Stock Record",))

    fig_stock.add_trace(go.Scatter(x=[record.date for record in stock_data],
                                   y=[record.balance for record in stock_data],
                                   mode='lines+markers', name="Stock Balance"))

    fig_profit = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                               subplot_titles=("Profit Gain Register",))
    fig_profit.add_trace(go.Scatter(x=[record.date for record in profit_data],
                                    y=[record.balance for record in profit_data],
                                    mode='lines+markers', name="Profit Gain"))

    fig_ledger.update_layout(title_text="Ledger Record", showlegend=True)
    fig_stock.update_layout(title_text="Stock Record", showlegend=True)
    fig_profit.update_layout(title_text="Profit Gain Register", showlegend=True)

    profit_graph_div = fig_profit.to_html(full_html=False)
    ledger_graph_div = fig_ledger.to_html(full_html=False)
    stock_graph_div = fig_stock.to_html(full_html=False)

    context = {
        'ledger_graph': ledger_graph_div,
        'stock_graph': stock_graph_div,
        'profit_graph': profit_graph_div,
    }
    return render(request, 'index.html', context=context)


@background(schedule=60)  # Run this task every 60 seconds (adjust as needed)
def sync_data_with_firebase():
    if not ENABLE_FIREBASE:
        return
    try:
        requests.get("https://www.google.com", timeout=5)
        internet_available = True
    except requests.ConnectionError:
        internet_available = False
    print(f"Syncing: {internet_available}")
    if internet_available:
        ledger_users = LedgerUser.objects.all()
        stock_users = StockUser.objects.all()
        profit_users = ProfitUser.objects.all()

        for user in profit_users:
            profit_data = ProfitRecord.objects.filter(user_id=user)
            profit_records = []
            for record in profit_data:
                profit_records.append({
                    "primary_key": str(record.primary_key),
                    "date": str(record.date),
                    "quantity": record.quantity,
                    "no_of_substance": record.no_of_substance,
                    "purchase": record.purchase,
                    "sale": record.sale,
                    "diff": record.diff,
                    "balance": record.balance
                })
            ref.child("profit_users").child(str(user.primary_key)).set({
                "date": str(user.date),
                "name": user.name,
                "client_type": user.client_type,
                "records": profit_records
            })

        # Sync Ledger data
        for user in ledger_users:
            ledger_data = LedgerRecord.objects.filter(user_id=user)
            ledger_records = []
            for record in ledger_data:
                ledger_records.append({
                    "primary_key": str(record.primary_key),
                    "date": str(record.date),
                    "particulars": record.particulars,
                    "folio": record.folio,
                    "debit": record.debit,
                    "credit": record.credit,
                    "dr_or_cr": record.dr_or_cr,
                    "balance": record.balance
                })

            ref.child("ledger_users").child(str(user.primary_key)).set({
                "date": str(user.date),
                "name": user.name,
                "client_type": user.client_type,
                "records": ledger_records
            })

        # Sync Stock data
        for user in stock_users:
            stock_data = StockRecord.objects.filter(user_id=user)
            stock_records = []
            for record in stock_data:
                stock_records.append({
                    "primary_key": str(record.primary_key),
                    "date": str(record.date),
                    "particulars": record.particulars,
                    "bill_no": record.bill_no,
                    "receipt": record.receipt,
                    "issued": record.issued,
                    "balance": record.balance,
                    "remarks": record.remarks
                })

            ref.child("stock_users").child(str(user.primary_key)).set({
                "date": str(user.date),
                "name": user.name,
                "client_type": user.client_type,
                "records": stock_records
            })


# -------- Update old data ----------------------------
def update_data(request):
    try:
        requests.get("https://www.google.com", timeout=5)
        internet_available = True
    except requests.ConnectionError:
        internet_available = False
    print(f"Updating data: {internet_available}")
    if internet_available:
        fetched_data = ref.get()
        if fetched_data:
            unpack_users(fetched_data)
            unpack_records(fetched_data)
    return redirect(reverse('index'))


def unpack_users(fetched_data):
    data_types = {"ledger_users": LedgerUser, "stock_users": StockUser, "profit_users": ProfitUser}
    for data_type in data_types.keys():
        user_records = fetched_data[data_type]
        for user in user_records:
            user_data = fetched_data[data_type][user]
            user_primary_key = user
            user_client_type = user_data['client_type']
            user_date = user_data['date']
            user_name = user_data['name']

            try:
                data_types[data_type].objects.get(pk=user_primary_key)
                continue
            except data_types[data_type].DoesNotExist:
                data_types[data_type].objects.create(
                    primary_key=user_primary_key,
                    date=user_date,
                    name=user_name,
                    client_type=user_client_type
                )


def unpack_records(fetched_data):
    data_types = {"ledger_users": LedgerRecord, "stock_users": StockRecord, "profit_users": ProfitRecord}
    for data_type in data_types.keys():
        user_records = fetched_data[data_type]
        for user in user_records:
            user_data = fetched_data[data_type][user]
            record = user_data['records'] if "records" in user_data else []
            if data_type == "ledger_users":
                for ledger_record_data in record:
                    ledger_record_primary_key = ledger_record_data["primary_key"]
                    ledger_record_date = ledger_record_data["date"]
                    ledger_record_particulars = ledger_record_data["particulars"]
                    ledger_record_folio = ledger_record_data["folio"]
                    ledger_record_debit = ledger_record_data["debit"] if "debit" in ledger_record_data else None
                    ledger_record_credit = ledger_record_data["credit"] if "credit" in ledger_record_data else None
                    ledger_record_dr_or_cr = ledger_record_data["dr_or_cr"]
                    ledger_record_balance = ledger_record_data["balance"]

                    try:
                        data_types[data_type].objects.get(pk=ledger_record_primary_key)
                        continue
                    except data_types[data_type].DoesNotExist:
                        user_instance = LedgerUser.objects.get(pk=user)
                        data_types[data_type].objects.create(
                            primary_key=ledger_record_primary_key,
                            user_id=user_instance,
                            date=ledger_record_date,
                            particulars=ledger_record_particulars,
                            folio=ledger_record_folio,
                            debit=ledger_record_debit,
                            credit=ledger_record_credit,
                            dr_or_cr=ledger_record_dr_or_cr,
                            balance=ledger_record_balance
                        )
            elif data_type == "stock_users":
                for stock_record_data in record:
                    stock_record_primary_key = stock_record_data["primary_key"]
                    stock_record_date = stock_record_data["date"]
                    stock_record_particulars = stock_record_data["particulars"]
                    stock_record_bill_no = stock_record_data["bill_no"]
                    stock_record_receipt = stock_record_data["receipt"] if "receipt" in stock_record_data else None
                    stock_record_issued = stock_record_data["issued"] if "issued" in stock_record_data else None
                    stock_record_balance = stock_record_data["balance"]
                    stock_record_remarks = stock_record_data["remarks"]

                    try:
                        data_types[data_type].objects.get(pk=stock_record_primary_key)
                        continue
                    except data_types[data_type].DoesNotExist:
                        user_instance = StockUser.objects.get(pk=user)
                        data_types[data_type].objects.create(
                            primary_key=stock_record_primary_key,
                            user_id=user_instance,
                            date=stock_record_date,
                            particulars=stock_record_particulars,
                            bill_no=stock_record_bill_no,
                            receipt=stock_record_receipt,
                            issued=stock_record_issued,
                            balance=stock_record_balance,
                            remarks=stock_record_remarks
                        )
            elif data_type == "profit_users":
                for profit_record_data in record:
                    profit_record_primary_key = profit_record_data["primary_key"]
                    profit_record_date = profit_record_data["date"]
                    profit_record_quantity = profit_record_data["quantity"] if "quantity" in profit_record_data else None
                    profit_record_no_of_substance = profit_record_data["no_of_substance"]
                    profit_record_purchase = profit_record_data["purchase"] if "purchase" in profit_record_data else None
                    profit_record_sale = profit_record_data["sale"] if "sale" in profit_record_data else None
                    profit_record_diff = profit_record_data["diff"] if "diff" in profit_record_data else None
                    profit_record_balance = profit_record_data["balance"] if "balance" in profit_record_data else None

                    try:
                        data_types[data_type].objects.get(pk=profit_record_primary_key)
                        continue
                    except data_types[data_type].DoesNotExist:
                        user_instance = ProfitUser.objects.get(pk=user)
                        data_types[data_type].objects.create(
                            primary_key=profit_record_primary_key,
                            user_id=user_instance,
                            date=profit_record_date,
                            quantity=profit_record_quantity,
                            no_of_substance=profit_record_no_of_substance,
                            purchase=profit_record_purchase,
                            sale=profit_record_sale,
                            diff=profit_record_diff,
                            balance=profit_record_balance
                        )
