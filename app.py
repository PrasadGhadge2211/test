from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING
import os
import pytz

app = Flask(__name__)
MONGO_URI = os.environ.get("MONGODB_URI", "")
client = MongoClient(MONGO_URI)
db = client['pharmacy_db']
LOCAL_TIMEZONE = pytz.timezone('Asia/Kolkata')

@app.template_filter('local_datetime')
def local_datetime_filter(dt):
    if isinstance(dt, str):
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(LOCAL_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def dashboard():
    today_utc = datetime.utcnow()
    expiry_threshold = today_utc + timedelta(days=30)

    # Convert expiry_date from MongoDB to Python datetime if stored as ISODate
    expiring_meds = []
    for med in db.medicines.find({"expiry_date": {"$lte": expiry_threshold}}).sort("expiry_date"):
        med['expiry_date'] = med['expiry_date'].strftime('%Y-%m-%d') if isinstance(med['expiry_date'], datetime) else med['expiry_date']
        expiring_meds.append(med)

    low_stock = list(db.medicines.find({"quantity": {"$lt": 10}}))

    # Prepare recent sales data
    recent_sales = []
    for sale in db.sales.find().sort("date", DESCENDING).limit(5):
        sale['invoice_number'] = sale.get('invoice_number', str(sale['_id'])[-6:])  # fallback if invoice_number not set
        sale['date'] = sale['date'] if isinstance(sale['date'], datetime) else datetime.fromtimestamp(sale['date'] / 1000)
        sale['customer_name'] = sale.get('customer_name', 'Walk-in')
        sale['total_amount'] = float(sale['total_amount'])
        recent_sales.append(sale)

    return render_template(
        'dashboard.html',
        expiring_meds=expiring_meds,
        low_stock=low_stock,
        recent_sales=recent_sales,
        datetime=datetime,
        now=today_utc
    )
if __name__ == '__main__':
    app.run(debug=True)
