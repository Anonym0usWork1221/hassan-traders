from django.db import models
from uuid import uuid4
from datetime import date


class LedgerUser(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    date = models.DateField(default=date.today)
    name = models.CharField(max_length=200)
    CLIENT_CHOICES = [
        ('M', 'Company'),
        ('C', 'Customer'),
    ]
    client_type = models.CharField(max_length=1, choices=CLIENT_CHOICES, default='C')

    def __str__(self):
        return self.name


class LedgerRecord(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    user_id = models.ForeignKey(LedgerUser, on_delete=models.CASCADE, related_name='ledger_records')
    date = models.DateField(default=date.today)
    particulars = models.CharField(max_length=200)
    folio = models.CharField(max_length=100, default="", blank=True)
    debit = models.IntegerField(null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True)
    dr_or_cr = models.CharField(max_length=100, blank=True)
    balance = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.particulars}-{self.balance}"


class StockUser(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    date = models.DateField(default=date.today)
    name = models.CharField(max_length=200)
    CLIENT_CHOICES = [
        ('M', 'Company'),
        ('C', 'Customer'),
    ]
    client_type = models.CharField(max_length=1, choices=CLIENT_CHOICES, default='C')

    def __str__(self):
        return self.name


class StockRecord(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    user_id = models.ForeignKey(StockUser, on_delete=models.CASCADE, related_name='stock_records')
    date = models.DateField(default=date.today)
    particulars = models.CharField(max_length=200)
    bill_no = models.CharField(max_length=100, default="", blank=True)
    receipt = models.IntegerField(null=True, blank=True)
    issued = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.particulars}-{self.balance}"


class ProfitUser(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    date = models.DateField(default=date.today)
    name = models.CharField(max_length=200)
    CLIENT_CHOICES = [
        ('M', 'Company'),
        ('C', 'Customer'),
    ]
    client_type = models.CharField(max_length=1, choices=CLIENT_CHOICES, default='C')

    def __str__(self):
        return self.name


class ProfitRecord(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid4, editable=True)
    user_id = models.ForeignKey(ProfitUser, on_delete=models.CASCADE, related_name='profit_records')
    date = models.DateField(default=date.today)
    quantity = models.IntegerField(null=True, blank=True)
    no_of_substance = models.CharField(max_length=200)
    purchase = models.IntegerField(null=True, blank=True)
    sale = models.IntegerField(null=True, blank=True)
    diff = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.no_of_substance}-{self.balance}"

