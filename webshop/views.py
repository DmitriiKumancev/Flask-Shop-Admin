from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Item
from . import db 
import json
from cloudipsp import Api, Checkout

views = Blueprint('views', __name__)


@views.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.htm', data=items)


@views.route('/about')
def about():
    return render_template('about.htm')


@views.route('/support')
def support():
    return render_template('support.htm')

@views.route('/koks')
def koks():
    return render_template('koks.htm')

@views.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@views.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Oops, something went wrong. Try again!"
    else:
        return render_template('create.htm')