# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
import json
from . import admin
from forms import CustomerForm, ItemForm
from .. import db
from ..models import Customer, Item, Bill, BillItem

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Customers Views
@admin.route('/customers', methods=['GET', 'POST'])
@login_required
def list_customers():
    """
    List all customers
    """
    check_admin()

    customers = Customer.query.all()

    return render_template('admin/customers/customers.html',
                           customers=customers, title="Customers")

@admin.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    """
    Add a customer to the database
    """
    check_admin()

    add_customer = True

    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data,
                                TIN=form.TIN.data,phone_number=form.phone_number.data,address=form.address.data)
        try:
            # add customer to the database
            db.session.add(customer)
            db.session.commit()
            flash('You have successfully added a new customer.')
        except Exception, e:
            print str(e)
            db.session.rollback()
            # in case customer name already exists
            flash('Error: customer name already exists.')
            return render_template('admin/customers/customer.html', action="Add",
                           add_customer=add_customer, form=form,
                           customer=customer, title="Add Customer")  

        # redirect to customers page
        return redirect(url_for('admin.list_customers'))

    # load customer template
    return render_template('admin/customers/customer.html', action="Add",
                           add_customer=add_customer, form=form,
                           title="Add Customer")

@admin.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    """
    Edit a customer
    """
    check_admin()

    add_customer = False

    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.name = form.name.data
        customer.TIN = form.TIN.data
        customer.phone_number = form.phone_number.data
        customer.address = form.address.data
        db.session.commit()
        flash('You have successfully edited the customer.')

        # redirect to the customers page
        return redirect(url_for('admin.list_customers'))
    else:
        print "VALIDATION FAILED"
        return render_template('admin/customers/customer.html', action="Edit",
                           add_customer=add_customer, form=form,
                           customer=customer, title="Edit Customer")   
    form.name.data = customer.name 
    form.TIN.data = customer.TIN 
    form.phone_number.data = customer.phone_number 
    form.address.data = customer.address 
    
    return render_template('admin/customers/customer.html', action="Edit",
                           add_customer=add_customer, form=form,
                           customer=customer, title="Edit Customer")

@admin.route('/customers/<int:id>', methods=['GET'])
@login_required
def view_customer(id):
    """
    View a customer
    """
    check_admin()

    add_customer = False

    customer = Customer.query.get_or_404(id)
    bills = db.session.query(Bill).filter(Bill.customer_id==id).all()
    # form = CustomerForm(obj=customer)
    # form.name.data = customer.name 
    # form.TIN.data = customer.TIN 
    # form.phone_number.data = customer.phone_number 
    # form.address.data = customer.address 
    
    return render_template('admin/customers/view_customer.html', action="View",
                           customer=customer,bills=bills, title="View Customer")


@admin.route('/customers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_customer(id):
    """
    Delete a customer from the database
    """
    check_admin()

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('You have successfully deleted the customer.')

    # redirect to the customers page
    return redirect(url_for('admin.list_customers'))

    return render_template(title="Delete Customer")


# Items Views
@admin.route('/items', methods=['GET', 'POST'])
@login_required
def list_items():
    """
    List all items
    """
    check_admin()

    items = Item.query.all()

    return render_template('admin/items/items.html',
                           items=items, title="Items")

@admin.route('/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    """
    Add a item to the database
    """
    check_admin()

    add_item = True

    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data,brand=form.brand.data,price=form.price.data)
        try:
            # add item to the database
            db.session.add(item)
            db.session.commit()
            flash('You have successfully added a new item.')
        except Exception, e:
            print str(e)
            db.session.rollback()
            # in case item name already exists
            flash('Error: item name already exists.')
            return render_template('admin/items/item.html', action="Add",
                           add_item=add_item, form=form,
                           item=item, title="Add Item")  

        # redirect to items page
        return redirect(url_for('admin.list_items'))

    # load item template
    return render_template('admin/items/item.html', action="Add",
                           add_item=add_item, form=form,
                           title="Add Item")

@admin.route('/items/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    """
    Edit a item
    """
    check_admin()

    add_item = False

    item = Item.query.get_or_404(id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.brand = form.brand.data
        item.price = form.price.data
        db.session.commit()
        flash('You have successfully edited the item.')

        # redirect to the items page
        return redirect(url_for('admin.list_items'))
    else:
        print "VALIDATION FAILED"
        return render_template('admin/items/item.html', action="Edit",
                           add_citem=add_item, form=form,
                           item=item, title="Edit Item")   
    form.name.data = item.name 
    form.brand.data = item.brand 
    form.price.data = item.price
    
    return render_template('admin/items/item.html', action="Edit",
                           add_item=add_item, form=form,
                           item=item, title="Edit Item")

@admin.route('/items/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    """
    Delete a item from the database
    """
    check_admin()

    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('You have successfully deleted the item.')

    # redirect to the items page
    return redirect(url_for('admin.list_items'))

    return render_template(title="Delete Item")



@admin.route('/bills', methods=['GET', 'POST'])
@login_required
def list_bills():
    check_admin()

    bills = Bill.query.all()
    return render_template('admin/bills/bills.html',
                           bills=bills, title="Bills")

#returns newly Created Bill ID
def createBillId(data):
    bill = Bill(bill_number=data["bill_number"],customer_id=data["customer_id"],customer_name=data["customer_name"],
        total_bill=data["total_bill"],status=data["payment_status"])
    db.session.add(bill)
    db.session.flush()
    return bill.id

def updateBill(data,bill):
    bill.customer_id = data["customer_id"]
    bill.customer_name = data["customer_name"]
    bill.total_bill = data["total_bill"]
    bill.status = data["payment_status"]
    

def insertBillItems(data,bill_id):
    items = data["items"]
    for i,item in enumerate(items):
        item_id = item["item_id"]
        item_price = item["item_price"]
        quantity = item["quantity"]
        discount = item["discount"]
        total_price = item["total_price"]
        bill_item = BillItem(bill_id = bill_id,item_id=item_id,
            item_price=item_price,quantity=quantity,discount=discount,total_price=total_price)
        db.session.add(bill_item)
    db.session.commit()

@admin.route('/bills/add', methods=['GET', 'POST'])
@login_required
def add_bill():
    """
    Add a bill to the database
    """
    check_admin()
    if request.method == 'POST':
        bill_id = createBillId(request.json)
        insertBillItems(request.json,bill_id)
        flash('You have successfully added a new bill.')

        return json.dumps({'redirect':url_for('admin.view_bill',id=bill_id)}), 200, {'ContentType':'application/json'} 
    
    add_bill = True
    items = Item.query.all()
    customers = Customer.query.all()

    billnumber = db.session.query(Bill).order_by(Bill.bill_number.desc()).first()
    if billnumber:
        bill_number = billnumber.bill_number + 1
    else:
        bill_number = 1
    return render_template('admin/bills/bill.html', action="Add",
                           add_bill=add_bill,bill_number=bill_number,items=items,customers=customers,title="Add Bill")


@admin.route('/bills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bill(id):
    """
    View a bill
    """
    check_admin()
    if request.method == 'POST':
        bill = Bill.query.get_or_404(id)
        updateBill(request.json,bill)
        BillItem.query.filter(BillItem.bill_id==id).delete()
        insertBillItems(request.json,id)
        flash('You have successfully edited a bill.')
        return json.dumps({'redirect':url_for('admin.view_bill',id=id)}), 200, {'ContentType':'application/json'} 
    edit_bill = True
    items = Item.query.all()
    customers = Customer.query.all()
    bill = Bill.query.get_or_404(id)
    bill_items = db.session.query(BillItem,Item).filter(BillItem.bill_id==id).join(Item).all()
    
    return render_template('admin/bills/bill.html', action="Edit",
                           edit_bill=True,bill_number=bill.bill_number,items=items,customers=customers,bill=bill,bill_items=bill_items, title="Edit Bill")

@admin.route('/bills/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_bill(id):
    """
    Delete a bill from the database
    """
    return
    check_admin()

    bill = Bill.query.get_or_404(id)
    db.session.delete(bill)
    db.session.commit()
    flash('You have successfully deleted the bill.')

    # redirect to the bills page
    return redirect(url_for('admin.list_bills'))

    return render_template(title="Delete Bill")

@admin.route('/bills/<int:id>', methods=['GET'])
@login_required
def view_bill(id):
    """
    View a bill
    """
    check_admin()


    bill = Bill.query.get_or_404(id)
    bill_items = db.session.query(BillItem,Item).filter(BillItem.bill_id==id).join(Item).all()
    
    return render_template('admin/bills/view_bill.html', action="View",
                           bill=bill,bill_items=bill_items, title="View Bill")


