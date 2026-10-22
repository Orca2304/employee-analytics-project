"""SQLite database layer: schema + CRUD operations for employee records."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "employees.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS employees (
    emp_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    department   TEXT    NOT NULL,
    job_title    TEXT    NOT NULL,
    gender       TEXT,
    age          INTEGER,
    hire_date    TEXT    NOT NULL,
    experience   REAL,
    salary       REAL    NOT NULL,
    performance  REAL
);
"""


def get_connection(db_path=DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    conn.commit()


# ---------- CRUD ----------
def add_employee(conn, name, department, job_title, gender, age,
                 hire_date, experience, salary, performance):
    cur = conn.execute(
        """INSERT INTO employees
           (name, department, job_title, gender, age, hire_date,
            experience, salary, performance)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (name, department, job_title, gender, age, hire_date,
         experience, salary, performance),
    )
    conn.commit()
    return cur.lastrowid


def get_employee(conn, emp_id):
    return conn.execute(
        "SELECT * FROM employees WHERE emp_id = ?", (emp_id,)
    ).fetchone()


def search_employees(conn, keyword):
    like = f"%{keyword}%"
    return conn.execute(
        """SELECT * FROM employees
           WHERE name LIKE ? OR department LIKE ? OR job_title LIKE ?""",
        (like, like, like),
    ).fetchall()


def update_salary(conn, emp_id, new_salary):
    cur = conn.execute(
        "UPDATE employees SET salary = ? WHERE emp_id = ?", (new_salary, emp_id)
    )
    conn.commit()
    return cur.rowcount


def delete_employee(conn, emp_id):
    cur = conn.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
    conn.commit()
    return cur.rowcount


def count_employees(conn):
    return conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
