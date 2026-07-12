import psycopg2
from datetime import date

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='1234',
    dbname='construction_management_system'
)

# CREATE
def create_project(project_name, location, budget):
    cur = conn.cursor()
    sql = """
    INSERT INTO projects
    (project_name, location, budget)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (project_name, location, budget))
    conn.commit()
    cur.close()
    print("Project added successfully")


# READ
def get_projects():
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM projects
        ORDER BY project_id
    """)
    projects = cur.fetchall()
    cur.close()
    return projects


# UPDATE
def update_project(project_id, budget):
    cur = conn.cursor()
    cur.execute("""
        UPDATE projects
        SET budget = %s
        WHERE project_id = %s
    """, (budget, project_id))

    conn.commit()
    cur.close()
    print("Project updated")


# DELETE
def delete_project(project_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM projects
        WHERE project_id = %s
    """, (project_id,))
    conn.commit()
    cur.close()
    print("Project deleted")

    
# CREATE
def create_supplier(supplier_name, phone, email):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO suppliers
        (supplier_name, phone, email)
        VALUES (%s, %s, %s)
    """, (supplier_name, phone, email))
    conn.commit()
    cur.close()


# READ
def get_suppliers():
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return suppliers


def delete_supplier(supplier_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM suppliers
        WHERE supplier_id=%s
    """, (supplier_id,))
    conn.commit()
    cur.close()

def create_material(material_name, category, unit, quantity, unit_price):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO materials
        (material_name, category, unit, quantity, unit_price)
        VALUES (%s,%s,%s,%s,%s)
    """,(material_name, category, unit, quantity, unit_price))
    conn.commit()
    cur.close()

def get_materials():
    cur = conn.cursor()
    cur.execute("SELECT * FROM materials")
    materials = cur.fetchall()
    cur.close()
    return materials

def update_material(material_id, quantity):
    cur = conn.cursor()
    cur.execute("""
        UPDATE materials
        SET quantity=%s
        WHERE material_id=%s
    """,(quantity, material_id))
    conn.commit()
    cur.close()

def delete_material(material_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM materials
        WHERE material_id=%s
    """,(material_id,))
    conn.commit()
    cur.close()

def get_project(project_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM projects
        WHERE project_id=%s
    """, (project_id,))
    project = cur.fetchone()
    cur.close()
    return project


def get_supplier(supplier_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM suppliers
        WHERE supplier_id=%s
    """, (supplier_id,))
    supplier = cur.fetchone()
    cur.close()
    return supplier

def update_supplier(supplier_id, supplier_name, phone, email):
    cur = conn.cursor()
    cur.execute("""
        UPDATE suppliers
        SET supplier_name=%s,
            phone=%s,
            email=%s
        WHERE supplier_id=%s
    """,(supplier_name, phone, email, supplier_id))
    conn.commit()
    cur.close()

def login_user(username, password):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM users
        WHERE username=%s
        AND password=%s
    """, (username, password))
    user = cur.fetchone()
    cur.close()
    return user

def get_users():
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, username, email, role
        FROM users
        ORDER BY user_id
    """)
    users = cur.fetchall()
    cur.close()
    return users

def get_user(user_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM users
        WHERE user_id=%s
    """, (user_id,))
    user = cur.fetchone()
    cur.close()
    return user

def create_user(username, email, password, role):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users
        (username,email,password,role)
        VALUES(%s,%s,%s,%s)
    """,(username,email,password,role))
    conn.commit()
    cur.close()

def update_user(user_id, username, email, role):
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET username=%s,
            email=%s,
            role=%s
        WHERE user_id=%s
    """,(username,email,role,user_id))
    conn.commit()
    cur.close()

def delete_user(user_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM users
        WHERE user_id=%s
    """,(user_id,))
    conn.commit()
    cur.close()

def create_role(role_name, description):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO roles
        (role_name, description)
        VALUES (%s, %s)
    """, (role_name, description))
    conn.commit()
    cur.close()

def get_roles():
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM roles
        ORDER BY role_id
    """)
    roles = cur.fetchall()
    cur.close()
    return roles

def get_role(role_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM roles
        WHERE role_id=%s
    """, (role_id,))
    role = cur.fetchone()
    cur.close()
    return role

def update_role(role_id, role_name, description):
    cur = conn.cursor()
    cur.execute("""
        UPDATE roles
        SET role_name=%s,
            description=%s
        WHERE role_id=%s
    """,(role_name, description, role_id))
    conn.commit()
    cur.close()

def delete_role(role_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM roles
        WHERE role_id=%s
    """,(role_id,))
    conn.commit()
    cur.close()

def create_purchase_order(supplier_id, order_date, total_amount):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO purchase_orders
        (supplier_id, order_date, total_amount)
        VALUES (%s, %s, %s)
    """, (supplier_id, order_date, total_amount))
    conn.commit()
    cur.close()

def get_pending_purchase_orders():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            purchase_order_id,
            supplier_name,
            total_amount
        FROM purchase_orders
        JOIN suppliers
            ON purchase_orders.supplier_id = suppliers.supplier_id
        WHERE payment_status = 'Pending'
    """)
    data = cur.fetchall()
    cur.close()
    return data

def get_purchase_order_details(purchase_order_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT
            suppliers.supplier_name,
            purchase_orders.total_amount,
            purchase_orders.balance
        FROM purchase_orders
        JOIN suppliers
            ON purchase_orders.supplier_id = suppliers.supplier_id
        WHERE purchase_orders.purchase_order_id = %s
    """, (purchase_order_id,))
    details = cur.fetchone()
    cur.close()
    return details

def get_purchase_order(purchase_order_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM purchase_orders
        WHERE purchase_order_id=%s
    """, (purchase_order_id,))
    purchase_order = cur.fetchone()
    cur.close()
    return purchase_order

def update_purchase_order(purchase_order_id, supplier_id, order_date, total_amount):
    cur = conn.cursor()
    cur.execute("""
        UPDATE purchase_orders
        SET supplier_id=%s,
            order_date=%s,
            total_amount=%s
        WHERE purchase_order_id=%s
    """, (supplier_id, order_date, total_amount, purchase_order_id))
    conn.commit()
    cur.close()

def delete_purchase_order(purchase_order_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM purchase_orders
        WHERE purchase_order_id=%s
    """, (purchase_order_id,))
    conn.commit()
    cur.close()

def get_pending_purchase_orders():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            purchase_orders.purchase_order_id,
            supplier_name,
            total_amount
        FROM purchase_orders
        JOIN suppliers
        ON purchase_orders.supplier_id = suppliers.supplier_id
        WHERE purchase_orders.payment_status = 'Pending'
    """)
    data = cur.fetchall()
    cur.close()
    return data


def update_payment_status(payment_id, status):
    cur = conn.cursor()
    cur.execute("""
        UPDATE payments
        SET status=%s
        WHERE payment_id=%s
    """, (status, payment_id))
    conn.commit()
    cur.close()

def create_material_request(project_id, requested_by, request_date):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO material_requests
        (project_id, requested_by, request_date)
        VALUES (%s, %s, %s)
    """, (project_id, requested_by, request_date))
    conn.commit()
    cur.close()

def get_material_requests():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            material_requests.request_id,
            projects.project_name,
            users.username,
            material_requests.request_date,
            material_requests.status
        FROM material_requests
        JOIN projects
        ON material_requests.project_id = projects.project_id
        JOIN users
        ON material_requests.requested_by = users.user_id
        ORDER BY request_id
    """)
    requests = cur.fetchall()
    cur.close()
    return requests

def get_material_request(request_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM material_requests
        WHERE request_id=%s
    """, (request_id,))
    request = cur.fetchone()
    cur.close()
    return request

def update_material_request(request_id, status):
    cur = conn.cursor()
    cur.execute("""
        UPDATE material_requests
        SET status=%s
        WHERE request_id=%s
    """, (status, request_id))
    conn.commit()
    cur.close()

def delete_material_request(request_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM material_requests
        WHERE request_id=%s
    """, (request_id,))
    conn.commit()
    cur.close()

def get_inventory_transactions():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            stock_in.stock_in_id,
            materials.material_name,
            'IN' AS transaction_type,
            stock_in.quantity,
            stock_in.received_date,
            stock_in.reference
        FROM stock_in
        JOIN materials
        ON stock_in.material_id = materials.material_id

        UNION ALL
                
        SELECT
            stock_out.stock_out_id,
            materials.material_name,
            'OUT',
            stock_out.quantity,
            stock_out.issued_date,
            projects.project_name
        FROM stock_out
        JOIN materials
        ON stock_out.material_id = materials.material_id
        JOIN projects
        ON stock_out.project_id = projects.project_id

        ORDER BY 5 DESC;
    """)
    data = cur.fetchall()
    cur.close()
    return data

def create_stock_in(material_id, quantity, supplier_id, reference, received_by):
    cur = conn.cursor()
    # Save Stock In transaction
    cur.execute("""
        INSERT INTO stock_in
        (
            material_id,
            quantity,
            supplier_id,
            reference,
            received_date,
            received_by
        )
        VALUES
        (%s,%s,%s,%s,CURRENT_DATE,%s)
    """, (
        material_id,
        quantity,
        supplier_id,
        reference,
        received_by
    ))
    # Increase inventory quantity
    cur.execute("""
        UPDATE materials
        SET quantity = quantity + %s
        WHERE material_id = %s
    """, (
        quantity,
        material_id
    ))
    conn.commit()
    cur.close()

def get_stock_in():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            stock_in.stock_in_id,
            materials.material_name,
            stock_in.quantity,
            stock_in.reference,
            stock_in.received_date,
            users.username
        FROM stock_in
        JOIN materials
            ON stock_in.material_id = materials.material_id
        JOIN users
            ON stock_in.received_by = users.user_id
        ORDER BY stock_in.stock_in_id DESC
    """)
    stock = cur.fetchall()
    cur.close()
    return stock

def create_stock_out(material_id, quantity, project_id, issued_by):
    cur = conn.cursor()
    # Check available stock
    cur.execute("""
        SELECT quantity
        FROM materials
        WHERE material_id=%s
    """, (material_id,))
    current_stock = cur.fetchone()[0]
    quantity = int(quantity)
    if current_stock < quantity:
        cur.close()
        raise Exception("Not enough stock available.")
    # Save stock out
    cur.execute("""
        INSERT INTO stock_out
        (material_id, quantity, project_id, issued_date, issued_by)
        VALUES (%s,%s,%s,CURRENT_DATE,%s)
    """, (
        material_id,
        quantity,
        project_id,
        issued_by
    ))
    # Reduce stock
    cur.execute("""
        UPDATE materials
        SET quantity = quantity - %s
        WHERE material_id=%s
    """, (
        quantity,
        material_id
    ))
    conn.commit()
    cur.close()

def create_request_item(request_id, material_id, quantity):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO request_items
        (request_id, material_id, quantity)
        VALUES (%s, %s, %s)
    """, (request_id, material_id, quantity))
    conn.commit()
    cur.close()

def get_request_items():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            ri.request_item_id,
            mr.request_id,
            m.material_name,
            ri.quantity
        FROM request_items ri
        JOIN material_requests mr
            ON ri.request_id = mr.request_id
        JOIN materials m
            ON ri.material_id = m.material_id
        ORDER BY ri.request_item_id
    """)
    items = cur.fetchall()
    cur.close()
    return items

def get_request_item(request_item_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM request_items
        WHERE request_item_id=%s
    """, (request_item_id,))
    item = cur.fetchone()
    cur.close()
    return item

def update_request_item(request_item_id, material_id, quantity):
    cur = conn.cursor()
    cur.execute("""
        UPDATE request_items
        SET material_id=%s,
            quantity=%s
        WHERE request_item_id=%s
    """, (material_id, quantity, request_item_id))
    conn.commit()
    cur.close()

def delete_request_item(request_item_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM request_items
        WHERE request_item_id=%s
    """, (request_item_id,))
    conn.commit()
    cur.close()


def create_payment(
    purchase_order_id,
    amount,
    request.form["payment_method"]
)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO payments
        (
            purchase_order_id,
            payment_date,
            amount,
            payment_method,
            status
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            'Pending'
        )
    """, (
        purchase_order_id,
        date.today(),
        amount,
        payment_method
    ))
    conn.commit()
    cur.close()


def get_payment(payment_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM payments
        WHERE payment_id=%s
    """, (payment_id,))
    payment = cur.fetchone()
    cur.close()
    return payment

def update_payment(payment_id, amount, payment_method):
    cur = conn.cursor()
    cur.execute("""
        UPDATE payments
        SET payment_date=%s,
            amount=%s,
            payment_method=%s
        WHERE payment_id=%s
    """, (
        payment_date,
        amount,
        payment_method,
        payment_id
    ))
    conn.commit()
    cur.close()

def delete_payment(payment_id):
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM payments
        WHERE payment_id=%s
    """, (payment_id,))
    conn.commit()
    cur.close()

def approve_payment(payment_id):
    cur = conn.cursor()
    # Get payment details
    cur.execute("""
        SELECT
            purchase_order_id,
            amount,
            status
        FROM payments
        WHERE payment_id = %s
    """, (payment_id,))
    payment = cur.fetchone()
    if payment is None:
        cur.close()
        return
    purchase_order_id = payment[0]
    amount = payment[1]
    status = payment[2]
    # Don't approve twice
    if status == "Approved":
        cur.close()
        return
    # Get current balance
    cur.execute("""
        SELECT balance
        FROM purchase_orders
        WHERE purchase_order_id=%s
    """, (purchase_order_id,))
    current_balance = cur.fetchone()[0]
    # Prevent overpayment
    if amount > current_balance:
        cur.close()
        return
    # Calculate new balance
    new_balance = current_balance - amount
    if new_balance < 0:
        new_balance = 0
    # Approve payment
    cur.execute("""
        UPDATE payments
        SET status='Approved',
            approved_date=CURRENT_DATE
        WHERE payment_id=%s
    """, (payment_id,))
    # Update balance
    cur.execute("""
        UPDATE purchase_orders
        SET balance=%s
        WHERE purchase_order_id=%s
    """, (
        new_balance,
        purchase_order_id
    ))
    # Update purchase order status
    if new_balance == 0:
        cur.execute("""
            UPDATE purchase_orders
            SET payment_status='Paid'
            WHERE purchase_order_id=%s
        """, (purchase_order_id,))
    else:
        cur.execute("""
            UPDATE purchase_orders
            SET payment_status='Partially Paid'
            WHERE purchase_order_id=%s
        """, (purchase_order_id,))
    conn.commit()
    cur.close()

def reject_payment(payment_id):
    cur = conn.cursor()
    # Check current status
    cur.execute("""
        SELECT status
        FROM payments
        WHERE payment_id=%s
    """, (payment_id,))
    payment = cur.fetchone()
    if payment is None:
        cur.close()
        return
    # Don't reject twice
    if payment[0] == "Rejected":
        cur.close()
        return
    # Update status
    cur.execute("""
        UPDATE payments
        SET status='Rejected'
        WHERE payment_id=%s
    """, (payment_id,))
    conn.commit()
    cur.close()

def total_payments():
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM payments
    """)
    total = cur.fetchone()[0]
    cur.close()
    return total

def pending_payments():
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM payments
        WHERE status='Pending'
    """)
    total = cur.fetchone()[0]
    cur.close()
    return total

def approved_payments():
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM payments
        WHERE status='Approved'
    """)
    total = cur.fetchone()[0]
    cur.close()
    return total


def rejected_payments():
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM payments
        WHERE status='Rejected'
    """)
    total = cur.fetchone()[0]
    cur.close()
    return total

def get_purchase_orders():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            purchase_orders.purchase_order_id,
            suppliers.supplier_name,
            purchase_orders.order_date,
            purchase_orders.total_amount,
            purchase_orders.balance,
            purchase_orders.payment_status
        FROM purchase_orders
        JOIN suppliers
            ON purchase_orders.supplier_id = suppliers.supplier_id
        ORDER BY purchase_orders.purchase_order_id DESC
    """)
    purchase_orders = cur.fetchall()
    cur.close()
    return purchase_orders

def get_purchase_order_balance(purchase_order_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT total_amount
        FROM purchase_orders
        WHERE purchase_order_id=%s
    """, (purchase_order_id,))
    total = cur.fetchone()[0]
   cur.execute("""
    SELECT COALESCE(SUM(amount),0)
    FROM payments
    WHERE purchase_order_id=%s
    AND status='Approved'
""", (purchase_order_id,))
    paid = cur.fetchone()[0]
    cur.close()
    return total - paid

def get_low_stock():
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM materials
        WHERE quantity < 20
        ORDER BY quantity ASC
    """)
    materials = cur.fetchall()
    cur.close()
    return materials

def get_recent_activity():
    cur = conn.cursor()
    cur.execute("""
        SELECT
            'Material Request Submitted' AS activity,
            users.username,
            material_requests.request_date
        FROM material_requests
        JOIN users
        ON material_requests.requested_by = users.user_id

        UNION

        SELECT
            'Stock Received',
            users.username,
            stock_in.received_date
        FROM stock_in
        JOIN users
        ON stock_in.received_by = users.user_id

        ORDER BY 3 DESC
        LIMIT 10
    """)
    activities = cur.fetchall()
    cur.close()
    return activities

if __name__ == "__main__":
    create_project(
        "Apartment Block",
        "Nairobi",
        5000000
    )
    print(get_projects())