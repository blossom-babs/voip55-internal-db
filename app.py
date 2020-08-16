import re
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import logout_user, login_required, login_user, LoginManager, current_user
from models import *
from bson import ObjectId
from datetime import datetime, date
import pymongo

# from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
# The above is used for confirm mail and isn't used anymore

import settings

# importing the settings file. this has the links to the mongodb url, everything

app = Flask(__name__)

import models
def do_backup(collection_name, doc_id):
    """

    :param collection_name:
    :type collection_name:
    :param doc_id:
    :type doc_id:
    :return:
    :rtype:
    """
    collection = getattr(models, collection_name.title(), None)  # pulls out the main collection
    if not collection:
        return
    backup = pymongo.MongoClient(settings.mongodb_url)  # connects to the db using pymongo
    backup_db = backup[settings.mongodb_name]
    backup_db_collection = backup_db["{}_backup".format(collection_name.lower())]
    document = collection.objects.raw({"_id": ObjectId(doc_id)})
    if document.count() < 1:
        return
    document = document.first()
    document_data = document.to_son().to_dict()
    document_data.pop('_cls', None)
    check_backup = backup_db_collection.find_one({"_id": ObjectId(doc_id)})
    if check_backup:
        backup_db_collection.update_one({"_id": ObjectId(doc_id)}, {"$set": document_data})
        return
    document_data.update(_cls = 'models.{}Backup'.format(collection_name.title()))
    backup_db_collection.insert_one(document_data)
    return ""

s = URLSafeTimedSerializer(settings.secret_key)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# THE LOGIN DETAILS ABOVE AFFECT THE /LOGIN


@login_manager.user_loader
def load_user(staff_id):
    print(staff_id, "---------")
    staff = Staff.objects.raw({"_id": ObjectId(staff_id)})
    if staff.count() < 1:
        print("ddddd")
    staff = staff.first()
    return staff


app.secret_key = settings.secret_key

@app.route("/")
def index():
    logout_user()
    return render_template("index.html")
    # return render_template("login.html")


@app.route("/admin")
@login_required
def admin():
    if not current_user.admin:
        return redirect(url_for('dashboard'))

    staff_body = list(Staff.objects.raw({"confirm_user": False, "approval_status": "pending"}))
    all_staff = list(Staff.objects.raw({"confirm_user": True, "admin": False}))
    start = datetime.now().replace(hour=0, minute=0)
    end = start.replace(hour=23, minute=29)
    daily_report = list(Reports.objects.raw({"currentDate": {"$gte": start, "$lte": end}}))
    print(staff_body)

    print(start)
    print(end)

    return render_template("admin.html", full_name=current_user.full_name.split()[0],
                           staff_body=staff_body, all_staff=all_staff, daily_report=daily_report)


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/failure")
def failure():
    return render_template("failure.html")


@app.route("/suppliers", methods=["GET", "POST"])
@login_required
def suppliers():
    if request.method == "POST":
        data = request.json
        print(data)
        supply_info = data.get("supply_info", [])

        suppliers = Suppliers(supplierName=data.get('supplierName'), supplierAddress=data.get('supplierAddress'),
        supplierContacts=data.get('supplierContacts'), supplierEmail=data.get('supplierEmail'), staff_created=current_user.full_name)
        
        suppliers.supply_info = supply_info
        print(suppliers)
        suppliers.save()
        do_backup('Suppliers', doc_id = suppliers.pk)
        
        return dict()
    return render_template("suppliers.html")


@app.route("/signupandlogin")
def authorization():
    return render_template("signupandlogin.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        print(request.form)
        form = request.form

        full_name = form["full_name"]
        email = form["email"]
        job_position = form["job_position"]
        password = form["password"]

        staff = Staff.objects.raw({"email": email})
        if staff.count() == 1:
            flash("Staff already exists.")
            return redirect(url_for('signup'))

        new_staff = Staff(full_name=full_name, job_position=job_position, email=email, password=password)
        new_staff = new_staff.save()

        return redirect(url_for('success'))
    return render_template("signupandlogin.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form = request.form

        email = form["email"]
        password = form["password"]

        staff = Staff.objects.raw({"email": email, "password": password})

        if staff.count() == 0:
            flash("Invalid email or password")
            return redirect(url_for('login'))
        print(staff.first().pk)

        login_user(staff.first())

        if staff.first().admin is True:
            return redirect(url_for('admin'))

        if staff.first().confirm_user is False:
            return redirect(url_for('failure'))

        if staff.first().confirm_user is True:
            return redirect(url_for('dashboard'))

    return render_template("signupandlogin.html")


@app.route("/dashboard")
@login_required
def dashboard():
    print(current_user)
    if current_user.admin is True:
        return redirect(url_for('admin'))

    tasks_data = list(Tasks.objects.raw({"staff__": str(current_user.pk)}))

    return render_template("dashboard.html", full_name=current_user.full_name.split()[0], tasks_data=tasks_data)


@app.route("/reports", methods=["POST", "GET"])
@login_required
def reports():
    if request.method == "POST":
        data = request.json
        print(data)
        daily_reports = Reports(reportsTitle=data.get("reportsTitle"),
                                reportsMessage=data.get("reportsMessage"))
        daily_reports = daily_reports.save()
        return dict()

    return render_template("dashboard.html")


@app.route("/tasks", methods=["POST", "GET"])
@login_required
def tasks():
    if request.method == "POST":
        data = request.json
        print(data)
        tasks_data = Tasks(staff__=data.get("staff__"), tasks=data.get("tasks"),
                           tasksMessage=data.get("tasksMessage"))
        tasks_data.save()
        return dict()

    return render_template("admin.html")


@app.route("/addclient", methods=["POST", "GET"])
@login_required
def addclient():
    print(request.json)
    if request.method == "POST":
        data = request.json
        print(data)
        service_provided = data.get("service_provided", [])
        passwords = data.get("passwords", [])
        helpdesk_service = data.get("helpdesk_service", [])
        office_devices = data.get("office_devices", [])
        new_client = Clients(client_name=data.get("client_name"), address=data.get("address"),
                             email=data.get("email"), customer_ref=data.get("customer_ref"),
                             telephone_num1=data.get("telephone_num1"), telephone_num2=data.get("telephone_num3"),
                             telephone_num3=data.get("telephone_num3"), business_name=data.get("business_name"), 
                             staff_created=current_user.full_name
                             )
      
        new_client.services = service_provided
        new_client.passwords = passwords
        new_client.helpdesk = helpdesk_service
        new_client.officeDevices = office_devices
        new_client = new_client.save()
        do_backup('Clients', doc_id = new_client.pk)
     
        return dict()
    return render_template("addclient.html")


@app.route("/clients")
@login_required
def clients():
    
    people = list(Clients.objects.raw({"isDeleted":False}))
    # print(people)
    return render_template("clients.html", people=people)


@app.route("/existingSuppliers")
@login_required
def existingSuppliers():
    existing_suppliers_information = list(Suppliers.objects.raw({"isDeleted":False}))
    # print(existing_suppliers_information)
    return render_template("existingsuppliers.html", existing_suppliers_information=existing_suppliers_information)


@app.route("/client/<pk>")
def client(pk):
    if ObjectId.is_valid(pk) is False:
        return "Invalid User Id"
    # print(request.json)
    person = Clients.objects.get({"_id": ObjectId(pk)})
    return render_template("client.html", client_name=person.client_name, address=person.address,
                           email=person.email, customer_ref=person.customer_ref, telephone_num1=person.telephone_num1,
                           telephone_num2=person.telephone_num2, telephone_num3=person.telephone_num3,
                           business_name=person.business_name, officeDevices=person.officeDevices,
                           services=person.services, passwords=person.passwords, helpdesk=person.helpdesk, client_id=pk)


@app.route("/existingsupplier/<pk>")
@login_required
def existingsupplier(pk):
    if ObjectId.is_valid(pk) is False:
        return "Invalid User Id"
    # print(request.json)
    supplier = Suppliers.objects.get({"_id": ObjectId(pk)})
    # existing_suppliers_information = list(Suppliers.objects.all())
    return render_template("existingsupplier.html", supplierName=supplier.supplierName,
                            supplierAddress=supplier.supplierAddress, supplierContacts= supplier.supplierContacts,
                            supplierEmail=supplier.supplierEmail, supply_info=supplier.supply_info, supplier_id=pk
                            )


@app.route("/search", methods=["POST"])
def search():
    print(request.form.get)
    form = request.form
    search_value = form['search']
    search_value = re.escape(search_value)
    params = {"$or": [
        {"client_name": re.compile(search_value, re.IGNORECASE)},
        {"email": re.compile(search_value, re.IGNORECASE)},
        {"customer_ref": re.compile(search_value, re.IGNORECASE)},
        {"address": re.compile(search_value, re.IGNORECASE)},
        {"business_name": re.compile(search_value, re.IGNORECASE)}
    ]}
    people = list(Clients.objects.raw(params).all())
    return render_template("clients.html", people=people)


@app.route("/suppliersearch", methods=["POST"])
@login_required
def suppliersearch():
    # print(request.form.get)
    form = request.form
    # print(form)
    search = form['search_supplier']
    # print((search))
    search = re.escape(search)
    # print(search)
    params = {"$or": [{"supplier_info.supplierName": re.compile(search, re.IGNORECASE)},
                      {"supplier_info.supplierEmail": re.compile(search, re.IGNORECASE)},
                      {"supplier_info.supplierAddress": re.compile(search, re.IGNORECASE)}
                      ]}

    # print(params)
    supplier = list(Suppliers.objects.raw(params).all())
    # print(supplier)
    return render_template("existingsuppliers.html", existing_suppliers_information=supplier)


@app.route("/edit/<pk>", methods=["POST"])
@login_required
def edit(pk):
    print(request.json)
    if request.method == "POST":
        data = request.json
        # print(data)
        service_provided = data.get("service_provided", [])
        passwords = data.get("passwords", [])
        helpdesk_service = data.get("helpdesk_service", [])
        office_devices = data.get("office_devices", [])
        update_data = dict(client_name=data.get("client_name"), address=data.get("address"),
                           email=data.get("email"), customer_ref=data.get("customer_ref"),
                           telephone_num1=data.get("telephone_num1"), telephone_num2=data.get("telephone_num3"),
                           telephone_num3=data.get("telephone_num3"), business_name=data.get("business_name")
                           )
        Clients.objects.raw({"_id": ObjectId(pk)}).update({"$set": update_data}, upsert=False)
        
    
        
        clientele = Clients.objects.get({"_id": ObjectId(pk)})
        clientele.services = service_provided
        clientele.passwords = passwords
        clientele.helpdesk = helpdesk_service
        clientele.officeDevices = office_devices
        clientele = clientele.save()
        do_backup(collection_name = 'Clients', doc_id= clientele.pk)
        return dict()
        # print(pk)

    return redirect(url_for("clients.html", pk=pk))


    # to edit normally, we did this: {'the criteria we will be editing' {"id_": "pk"}, 'followed by the information we will be editing' {$set: {"name":"Babalola"}}}


@app.route("/editsupplier/<pk>", methods=["POST"])
def editsupplier(pk):
    print(request.json)
    if request.method == "POST":
        data = request.json
        supply_info = data.get("supply_info", [])

        suppliers_data= dict(supplierName=data.get('supplierName'), supplierAddress=data.get('supplierAddress'),
                            supplierContacts=data.get('supplierContacts'), supplierEmail=data.get('supplierEmail'))
        Suppliers.objects.raw({"_id": ObjectId(pk)}).update({"$set": suppliers_data}, upsert=False)
        update_supplier = Suppliers.objects.get({"_id": ObjectId(pk)})
        update_supplier.supply_info = supply_info
        print(update_supplier)
        update_supplier = update_supplier.save()
        do_backup(collection_name ='Suppliers', doc_id= update_supplier.pk)
        return dict()
    return redirect(url_for("existingsupplier.html", pk=pk))


@app.route("/approvals", methods=["POST"])
@login_required
def approvals():
    dataset = request.json
    action = dataset.get("action")
    value = dataset.get("staff_id")

    if not action or not value:
        return
    if ObjectId.is_valid(value) is False:
        return "not valid"
    staff = Staff.objects.get({"_id": ObjectId(value)})

    if action == "reject":
        staff.approval_status = "rejected"
    if action == "confirm":
        staff.approval_status = "confirmed"
        staff.confirm_user = True

    staff.save()
    return dict()


@app.route("/restoreClient", methods=["POST"])
@login_required
def restoreClient():
    data = request.json
    action = data.get("action")
    value = data.get("value")

    if not action or not value:
        return
    if ObjectId.is_valid(value) is False:
        return "not valid"

    client = Clients.objects.get({"_id":ObjectId(value)})

    if action == "restore":
        client.isDeleted = False

    client.save()
    return dict()


@app.route("/restoreSupplier", methods=["POST"])
@login_required
def restoreSupplier():
    data = request.json
    action = data.get("action")
    value = data.get("value")

    if not action or not value:
        return
    if ObjectId.is_valid(value) is False:
        return "not valid"

    supplier = Suppliers.objects.get({"_id":ObjectId(value)})

    if action == "restore":
        supplier.isDeleted = False

    supplier.save()
    return dict()


@app.route("/deletedClient", methods=["POST"])
@login_required
def deletedClient():
    data = request.json
    action = data.get("action")
    value= data.get("clients_id")

    if not action or not value:
            return
    if ObjectId.is_valid(value) is False:
        return "not valid"
    client = Clients.objects.get({"_id": ObjectId(value)})

    if action == "delete":
        client.isDeleted = True

    client.save()
    return dict()


@app.route("/deletedSupplier", methods=["POST"])
@login_required
def deletedSupplier():
    data = request.json
    action = data.get('action')
    value = data.get('supplier_id')
    if not action or not value:
            return
    if ObjectId.is_valid(value) is False:
        return "not valid"
    supplier = Suppliers.objects.get({"_id": ObjectId(value)})

    if action == "delete":
        supplier.isDeleted = True

    supplier.save()
    return dict()


@app.route("/hideClients", methods=["POST"])
@login_required
def hideClients():
    data = request.json
    action = data.get('action')
    value = data.get('value')
    if not action or not value:
            return
    if ObjectId.is_valid(value) is False:
        return "not valid"
    client = Clients.objects.get({"_id": ObjectId(value)})

    if action == "hide":
        client.display = False

    client.save()
    return dict()


@app.route("/hideSuppliers", methods=["POST"])
@login_required
def hideSuppliers():
    data = request.json
    action = data.get('action')
    value = data.get('value')
    if not action or not value:
            return
    if ObjectId.is_valid(value) is False:
        return "not valid"
    supplier = Suppliers.objects.get({"_id": ObjectId(value)})

    if action == "hide_supplier":
        supplier.display = False

    supplier.save()
    return dict()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("signupandlogin.html")


@app.route("/trash")
@login_required
def trash():
    people = list(Clients.objects.raw({"isDeleted":True, 'display':True}))
    suppliers  = list(Suppliers.objects.raw({"isDeleted":True, 'display':True}))
    return render_template('trash.html', people=people, suppliers=suppliers)

if __name__ == "__main__":
    app.run(debug=True, port=7000)
