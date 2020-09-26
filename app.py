from flask import Flask, render_template, request, redirect, url_for
import os
import json
import random

app = Flask(__name__)
database = {}
with open('customers.json') as fp:
    database = json.load(fp)


@app.route('/')
def home():
    return render_template('home.template.html')

@app.route('/customers')
def show_customers():
    return render_template('customers.template.html', all_customers=database)

@app.route('/customers/add')
def add_customers():
    return render_template('add_customer.template.html', page_title="Add Customer")


@app.route('/customers/add', methods=["POST"])
def process_add_customers():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    if 'can_send' in request.form:
        can_send = True
    else:
        can_send = False

    new_customer = {
        'id': random.randint(1000,9999),
        'first_name': first_name,
        'last_name': first_name,
        'email': email,
        'can_send': can_send,
    }

    database.append(new_customer)

    with open('customers.json', 'w') as fp:
        json.dump(database, fp)

    return redirect(url_for('show_customers'))



# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            # only one program can run on one port, therefore flask gives error if it is run 2nd time
            port=int(os.environ.get('PORT')),
            debug=True)
