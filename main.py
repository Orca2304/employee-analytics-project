"""Run the full pipeline: create DB -> seed data -> analyse -> charts -> report."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import pandas as pd

import analysis as an
import visualize as viz
from database import get_connection, init_db, count_employees
from seed_data import seed_database

OUT = Path(__file__).resolve().parent / "outputs"


def fmt_inr(x):
    return f"Rs {x:,.0f}"


def main():
    OUT.mkdir(exist_ok=True)
    conn = get_connection()
    init_db(conn)
    added = seed_database(conn)
    print(f"Database ready: {count_employees(conn)} employees ({added} newly added)\n")

    df = an.load_dataframe(conn)

    dept = an.sql_department_summary(conn)
    top = an.sql_top_earners(conn)
    stats = an.salary_statistics(df)
    means, gap = an.gender_pay_gap(df)
    corr_exp = an.experience_salary_correlation(df)
    corr_perf = an.performance_salary_correlation(df)
    slope, intercept = an.salary_fit(df)
    outliers = an.detect_salary_outliers(df)
    performers = an.top_performers(df)

    dept.to_csv(OUT / "department_summary.csv", index=False)
    top.to_csv(OUT / "top_earners.csv", index=False)
    outliers.to_csv(OUT / "salary_outliers.csv", index=False)
    performers.to_csv(OUT / "top_performers.csv", index=False)

    lines = []
    lines.append("EMPLOYEE DATA ANALYTICS REPORT")
    lines.append("=" * 40)
    lines.append(f"Total employees : {len(df)}")
    lines.append(f"Departments     : {df['department'].nunique()}")
    lines.append("")
    lines.append("Salary statistics")
    for k, v in stats.items():
        lines.append(f"  {k:<7}: {fmt_inr(v)}")
    lines.append("")
    lines.append("Department summary (SQL GROUP BY)")
    lines.append(dept.to_string(index=False))
    lines.append("")
    lines.append("Average salary by gender")
    for g, v in means.items():
        lines.append(f"  {g:<7}: {fmt_inr(v)}")
    lines.append(f"  Raw pay gap (Male vs Female): {gap:.2f}%")
    lines.append("  (Unadjusted: does not control for role, department or experience.)")
    lines.append("")
    lines.append(f"Correlation experience-salary : {corr_exp:.3f}")
    lines.append(f"Correlation performance-salary: {corr_perf:.3f}")
    lines.append(f"Linear fit: each extra year of experience ~ {fmt_inr(slope)} more salary")
    lines.append("")
    lines.append(f"Salary outliers within department (|z| > 2.5): {len(outliers)}")
    lines.append("")
    lines.append("Top 5 earners")
    lines.append(top.head(5).to_string(index=False))

    report = "\n".join(lines)
    (OUT / "report.txt").write_text(report, encoding="utf-8")
    print(report)

    paths = viz.make_all(df)
    print(f"\nSaved {len(paths)} charts to {viz.PLOT_DIR}")
    conn.close()


if __name__ == "__main__":
    main()
