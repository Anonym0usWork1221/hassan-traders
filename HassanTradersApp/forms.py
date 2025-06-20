from .models import LedgerRecord, LedgerUser, StockUser, StockRecord, ProfitRecord, ProfitUser
from datetime import date
from django import forms


# -------------------------------- LEDGER FORM --------------------------------

class LedgerForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=["%Y-%m-%d"],
        initial=date.today
    )

    class Meta:
        model = LedgerRecord
        fields = ['date', 'particulars', 'folio', 'debit', 'credit', 'dr_or_cr', 'balance']
        labels = {
            'date': 'Date',
            'particulars': 'Particulars',
            'folio': 'Folio',
            'debit': 'Debit',
            'credit': 'Credit',
            'dr_or_cr': 'DR/CR',
            'balance': 'Balance',
        }
        widgets = {
            'particulars': forms.TextInput(attrs={'class': 'form-control'}),
            'folio': forms.TextInput(attrs={'class': 'form-control'}),
            'debit': forms.NumberInput(attrs={'class': 'form-control'}),
            'credit': forms.NumberInput(attrs={'class': 'form-control'}),
            'dr_or_cr': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class LedgerUserForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=["%Y-%m-%d"],
        initial=date.today
    )

    CLIENT_CHOICES = [
        ('M', 'Company'),
        ('C', 'Customer'),
    ]

    client_type = forms.ChoiceField(
        choices=CLIENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='C'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_type'].initial = 'C'

    class Meta:
        model = LedgerUser
        fields = ['date', 'name', 'client_type']
        labels = {
            'date': 'Date',
            'name': 'Name',
            'client_type': 'Client Type'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


# -------------------------------- STOCK FORM --------------------------------

class StockForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=["%Y-%m-%d"],
        initial=date.today
    )

    class Meta:
        model = StockRecord
        fields = ['date', 'particulars', 'bill_no', 'receipt', 'issued', 'balance', 'remarks']
        labels = {
            'date': 'Date',
            'particulars': 'Particulars',
            'bill_no': 'Bill No.',
            'receipt': 'Receipt',
            'issued': 'Issued',
            'balance': 'Balance',
            'remarks': 'Remarks',
        }
        widgets = {
            'particulars': forms.TextInput(attrs={'class': 'form-control'}),
            'bill_no': forms.TextInput(attrs={'class': 'form-control'}),
            'receipt': forms.NumberInput(attrs={'class': 'form-control'}),
            'issued': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StockUserForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=["%Y-%m-%d"],
        initial=date.today
    )

    CLIENT_CHOICES = [
        ('M', 'Company'),
        ('C', 'Customer'),
    ]

    client_type = forms.ChoiceField(
        choices=CLIENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='C'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_type'].initial = 'C'

    class Meta:
        model = StockUser
        fields = ['date', 'name', 'client_type']
        labels = {
            'date': 'Date',
            'name': 'Name',
            'client_type': 'Client Type'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


# -------------------------------- PROFIT FORM --------------------------------

class ProfitForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=["%Y-%m-%d"],
        initial=date.today
    )

    class Meta:
        model = ProfitRecord
        fields = ['date', 'quantity', 'no_of_substance', 'purchase', 'sale', 'diff', 'balance']
        labels = {
            'date': 'Date',
            'quantity': 'Quantity',
            'no_of_substance': 'No. of Substance',
            'purchase': 'Purchase',
            'sale': 'Sale',
            'diff': 'Difference',
            'balance': 'Balance',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_of_substance': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale': forms.NumberInput(attrs={'class': 'form-control'}),
            'diff': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ProfitUserForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=["%Y-%m-%d"],
        initial=date.today
    )

    CLIENT_CHOICES = [
        ('M', 'Company'),
        ('C', 'Customer'),
    ]

    client_type = forms.ChoiceField(
        choices=CLIENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='C'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_type'].initial = 'C'

    class Meta:
        model = ProfitUser
        fields = ['date', 'name', 'client_type']
        labels = {
            'date': 'Date',
            'name': 'Name',
            'client_type': 'Client Type'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
