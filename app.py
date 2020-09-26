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

    print(request.form)

    new_customer = {
        'id': random.randint(1000, 9999),
        'first_name': first_name,
        'last_name': first_name,
        'email': email,
        'can_send': can_send,
    }

    database.append(new_customer)

    with open('customers.json', 'w') as fp:
        json.dump(database, fp)

    return redirect(url_for('show_customers'))


# or customer_id = int(customer_id)
@app.route('/customers/<int:customer_id>/edit')
def show_edit_customer(customer_id):
    #  -- Steps to find the customer that we are supposed to edit --
    # 1. initialise customer_to_edit = None
    customer_to_edit = None
    # 2. for loop to iterate through database [json data],
    for each_customer in database:
        # 3. Check if customer_id (keyed in) is equal to [json data] id
        if each_customer["id"] == customer_id:
            #4. if true, assign each_customer to customer_to_edit
            customer_to_edit = each_customer
            break
    print('customer_to_edit:', customer_to_edit)

    # checks customer_to_edit value (or checks customer id) 
    if customer_to_edit:
        # returns the edit customer template based on customer id above
        return render_template('edit_customer.template.html',
                                customer=customer_to_edit)
    # if customer_to_edit (customer id) is not found, return customer {id} not found
    else:
        return f"The customer with the id of {customer_id} is not found"



@app.route('/customers/<int:customer_id>/edit', methods=["POST"])
def process_edit_customer(customer_id):
    customer_to_edit = None
    for each_customer in database:
        if each_customer["id"] == customer_id:
            customer_to_edit = each_customer
            break

        # checks customer_to_edit value (or checks customer id) 
    if customer_to_edit:
        # obtain value from update form and update it in customer_to_edit [data]
        customer_to_edit["first_name"] = request.form.get('first_name')
        customer_to_edit["last_name"] = request.form.get('last_name')
        customer_to_edit["email"] = request.form.get('email')

        if 'can_send' in request.form:
            print("send marketing material true")
            customer_to_edit['send_marketing_material'] = True
        else:
            print("send marketing material False")
            customer_to_edit['send_marketing_material'] = False

        with open('customers.json', 'w') as fp:
            json.dump(database, fp)
        return redirect(url_for('show_customers'))

    else:
        return f"The customer {customer_id} is not found."


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            # only one program can run on one port, therefore flask gives error if it is run 2nd time
            port=int(os.environ.get('PORT')),
            debug=True)
