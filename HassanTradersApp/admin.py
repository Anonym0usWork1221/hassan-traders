from django.contrib import admin
from .models import LedgerRecord, LedgerUser, StockUser, StockRecord


admin.site.register(LedgerRecord)
admin.site.register(LedgerUser)
admin.site.register(StockUser)
admin.site.register(StockRecord)

