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


if __name__ == "__main__":

    create_project(
        "Apartment Block",
        "Nairobi",
        5000000
    )

    print(get_projects())