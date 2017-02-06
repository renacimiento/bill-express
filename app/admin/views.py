# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import CustomerForm, ItemForm
from .. import db
from ..models import Customer, Item

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
    # form = CustomerForm(obj=customer)
    # form.name.data = customer.name 
    # form.TIN.data = customer.TIN 
    # form.phone_number.data = customer.phone_number 
    # form.address.data = customer.address 
    
    return render_template('admin/customers/view_customer.html', action="View",
                           customer=customer, title="View Customer")


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
        print "ITEM PRICE"
        print form.price.data
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


