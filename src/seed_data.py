"""Generate a reproducible synthetic employee dataset with NumPy and load it into SQLite."""
import numpy as np
from datetime import date, timedelta

from database import add_employee, count_employees

DEPARTMENTS = {
    # name: (base salary in INR/yr, job titles)
    "Engineering": (900_000, ["Software Engineer", "Senior Engineer", "QA Engineer", "DevOps Engineer"]),
    "Data Science": (1_000_000, ["Data Analyst", "Data Scientist", "ML Engineer"]),
    "Sales": (600_000, ["Sales Executive", "Account Manager", "Sales Lead"]),
    "Marketing": (550_000, ["Marketing Executive", "Content Strategist", "SEO Specialist"]),
    "HR": (500_000, ["HR Executive", "Recruiter", "HR Manager"]),
    "Finance": (700_000, ["Accountant", "Financial Analyst", "Finance Manager"]),
}

FIRST = ["Aarav", "Vivaan", "Aditya", "Ishaan", "Rohan", "Karan", "Arjun", "Rahul",
         "Ananya", "Diya", "Priya", "Sneha", "Neha", "Pooja", "Kavya", "Riya",
         "Meera", "Isha", "Sanjay", "Amit", "Vikram", "Nikhil", "Tanvi", "Shreya"]
LAST = ["Sharma", "Verma", "Patel", "Gupta", "Singh", "Mehta", "Joshi", "Iyer",
        "Nair", "Reddy", "Khan", "Das", "Chauhan", "Mishra", "Yadav", "Jain"]


def generate_employees(n=300, seed=42):
    rng = np.random.default_rng(seed)
    dept_names = list(DEPARTMENTS)
    dept_weights = np.array([0.30, 0.15, 0.20, 0.12, 0.08, 0.15])

    rows = []
    today = date(2026, 10, 22)
    for _ in range(n):
        dept = rng.choice(dept_names, p=dept_weights)
        base, titles = DEPARTMENTS[dept]
        title = rng.choice(titles)
        gender = rng.choice(["Male", "Female"], p=[0.55, 0.45])
        age = int(np.clip(rng.normal(32, 6), 22, 58))
        experience = float(np.clip(age - 22 - rng.uniform(0, 3), 0, 35))
        experience = round(experience, 1)
        hire_date = today - timedelta(days=int(min(experience, 15) * 365 * rng.uniform(0.5, 1.0)))

        title_bump = 1.0 + 0.25 * titles.index(title) / max(len(titles) - 1, 1)
        salary = base * title_bump * (1 + 0.045 * experience) * rng.normal(1.0, 0.07)
        salary = round(float(salary), -2)

        performance = round(float(np.clip(rng.normal(3.5, 0.7), 1.0, 5.0)), 1)
        name = f"{rng.choice(FIRST)} {rng.choice(LAST)}"

        rows.append((name, str(dept), str(title), str(gender), age,
                     hire_date.isoformat(), experience, salary, performance))
    return rows


def seed_database(conn, n=300, seed=42):
    if count_employees(conn) > 0:
        return 0
    rows = generate_employees(n, seed)
    for r in rows:
        add_employee(conn, *r)
    return len(rows)
