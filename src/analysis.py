"""Analysis using SQL (SQLite), Pandas and NumPy."""
import numpy as np
import pandas as pd


def load_dataframe(conn):
    df = pd.read_sql_query("SELECT * FROM employees", conn, parse_dates=["hire_date"])
    return df


# ---------- SQL-based insights ----------
def sql_department_summary(conn):
    query = """
        SELECT department,
               COUNT(*)                    AS headcount,
               ROUND(AVG(salary), 0)       AS avg_salary,
               ROUND(MIN(salary), 0)       AS min_salary,
               ROUND(MAX(salary), 0)       AS max_salary,
               ROUND(AVG(performance), 2)  AS avg_performance
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC
    """
    return pd.read_sql_query(query, conn)


def sql_top_earners(conn, n=10):
    query = """
        SELECT emp_id, name, department, job_title, salary
        FROM employees
        ORDER BY salary DESC
        LIMIT ?
    """
    return pd.read_sql_query(query, conn, params=(n,))


# ---------- Pandas / NumPy insights ----------
def salary_statistics(df):
    s = df["salary"].to_numpy()
    return {
        "mean": float(np.mean(s)),
        "median": float(np.median(s)),
        "std": float(np.std(s, ddof=1)),
        "p25": float(np.percentile(s, 25)),
        "p75": float(np.percentile(s, 75)),
        "p90": float(np.percentile(s, 90)),
    }


def gender_pay_gap(df):
    g = df.groupby("gender")["salary"].mean()
    if {"Male", "Female"} <= set(g.index):
        gap = (g["Male"] - g["Female"]) / g["Male"] * 100
    else:
        gap = float("nan")
    return g.round(0), float(gap)


def experience_salary_correlation(df):
    return float(np.corrcoef(df["experience"], df["salary"])[0, 1])


def performance_salary_correlation(df):
    return float(np.corrcoef(df["performance"], df["salary"])[0, 1])


def salary_fit(df):
    """Linear fit: salary ~ experience (NumPy polyfit). Returns slope, intercept."""
    slope, intercept = np.polyfit(df["experience"], df["salary"], 1)
    return float(slope), float(intercept)


def detect_salary_outliers(df, z_thresh=2.5):
    """Flag employees whose salary is an outlier within their department (z-score)."""
    grp = df.groupby("department")["salary"]
    z = (df["salary"] - grp.transform("mean")) / grp.transform("std")
    out = df.assign(z_score=z.round(2))
    return out[np.abs(out["z_score"]) > z_thresh][
        ["emp_id", "name", "department", "job_title", "salary", "z_score"]
    ]


def hiring_trend(df):
    return df.groupby(df["hire_date"].dt.year).size().rename("hires")


def add_experience_bands(df):
    bins = [-0.1, 2, 5, 10, 20, 100]
    labels = ["0-2 yrs", "2-5 yrs", "5-10 yrs", "10-20 yrs", "20+ yrs"]
    return df.assign(exp_band=pd.cut(df["experience"], bins=bins, labels=labels))


def top_performers(df, n=10):
    return (df.sort_values(["performance", "salary"], ascending=[False, True])
              .head(n)[["emp_id", "name", "department", "performance", "salary"]])
