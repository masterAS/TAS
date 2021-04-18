from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,redirect
)
from sqlalchemy import and_
from werkzeug.exceptions import abort
from sqlalchemy import create_engine
engine = create_engine('sqlite:///tas_db.db', echo = True)
from tasApp.auth import login_required
from . import db_initialization as db
from sqlalchemy.orm import sessionmaker
from datetime import date
import time

bp = Blueprint('ledger', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        t_date= request.form['date']
        return redirect(url_for('ledger.display',vehicle_number=vehicle_number,t_date=t_date))
    return render_template('search.html')

@bp.route('/display')
@login_required
def display():
    vehicle_number = request.args.get('vehicle_number')
    t_date = request.args.get('t_date')
    db_session = sessionmaker(bind = engine)
    d_session = db_session()
    rows = d_session.query(db.Account).filter(and_(db.Account.vehicle_number ==vehicle_number,
         db.Account.transaction_date==str(t_date)) ).all()
    for r in rows:
            print(r)
    if rows is not None:
        return render_template('display.html', rows=rows)

@bp.route('/searchVehicle', methods=('GET', 'POST'))
def vehicle():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        return redirect(url_for('ledger.addentry', vehicle_number=vehicle_number))
    return render_template('vehicle.html')  

@bp.route('/addentry', methods=('GET', 'POST'))
def addentry():
    if request.method == 'POST':
        db_session = sessionmaker(bind = engine)
        d_session = db_session()
        vehicle_number = request.form['vehicle_number']
        trip_no = request.form['trip_no']
        transaction_type = request.form['transaction_type']
        transaction_description = request.form['transaction_description']
        t_date= request.form['date']
        rows = d_session.query(db.Account).filter(and_(db.Account.vehicle_number ==vehicle_number,
        db.Account.transaction_date==str(t_date)) ).all()
        net_bal = 0
        bal =0
        if len(rows)!=0:
            bal = rows[-1].balance
        amount = request.form['amount']
        if transaction_type =='debit':
            amount_debit = int(amount)
            amount_credit = 0
            net_bal = bal - int(amount)
        else:
            amount_credit = int(amount)
            net_bal = bal + int(amount)
            amount_debit = 0
        # To be fixed later
        balance = net_bal
        username = session.get('user_id')
        current_time = str(time.strftime("%H:%M:%S",time.localtime()))
        
        account = db.Account(vehicle_number=vehicle_number,username=username, transaction_type=transaction_type,
        transaction_description = transaction_description , amount_debit=amount_debit, amount_credit =amount_credit,
        balance = balance, transaction_date=t_date , transaction_time =current_time)
        d_session.add(account)
        d_session.commit()
        return redirect(url_for('ledger.display',vehicle_number=vehicle_number,t_date=t_date))
    else:
        vehicle_number = request.args.get('vehicle_number')
        return redirect(url_for('ledger.addentry',vehicle_number=vehicle_number))