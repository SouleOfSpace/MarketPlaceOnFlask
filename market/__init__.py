from flask_sqlalchemy import  SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import stripe, os

app = Flask(__name__, static_url_path='', static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'bfceb89382aae12b9bcc9dca'

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51JuB3KIb9zKKo8MkOl9xFupXOC26sSjHCJnEbV5JZsj9mlCXO0sEOdUVayfvjTXkBNSmceXFynCIVgohHS7N3Or900u8y5iKqu'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51JuB3KIb9zKKo8MkOLCSdJhOkLds0cv4EFjQwBBv4VLWJXRG9UGG39csVtACtiqkgZbrm98pzrxzNoM4YJwHxFDz00xvNBoSKl'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

stripe_keys = {
    'secret_key': app.config['STRIPE_SECRET_KEY'],
    'publishable_key': app.config['STRIPE_PUBLIC_KEY']
}

# stripe_keys = {
#     'secret_key': os.environ['SECRET_KEY'],
#     'publishable_key': os.environ['PUBLISHABLE_KEY']
# }
# stripe.api_key = stripe_keys['secret_key']


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from market import routes

def get_products():
    products = {
        'megatutorial': {
            'name': 'The Flask Mega-Tutorial',
            'price': 3900,
        },
        'support': {
            'name': 'Python 1:1 support',
            'price': 20000,
            'per': 'hour',
        },
    }
    return products

@app.route('/stripe')
def index():
    products = get_products()
    print(request.host_url)
    return render_template('stripe/checkout.html', products=products)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'T-shirt',
        },
        'unit_amount': 2000,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
  )

  return redirect(session.url, code=303)

@app.route('/stripe/success')
def success():
    return render_template('stripe/success.html')

@app.route('/stripe/cancel')
def cancel():
    return render_template('stripe/cancel.html')
