from django.urls import path
from . import views, ledger_views, stock_views, profit_loss_views

urlpatterns = [
    # -------------------- Landing Views --------------------

    path('', views.index, name='index'),
    path('sync_data/', views.sync_data_with_firebase, name='sync_data'),
    path('update_data/', views.update_data, name='update_data'),

    # -------------------- Profit Views --------------------
    # Profit USERS
    path('profit_users/', profit_loss_views.profit_users, name='profit_users'),
    path('add_profit_user/', profit_loss_views.add_profit_user, name='add_profit_user'),
    path('edit_profit_user/<uuid:record_id>/', profit_loss_views.edit_profit_user, name='edit_profit_user'),
    path('delete_profit_user/<uuid:record_id>/', profit_loss_views.delete_profit_user, name='delete_profit_user'),

    # Profit DETAILS
    path('profit_details/<uuid:user_id>', profit_loss_views.profit_details, name='profit_details'),
    path('add_profit/<uuid:user_id>', profit_loss_views.add_profit, name='add_profit'),
    path('edit_profit/<uuid:record_id>/', profit_loss_views.edit_profit, name='edit_profit'),
    path('delete_profit/<uuid:record_id>/', profit_loss_views.delete_profit, name='delete_profit'),

    # -------------------- Stock Views --------------------
    # Stock USERS
    path('stock_users/', stock_views.stock_users, name='stock_users'),
    path('add_stock_user/', stock_views.add_stock_user, name='add_stock_user'),
    path('edit_stock_user/<uuid:record_id>/', stock_views.edit_stock_user, name='edit_stock_user'),
    path('delete_stock_user/<uuid:record_id>/', stock_views.delete_stock_user, name='delete_stock_user'),

    # Stock DETAILS
    path('stock_details/<uuid:user_id>', stock_views.stock_details, name='stock_details'),
    path('add_stock/<uuid:user_id>', stock_views.add_stock, name='add_stock'),
    path('edit_stock/<uuid:record_id>/', stock_views.edit_stock, name='edit_stock'),
    path('delete_stock/<uuid:record_id>/', stock_views.delete_stock, name='delete_stock'),

    # -------------------- Ledger Views --------------------
    # Ledger USERS
    path('ledger_users/', ledger_views.ledger_users, name='ledger_users'),
    path('add_ledger_user/', ledger_views.add_ledger_user, name='add_ledger_user'),
    path('edit_ledger_user/<uuid:record_id>/', ledger_views.edit_ledger_user, name='edit_ledger_user'),
    path('delete_ledger_user/<uuid:record_id>/', ledger_views.delete_ledger_user, name='delete_ledger_user'),

    # Ledger DETAILS
    path('ledger_details/<uuid:user_id>', ledger_views.ledger_details, name='ledger_details'),
    path('add_ledger/<uuid:user_id>', ledger_views.add_ledger, name='add_ledger'),
    path('edit_ledger/<uuid:record_id>/', ledger_views.edit_ledger, name='edit_ledger'),
    path('delete_ledger/<uuid:record_id>/', ledger_views.delete_ledger, name='delete_ledger')
]
