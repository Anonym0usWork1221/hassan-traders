import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate("./static/google-services.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://test-app-5e321-default-rtdb.firebaseio.com/"
})
ref = db.reference("/")
# r = ref.get()
r = {'ledger_users': {'8554e248-4624-4ea8-b44a-193179c657cb': {'client_type': 'M', 'date': '2023-07-28', 'name': 'Proxy GitPusher', 'records': [{'balance': 20, 'date': '2023-07-28', 'debit': 20, 'dr_or_cr': 'DR', 'folio': '', 'particulars': 'Added Manually', 'primary_key': '6254484b-120a-417f-9b0d-b110399eb06f'}]}, 'ca96b859-5056-46f6-87c5-297d4dd7fd20': {'client_type': 'C', 'date': '2023-07-27', 'name': 'Abdul Moez', 'records': [{'balance': 10, 'date': '2023-07-28', 'debit': 10, 'dr_or_cr': 'DR', 'folio': '', 'particulars': 'Abbas', 'primary_key': 'b01d344c-6592-4cb7-bbba-cc53aac33642'}, {'balance': 30, 'date': '2023-07-28', 'debit': 20, 'dr_or_cr': 'DR', 'folio': '', 'particulars': 'Shakeeel', 'primary_key': '83d6df56-4684-442f-ad88-76ad15b22fd9'}, {'balance': 0, 'credit': 30, 'date': '2023-07-28', 'dr_or_cr': 'CR', 'folio': '', 'particulars': 'Added Manually', 'primary_key': '414e9365-f7a3-4d30-bcee-3572b4fc5b2d'}]}}, 'stock_users': {'53a3e9f1-3655-4f64-8185-fb160022547a': {'client_type': 'C', 'date': '2023-07-28', 'name': 'Abdul Moez', 'records': [{'balance': 20, 'bill_no': '1', 'date': '2023-07-28', 'particulars': 'Abbas', 'primary_key': 'a03012ae-aaf6-4ae3-b973-4d115e97fc31', 'receipt': 20, 'remarks': 'ASJAD'}, {'balance': 18, 'bill_no': '2', 'date': '2023-07-28', 'issued': 2, 'particulars': 'Shakeeel', 'primary_key': 'bd0e8340-8aea-4743-8968-0539d3ef054c', 'remarks': ''}]}}}
ledger_users = r["ledger_users"]
for user in ledger_users:
    user_primary_key = user
    ledger_user_data = r["ledger_users"][user]
    user_client_type = ledger_user_data['client_type']
    user_date = ledger_user_data['date']
    user_name = ledger_user_data['name']
    ledger_record = ledger_user_data['records']
    print(user_primary_key)
    print(user_client_type)
    print(user_date)
    print(user_name)
    for ledger_record_data in ledger_record:
        ledger_record_primary_key = ledger_record_data["primary_key"]
        ledger_record_date = ledger_record_data["date"]
        ledger_record_particulars = ledger_record_data["particulars"]
        ledger_record_folio = ledger_record_data["folio"]
        ledger_record_debit = ledger_record_data["debit"] if "debit" in ledger_record_data else None
        ledger_record_credit = ledger_record_data["credit"] if "credit" in ledger_record_data else None
        ledger_record_dr_or_cr = ledger_record_data["dr_or_cr"]
        ledger_record_balance = ledger_record_data["balance"]
        print(ledger_record_primary_key)
        print(ledger_record_date)
        print(ledger_record_particulars)
        print(ledger_record_folio)
        print(ledger_record_debit)
        print(ledger_record_credit)
        print(ledger_record_dr_or_cr)
        print(ledger_record_balance)
