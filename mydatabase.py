import psycopg2

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
    cur.execute("SELECT * FROM projects")
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



if __name__ == "__main__":
    create_project(
        "Apartment Block",
        "Nairobi",
        5000000
    )
    print(get_projects())