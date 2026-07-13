from flask import Flask, render_template, request, redirect, url_for, session
from mydatabase import get_project, get_projects,get_suppliers,get_supplier ,create_project,update_project,delete_project,create_supplier,update_supplier,delete_supplier,login_user,get_materials,get_purchase_order,create_purchase_order,update_purchase_order,delete_purchase_order, get_material_request, get_material_requests, create_material_request, update_material_request, delete_material_request,create_request_item,get_request_item,get_request_items,update_request_item,delete_request_item,create_payment,get_payment,get_payments,update_payment,delete_payment,get_users,get_user,create_user,update_user,delete_user,get_roles,get_role,create_role,update_role,delete_role,get_inventory_transactions,create_stock_in,get_stock_in,create_stock_out,get_low_stock,get_recent_activity,approve_payment,reject_payment,update_payment_status,total_payments,pending_payments,approved_payments,rejected_payments,get_pending_purchase_orders,get_purchase_order_balance,get_purchase_order_details,get_purchase_orders
from datetime import datetime,date

today=date.today()

app = Flask(__name__)
app.secret_key = "buildtrack123"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def projects():

    # User must be logged in
    if "user" not in session:
        return redirect("/login")

    # Only Administrators can access Projects
    if session["role"] != "Administrator":
        return "Access Denied! Only Administrators can view Projects.", 403
    projects = get_projects()
    return render_template(
        "projects.html",
        active_page="projects",
        projects=projects
    )

@app.route("/suppliers")
def suppliers():
    suppliers = get_suppliers()
    return render_template(
        "suppliers.html",
        active_page="suppliers",
        suppliers=suppliers
    )

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    projects = get_projects()
    suppliers = get_suppliers()
    materials = get_materials()
    low_stock = get_low_stock()
    requests = get_material_requests()
    payments = get_payments()
    activities = get_recent_activity()
    inventory = get_inventory_transactions()
    pending_requests = [
        r for r in requests
        if r[4] == "Pending"
    ]
    return render_template(
        "dashboard.html",
        active_page="dashboard",
        total_projects=len(projects),
        total_suppliers=len(suppliers),
        total_materials=len(materials),
        total_requests=len(requests),
        total_payments=len(payments),
        activities=activities,
        low_stock=low_stock,
        projects=projects[:5],
        requests=pending_requests[:5],
        inventory=inventory[:5]
    )

@app.route("/materials")
def materials():
    materials = get_materials()
    return render_template(
        "materials.html",
        active_page="materials",
        materials=materials
    )

@app.route("/material_requests")
def material_requests():
    requests = get_material_requests()
    return render_template(
        "material_requests.html",
        material_requests=requests,
        active_page="material_requests"
    )

@app.route("/inventory")
def inventory():
    if "user" not in session:
        return redirect("/login")
    if session["role"] not in [
        "Administrator",
        "Procurement Officer",
        "Store Keeper"
    ]:
        return "Access Denied",403
    transactions = get_inventory_transactions()
    return render_template(
        "inventory.html",
        transactions=transactions,
        active_page="inventory"
    )

@app.route("/stock_in", methods=["GET","POST"])
def stock_in():
    if "user" not in session:
        return redirect("/loin")
    if session["role"] not in [
        "Administrator",
        "Store Keeper"
    ]:
        return "Access Denied",403
    if request.method=="POST":
        create_stock_in(
            request.form["supplier_id"],
            request.form["material_id"],
            request.form["quantity"],
            request.form["reference"],
            session["user_id"]
        )
    
        return redirect("/inventory")
    materials=get_materials()
    return render_template(
        "stock_in.html",
        materials=materials,
        active_page="inventory"
    )

@app.route("/stock_out", methods=["GET","POST"])
def stock_out():
    if "user" not in session:
        return redirect("/login")
    if session["role"] not in [
        "Administrator",
        "Store Keeper"
    ]:
        return "Access Denied",403
    if request.method=="POST":
        create_stock_out(
            request.form["material_id"],
            request.form["quantity"],
            request.form["project_id"],
            session["user_id"]
        )
        return redirect("/inventory")
    materials=get_materials()
    projects=get_projects()
    return render_template(
        "stock_out.html",
        materials=materials,
        projects=projects,
        active_page="inventory"
    )

@app.route("/add_material_request", methods=["GET", "POST"])
def add_material_request():

    if request.method == "POST":
        create_material_request(
            request.form["project_id"],
            session["user_id"],
            date.today()
        )
        return redirect("/material_requests")
    projects = get_projects()
    return render_template(
        "add_material_request.html",
        projects=projects,
        active_page="material_requests"
    )

@app.route("/purchase_orders")
def purchase_orders():
    if "user" not in session:
        return redirect("/login")
    purchase_orders = get_purchase_orders()
    return render_template(
        "purchase_orders.html",
        active_page="purchase_orders",
        purchase_orders=purchase_orders
    )

@app.route("/add_purchase_order", methods=["GET", "POST"])
def add_purchase_order():
    if request.method == "POST":
        create_purchase_order(
            request.form["supplier_id"],
            request.form["order_date"],
            request.form["total_amount"]
        )
        return redirect(url_for("purchase_orders"))
    suppliers = get_suppliers()
    return render_template(
        "add_purchase_order.html",
        suppliers=suppliers,
        active_page="purchase_orders"
    )

@app.route("/edit_purchase_order/<int:purchase_order_id>", methods=["GET", "POST"])
def edit_purchase_order(purchase_order_id):
    if request.method == "POST":
        update_purchase_order(
            purchase_order_id,
            request.form["supplier_id"],
            request.form["order_date"],
            request.form["total_amount"]
        )
        return redirect(url_for("purchase_orders"))
    purchase_order = get_purchase_order(purchase_order_id)
    suppliers = get_suppliers()
    return render_template(
        "edit_purchase_order.html",
        purchase_order=purchase_order,
        suppliers=suppliers,
        active_page="purchase_orders"
    )

@app.route("/delete_purchase_order/<int:purchase_order_id>")
def remove_purchase_order(purchase_order_id):
    delete_purchase_order(purchase_order_id)
    return redirect(url_for("purchase_orders"))


@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    if "user" not in session:
        return redirect("/login")

    if session["role"] != "Administrator":
        return "Access Denied",403

    if request.method == "POST":
        create_project(
            request.form["project_name"],
            request.form["location"],
            request.form["budget"]
        )
        return redirect(url_for("projects"))
    return render_template(
        "add_project.html",
        active_page="projects"
    )

@app.route("/edit_project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    if request.method == "POST":
        update_project(
            project_id,
            request.form["budget"]
        )
        return redirect("/projects")
    project = get_project(project_id)
    return render_template(
        "edit_project.html",
        project=project,
        active_page="projects"
    )

@app.route("/delete_project/<int:project_id>")
def remove_project(project_id):
    delete_project(project_id)
    return redirect("/projects")

@app.route("/add_supplier", methods=["GET","POST"])
def add_supplier():
    if request.method == "POST":
        create_supplier(
            request.form["supplier_name"],
            request.form["phone"],
            request.form["email"]
        )
        return redirect(url_for("suppliers"))
    return render_template(
        "add_supplier.html",
        active_page="suppliers"
    )

@app.route("/edit_supplier/<int:supplier_id>", methods=["GET","POST"])
def edit_supplier(supplier_id):
    if request.method == "POST":
        update_supplier(
            supplier_id,
            request.form["supplier_name"],
            request.form["phone"],
            request.form["email"]
        )
        return redirect(url_for("suppliers"))
    supplier = get_supplier(supplier_id)
    return render_template(
        "edit_supplier.html",
        supplier=supplier,
        active_page="suppliers"
    )

@app.route("/delete_supplier/<int:supplier_id>")
def remove_supplier(supplier_id):
    delete_supplier(supplier_id)
    return redirect(url_for("suppliers"))

@app.route("/users")
def users():
    if "user" not in session:
        return redirect("/login")
    if session["role"] != "Administrator":
        return "Access Denied", 403
    users = get_users()
    return render_template(
        "users.html",
        users=users,
        active_page="users"
    )

@app.route("/add_user", methods=["GET","POST"])
def add_user():
    if request.method == "POST":
        create_user(
            request.form["username"],
            request.form["email"],
            request.form["password"],
            request.form["role"]
        )
        return redirect("/users")
    roles = get_roles()
    return render_template(
        "add_user.html",
        roles=roles,
        active_page="users"
    )

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if request.method == "POST":
        update_user(
            user_id,
            request.form["username"],
            request.form["email"],
            request.form["role"]
        )
        return redirect("/users")
    user = get_user(user_id)
    return render_template(
        "edit_user.html",
        user=user,
        active_page="users"
    )

@app.route("/delete_user/<int:user_id>")
def delete_user_route(user_id):
    delete_user(user_id)
    return redirect("/users")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = login_user(username, password)
        if user:
            session["user_id"] = user[0]      # User ID
            session["user"] = user[1]         # Username
            session["role"] = user[4]  #role
            return redirect("/dashboard")
        return render_template(
            "login.html",
            error="Invalid username or password"
        )
    return  render_template("login.html")



@app.route("/request_items")
def request_items():
    if "user" not in session:
        return redirect("/login")
    items = get_request_items()
    return render_template(
        "request_items.html",
        request_items=items,
        active_page="request_items"
    )

@app.route("/add_request_item", methods=["GET", "POST"])
def add_request_item():
    if request.method == "POST":
        create_request_item(
            request.form["request_id"],
            request.form["material_id"],
            request.form["quantity"]
        )
        return redirect("/request_items")
    requests = get_material_requests()
    materials = get_materials()
    return render_template(
        "add_request_item.html",
        requests=requests,
        materials=materials,
        active_page="request_items"
    )

@app.route("/edit_request_item/<int:request_item_id>", methods=["GET", "POST"])
def edit_request_item(request_item_id):
    if request.method == "POST":
        update_request_item(
            request_item_id,
            request.form["material_id"],
            request.form["quantity"]
        )
        return redirect("/request_items")
    item = get_request_item(request_item_id)
    materials = get_materials()
    return render_template(
        "edit_request_item.html",
        item=item,
        materials=materials,
        active_page="request_items"
    )

@app.route("/delete_request_item/<int:request_item_id>")
def delete_request_item_route(request_item_id):
    delete_request_item(request_item_id)
    return redirect("/request_items")

@app.route("/payments")
def payments():
    if "user" not in session:
        return redirect("/login")

    return render_template(
        "payments.html",
        payments=get_payments(),
        pending_orders=get_pending_purchase_orders(),
        total_payments=total_payments(),
        pending_payments=pending_payments(),
        approved_payments=approved_payments(),
        rejected_payments=rejected_payments(),
        active_page="payments"
    )


@app.route("/add_payment/<int:purchase_order_id>", methods=["GET", "POST"])
def add_payment(purchase_order_id):
    if "user" not in session:
        return redirect("/login")
    details = get_purchase_order_details(purchase_order_id)
    if details is None:
        return "Purchase Order not found.", 404
    supplier = details[1]
    total_amount = details[2]
    balance = details[3]
    if request.method == "POST":
        payment_date = datetime.strptime(
            request.form["payment_date"],
            "%Y-%m-%d"
        ).date()
        if payment_date > date.today():
            return render_template(
                "add_payment.html",
                purchase_order_id=purchase_order_id,
                supplier=supplier,
                total_amount=total_amount,
                balance=balance,
                today=date.today(),
                error="Future payment dates are not allowed.",
                active_page="payments"
            )
        amount = float(request.form["amount"])
        if amount > balance:
            return render_template(
                "add_payment.html",
                purchase_order_id=purchase_order_id,
                supplier=supplier,
                total_amount=total_amount,
                balance=balance,
                today=date.today(),
                error="Payment cannot exceed remaining balance.",
                active_page="payments"
            )
        payment_id = create_payment(
            purchase_order_id,
            payment_date,
            amount,
            request.form["payment_method"],
            "Pending"
        )
        approve_payment(payment_id)
        return redirect("/payments")
    return render_template(
        "add_payment.html",
        purchase_order_id=purchase_order_id,
        supplier=supplier,
        total_amount=total_amount,
        balance=balance,
        today=date.today(),
        active_page="payments"
    )

@app.route("/edit_payment/<int:payment_id>", methods=["GET", "POST"])
def edit_payment(payment_id):
    if "user" not in session:
        return redirect("/login")
    payment = get_payment(payment_id)
    if request.method == "POST":
        update_payment(
            payment_id,
            request.form["payment_date"],
            request.form["amount"],
            request.form["payment_method"]
        )
        return redirect("/payments")
    return render_template(
        "edit_payment.html",
        payment=payment,
        active_page="payments"
    )

@app.route("/delete_payment/<int:payment_id>")
def delete_payment_route(payment_id):
    if "user" not in session:
        return redirect("/login")
    delete_payment(payment_id)
    return redirect("/payments")

@app.route("/approve_payment/<int:payment_id>")
def approve_payment_route(payment_id):
    if "user" not in session:
        return redirect("/login")
    approve_payment(payment_id)
    return redirect("/payments")

@app.route("/reject_payment/<int:payment_id>")
def reject_payment_route(payment_id):
    if "user" not in session:
        return redirect("/login")
    reject_payment(payment_id)
    return redirect("/payments")


@app.route("/roles")
def roles():
    if "user" not in session:
        return redirect("/login")
    if session["role"] != "Administrator":
        return "Access Denied",403
    roles = get_roles()
    return render_template(
        "roles.html",
        roles=roles,
        active_page="roles"
    )

@app.route("/add_role", methods=["GET","POST"])
def add_role():
    if request.method=="POST":
        create_role(
            request.form["role_name"],
            request.form["description"]
        )
        return redirect("/roles")
    return render_template(
        "add_role.html",
        active_page="roles"
    )

@app.route("/edit_role/<int:role_id>", methods=["GET","POST"])
def edit_role(role_id):
    if request.method=="POST":
        update_role(
            role_id,
            request.form["role_name"],
            request.form["description"]
        )
        return redirect("/roles")
    role=get_role(role_id)
    return render_template(
        "edit_role.html",
        role=role,
        active_page="roles"
    )

@app.route("/delete_role/<int:role_id>")
def remove_role(role_id):
    delete_role(role_id)
    return redirect("/roles")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
if __name__ == "__main__":
    app.run(debug=True)