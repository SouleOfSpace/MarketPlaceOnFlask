from market import app, db, stripe_keys
from market.models import Item, User
from flask import render_template, redirect, url_for, flash, request, jsonify
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, CreateItemForm, DeleteITemForm
from flask_login import login_user, logout_user, login_required, current_user

from flask_ssl import *

import stripe


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('flask/home.html')


@app.route('/market', methods=['POST', 'GET'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == 'POST':
        #Purchase item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()

        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulation! You purchased {p_item_object.name} for {p_item_object.price}$', category='success')
            else:
                flash(f'Unfortunately, you do not have enought money to purchase {p_item_object.name} for {p_item_object.price}.'
                      f'\nEnought is {p_item_object.price - current_user.budget}$', category='danger')

        #Sell item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()

        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulation! You sold {s_item_object.name} back to market for {s_item_object.price}$', category='success')
            else:
                flash(f'Something went wrong with selling {s_item_object.name}', category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)

    return render_template('flask/market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfuly! You are now logged in as {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error by create user: {err_msg}', category='danger')

    return render_template('flask/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'You input uncorrect date. Try again, please!', category='danger')

    return render_template('flask/login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out', category='info')
    return redirect(url_for('home_page'))


@login_required
@app.route('/profile/<string:username>/<int:user_id>', methods=["GET", "POST"])
def profile_page(username, user_id):
    items_owned = Item.query.filter_by(owner=current_user.id)
    form_create_item = CreateItemForm()
    form_delete_item = DeleteITemForm()

    #Create new Item
    if request.method == "POST":
        if form_create_item.validate_on_submit():
            try:
                item_to_create = Item(name=form_create_item.name.data,
                                      price=form_create_item.price.data,
                                      barcode=form_create_item.barcode.data,
                                      description=form_create_item.description.data,
                                      owner=current_user.id)
                db.session.add(item_to_create)
                db.session.commit()

                flash(f'New item is created successfully', category='success')
                return redirect(url_for('market_page'))
            except:
                flash(f'Something went wrong by trying to create new item ! Please try again!', category='danger')


        deleted_item = request.form.get('deleted_item')
        d_item_object = Item.query.filter_by(name=deleted_item).first()

        if d_item_object:
            try:
                db.session.delete(d_item_object)
                db.session.commit()

                flash(f'Item "{d_item_object.name}" is deleted successfully', category='success')
                return redirect(url_for('market_page'))
            except:
                flash(f'Something went wrong by trying to delete item! Please try again!', category='danger')

    return render_template('flask/profile.html',
                           form_create_item=form_create_item,
                           items_owned=items_owned,
                           form_delete_item=form_delete_item)
