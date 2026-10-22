
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from src.database import get_connection

# 1. Connect to the existing SQLite database
conn = get_connection()

# 2. Load employee data into a Pandas DataFrame
df = pd.read_sql_query(
    "SELECT * FROM employees",
    conn
)

conn.close()

# 3. Create output folder
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# 4. Explore the dataset
print("\nFirst 5 employees:")
print(df.head())

print("\nDataset shape (rows, columns):")
print(df.shape)

print("\nColumn information:")
df.info()

print("\nMissing values:")
print(df.isnull().sum())

# 5. Basic salary analysis
print("\nSalary statistics:")
print(df["salary"].describe())

print("\nAverage salary by department:")
dept_salary = (
    df.groupby("department")["salary"]
    .mean()
    .sort_values(ascending=False)
)
print(dept_salary)

# 6. Count employees in each department
print("\nEmployees per department:")
print(df["department"].value_counts())

# 7. Save the analyse data
df.to_csv(output_dir / "employee_data.csv", index=False)
dept_salary.to_csv(output_dir / "department_salary.csv")

# 8. Plot average salary by department
dept_salary.plot(kind="bar", title="Average Salary by Department")
plt.label("Department")
plt.labe("Average Salary")
plt.ticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / "department_salary.png")
plt.show()

print("\nAnalysis complete! Check the outputs folder.")
