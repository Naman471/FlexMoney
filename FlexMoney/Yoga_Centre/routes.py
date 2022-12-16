from Yoga_Centre import app
from flask import render_template, url_for, redirect, flash
from Yoga_Centre.models import BatchDetails, Payment, User
from Yoga_Centre.forms import RegisterForm, BatchForm, PaymentForm
from Yoga_Centre import db
from flask_login import login_user

@app.route('/')  
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/base')
def base_page():
    return render_template('base.html')

@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
        email_address=form.email.data,
        password=form.password_1.data,
        age=form.age.data,)

        batch_details = BatchDetails(username=form.username.data,
        email_address=form.email.data,
        password=form.password_1.data,
        last_update_month=form.month.data,
        current_batch_timing=form.batch_timing.data,)

        payment_details = Payment(username=form.username.data,
        email_address=form.email.data,
        password=form.password_1.data,
        last_month_paid=form.month.data,)

        db.session.add(user_to_create)
        db.session.add(batch_details)
        db.session.add(payment_details)
        db.session.commit()
        flash(f'Account Created for {form.username.data}',category='success')

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}',category='danger')

    return render_template('register.html', form = form)

def month_to_number(month_to_convert):
    month = {	
        'January':1,
		'February':2,
		'March':3,
		'April':4,
		'May':5,
		'June':6,
		'July':7,
		'August':8,
		'September':9,
		'October':10,
		'November':11,
		'December':12		
        }
    return month[month_to_convert]

@app.route('/batch_change',methods=['GET','POST'])
def batch_change_page():
    form=BatchForm()
    if form.validate_on_submit():
        attempted_user=BatchDetails.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)

            last_updated_month=attempted_user.last_update_month
            new_month=form.month.data
            last_updated_month_no=month_to_number(last_updated_month)
            new_month_no=month_to_number(new_month)
            last_batch=attempted_user.current_batch_timing

            if last_batch==form.new_batch_timing.data:
                flash(f'Your previous batch timing is same as the new chosen timing!', category='danger')
            elif last_updated_month_no==new_month_no:
                flash(f'Failed to change the batch timing for {attempted_user.username}! You\'ve already updated the timings for this month. Try again next month!', category='danger')
            elif last_updated_month_no==12 or new_month_no>last_updated_month_no:
                attempted_user.last_update_month=new_month
                attempted_user.current_batch_timing=form.new_batch_timing.data
                db.session.commit()
                flash(f'Success! Changes made for {attempted_user.username}. New batch timings are {attempted_user.current_batch_timing}',category='success')
            elif new_month_no<last_updated_month_no:
                flash(f'Illegal change! Batch changes cannot be made for month prior to {attempted_user.last_update_month} ', category='danger')
            else:
                flash(f'Failed to change the batch timing for {attempted_user.username}! You can change your timings next month', category='danger')
            
        else:
            flash('Username and Password are not matching. Please try again!',category='danger')

    return render_template('batch_change.html',form = form)

@app.route('/payment',methods=['GET','POST'])
def payment_page():
    form=PaymentForm()
    if form.validate_on_submit():
        attempted_user=Payment.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)

            last_paid_month=attempted_user.last_month_paid
            new_month=form.month.data
            last_paid_month_no=month_to_number(last_paid_month)
            new_month_no=month_to_number(new_month)

            if last_paid_month_no==new_month_no:
                flash(f'Payment already made for this month',category='danger')
            elif last_paid_month_no==12 and new_month_no==1:
                attempted_user.last_month_paid=new_month
                db.session.commit()
                flash(f'Your payment of INR 500 is recieved. Thank you {attempted_user.username}!',category='success')
            elif new_month_no==last_paid_month_no+1:
                attempted_user.last_month_paid=new_month
                db.session.commit()
                flash(f'Your payment of INR 500 is recieved. Thank you {attempted_user.username}!',category='success')
            else:
                flash(f'Kindly pay for prior months first. You last made a payment for {attempted_user.last_month_paid}!',category='danger')
        else:
            flash('Username and Password are not matching. Please try again!',category='danger')
    return render_template('payment_page.html', form= form)
