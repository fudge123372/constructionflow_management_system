from flask import Flask, render_template, request, redirect, url_for, session
from mydatabase import get_projects, get_suppliers, get_materials , create_project , update_project , delete_project , create_supplier , update_supplier , delete_supplier , login_user

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

    return render_template(
        "dashboard.html",
        active_page="dashboard",
        total_projects=len(projects),
        total_suppliers=len(suppliers),
        projects=projects
    )

@app.route("/materials")
def materials():
    materials = get_materials()
    return render_template(
        "materials.html",
        active_page="materials",
        materials=materials
    )

@app.route("/add_project", methods=["GET", "POST"])
def add_project():
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
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = login_user(username, password)
        if user:
            session["user"] = user[1]   # username
            session["role"] = user[4]   # role
            return redirect("/dashboard")
        return render_template(
            "login.html",
            error="Invalid username or password"
        )
    return render_template("login.html")
    return render_template(
        "login.html",
        error=None
    )




if __name__ == "__main__":
    app.run(debug=True)