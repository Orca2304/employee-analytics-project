"""Matplotlib / Seaborn-free charts (matplotlib only, to keep dependencies small)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless-safe
import matplotlib.pyplot as plt
import numpy as np

from analysis import add_experience_bands, salary_fit

PLOT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "charts"
COLORS = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B8EA5", "#6A994E"]


def _save(fig, name):
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    path = PLOT_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def headcount_by_department(df):
    counts = df["department"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(counts.index, counts.values, color=COLORS[: len(counts)])
    ax.bar_label(bars)
    ax.set_title("Headcount by Department")
    ax.set_ylabel("Employees")
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    return _save(fig, "01_headcount_by_department.png")


def avg_salary_by_department(df):
    avg = df.groupby("department")["salary"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(avg.index, avg.values / 1e5, color="#2E86AB")
    ax.set_title("Average Salary by Department")
    ax.set_xlabel("Salary (lakh INR / year)")
    return _save(fig, "02_avg_salary_by_department.png")


def salary_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["salary"] / 1e5, bins=25, color="#6A994E", edgecolor="white")
    ax.axvline(df["salary"].median() / 1e5, color="#C73E1D", ls="--", label="Median")
    ax.set_title("Salary Distribution")
    ax.set_xlabel("Salary (lakh INR / year)")
    ax.set_ylabel("Employees")
    ax.legend()
    return _save(fig, "03_salary_distribution.png")


def experience_vs_salary(df):
    slope, intercept = salary_fit(df)
    x = np.linspace(df["experience"].min(), df["experience"].max(), 50)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["experience"], df["salary"] / 1e5, alpha=0.5, color="#A23B72", s=18)
    ax.plot(x, (slope * x + intercept) / 1e5, color="black", lw=2, label="Linear fit")
    ax.set_title("Experience vs Salary")
    ax.set_xlabel("Experience (years)")
    ax.set_ylabel("Salary (lakh INR / year)")
    ax.legend()
    return _save(fig, "04_experience_vs_salary.png")


def salary_boxplot_by_department(df):
    depts = sorted(df["department"].unique())
    data = [df.loc[df["department"] == d, "salary"] / 1e5 for d in depts]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.boxplot(data, tick_labels=depts)
    ax.set_title("Salary Spread by Department")
    ax.set_ylabel("Salary (lakh INR / year)")
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    return _save(fig, "05_salary_boxplot_by_department.png")


def hiring_trend_chart(df):
    trend = df.groupby(df["hire_date"].dt.year).size()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(trend.index, trend.values, marker="o", color="#F18F01")
    ax.set_title("Hiring Trend by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Hires")
    return _save(fig, "06_hiring_trend.png")


def gender_salary_by_band(df):
    banded = add_experience_bands(df)
    pivot = banded.pivot_table(index="exp_band", columns="gender",
                               values="salary", aggfunc="mean", observed=True) / 1e5
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot.plot(kind="bar", ax=ax, color=["#A23B72", "#2E86AB"])
    ax.set_title("Average Salary by Experience Band and Gender")
    ax.set_ylabel("Salary (lakh INR / year)")
    ax.set_xlabel("")
    plt.setp(ax.get_xticklabels(), rotation=0)
    return _save(fig, "07_gender_salary_by_band.png")


def performance_by_department(df):
    avg = df.groupby("department")["performance"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(avg.index, avg.values, color="#3B8EA5")
    ax.set_xlim(0, 5)
    ax.set_title("Average Performance Rating by Department")
    ax.set_xlabel("Rating (1-5)")
    return _save(fig, "08_performance_by_department.png")


def make_all(df):
    return [
        headcount_by_department(df),
        avg_salary_by_department(df),
        salary_distribution(df),
        experience_vs_salary(df),
        salary_boxplot_by_department(df),
        hiring_trend_chart(df),
        gender_salary_by_band(df),
        performance_by_department(df),
    ]
